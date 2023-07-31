from typing import Optional
from abc import ABC

from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import render, redirect

from .models import TradeType, MilkTrade, District, LocalBody, Ward, Animal
from .forms import MilkTradeForm, AdditionalMilkTradeForm
from .utils import create_address_json


# Create your views here.


def get_user_producer_model(session, session_key):
    model_pk: int = session.get(session_key)
    if not model_pk:
        return None

    try:
        return MilkTrade.objects.get(pk=model_pk)
    except MilkTrade.DoesNotExist:
        del model_pk

    return None


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html')


class TradeRequestView(View, ABC):
    model_session_key: Optional[str] = None
    form_fill_url: Optional[str] = None
    trade_type: Optional[TradeType] = None

    def validate_fields(self):
        if not self.model_session_key:
            raise Exception('Please provide model session key')

        if not self.form_fill_url:
            raise Exception('Please provide a form fill url')

        if not self.trade_type:
            raise Exception('Please specify trade type')

    def get_initials_form(self, trade_model) -> dict[str, QuerySet]:
        districts: QuerySet = District.objects.filter(name=trade_model.district, localbody__name=trade_model.local_body,
                                                      localbody__ward__number=trade_model.ward)

        local_bodies: QuerySet = LocalBody.objects.filter(district__name=trade_model.district,
                                                          name=trade_model.local_body)

        wards: QuerySet = Ward.objects.filter(number=trade_model.ward, local_body__name=trade_model.local_body,
                                              local_body__district__name=trade_model.district)

        if districts.count() > 0 or local_bodies.count() > 0 or wards.count() > 0:
            return {
                'district': districts.first(),
                'local_body': local_bodies.first(),
                'ward': wards.first()
            }

        return {}

    def get(self, request):
        next_form = request.GET.get('next_form', 'false')
        user_producer_model = get_user_producer_model(request.session, self.model_session_key)

        if next_form == 'true' and not user_producer_model:
            # model don't exist, so ask user to again fill the form from first
            return redirect(self.form_fill_url)

        # User has previously submitted form and its instance exists in database
        if user_producer_model:
            if next_form == "true":
                initial = {}
                cows = Animal.objects.filter(name__iexact='cow').all()

                if cows.count() > 0:
                    initial['milk_source'] = cows.first()

                form = AdditionalMilkTradeForm(instance=user_producer_model, initial=initial)
            else:
                form = MilkTradeForm(instance=user_producer_model, initial=self.get_initials_form(user_producer_model))

        else:
            form = MilkTradeForm()

        addresses = create_address_json()

        return render(request, 'producer.html', {
            'form': form,
            'addresses': addresses,
            'trade_type': self.trade_type
        })

    def post(self, request):
        next_form: str = request.GET.get('next_form', 'false')  # toggles form
        model = get_user_producer_model(request.session, self.model_session_key)

        if model and next_form == 'true':
            form = AdditionalMilkTradeForm(data=request.POST, instance=model)

        else:
            if model:
                form = MilkTradeForm(data=request.POST, files=request.FILES, instance=model)
            else:
                form = MilkTradeForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            model.trade_type = self.trade_type

            # Copy address from form to model
            if type(form) == MilkTradeForm:
                # In the future, available address may be changed or removed, so instead we copy data
                model.district = form.cleaned_data['district'].name
                model.local_body = form.cleaned_data['local_body'].name
                model.ward = form.cleaned_data['ward'].number

                model.save()

                # Store user model to session
                request.session[self.model_session_key] = model.pk
                return redirect(f'{self.form_fill_url}?next_form=true')

            else:
                model.save()
                # Form submitted successfully, so redirect to success message page
                return redirect(reverse('success'))

        addresses = create_address_json()

        return render(request, 'producer.html', {
            'form': form,
            'addresses': addresses,
            'trade_type': self.trade_type
        })


class ProducerView(TradeRequestView):
    model_session_key = 'producer_trade_pk'
    trade_type = TradeType.SELL
    form_fill_url = reverse_lazy('producer')


class ConsumerView(TradeRequestView):
    model_session_key = 'consumer_trade_pk'
    form_fill_url = reverse_lazy('consumer')
    trade_type = TradeType.BUY
