from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect

from .models import Producer, District, LocalBody, Ward, Animal
from .forms import ProducerForm, AdditionalProducerForm
from .utils import create_address_json


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class ProducerView(View):

    def get_user_producer_model(self, session):
        producer_model_pk = session.get('producer_model_pk')
        if not producer_model_pk:
            return None

        try:
            return Producer.objects.get(pk=producer_model_pk)
        except Producer.DoesNotExist:
            del producer_model_pk

        return None

    def get_initials_form(self, producer_model):
        districts = District.objects.filter(name=producer_model.district, localbody__name=producer_model.local_body,
                                            localbody__ward__number=producer_model.ward)

        local_bodies = LocalBody.objects.filter(district__name=producer_model.district,
                                                name=producer_model.local_body)

        wards = Ward.objects.filter(number=producer_model.ward, local_body__name=producer_model.local_body,
                                    local_body__district__name=producer_model.district)

        if districts.count() > 0 or local_bodies.count() > 0 or wards.count() > 0:
            return {
                'district': districts.first(),
                'local_body': local_bodies.first(),
                'ward': wards.first()
            }

        return {}

    def get(self, request):
        next_form = request.GET.get('next_form', 'false')
        user_producer_model = self.get_user_producer_model(request.session)

        if next_form == 'true' and not user_producer_model:
            # Producer model don't exist, so ask user to again fill the form from first
            return redirect(reverse('producer'))

        # User has previously submitted form and its instance exists in database
        if user_producer_model:
            if next_form == "true":
                initial = {}
                cows = Animal.objects.filter(name__iexact='cow').all()

                if cows.count() > 0:
                    initial['milk_source'] = cows.first()

                form = AdditionalProducerForm(instance=user_producer_model, initial=initial)
            else:
                form = ProducerForm(instance=user_producer_model, initial=self.get_initials_form(user_producer_model))

        else:
            form = ProducerForm()

        addresses = create_address_json()

        return render(request, 'producer.html', {
            'form': form,
            'addresses': addresses
        })

    def post(self, request):
        next_form = request.GET.get('next_form', 'false')  # toggles form
        user_producer_model = self.get_user_producer_model(request.session)

        if user_producer_model and next_form == 'true':
            form = AdditionalProducerForm(data=request.POST, instance=user_producer_model)

        else:
            if user_producer_model:
                form = ProducerForm(data=request.POST, files=request.FILES, instance=user_producer_model)
            else:
                form = ProducerForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            model = form.save(commit=False)

            # Copy address from form to model
            if type(form) == ProducerForm:
                # In the future, available address may be changed or removed, so instead we copy data
                model.district = form.cleaned_data['district'].name
                model.local_body = form.cleaned_data['local_body'].name
                model.ward = form.cleaned_data['ward'].number
                model.save()

                # Store user model to session
                request.session['producer_model_pk'] = model.pk
                return redirect(f'{reverse("producer")}?next_form=true')

            else:
                model.save()
                return redirect(request.path)

        addresses = create_address_json()

        return render(request, 'producer.html', {
            'form': form,
            'addresses': addresses
        })
