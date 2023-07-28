from django import forms
from django.core.exceptions import ValidationError

from .models import District, LocalBody, Ward, Producer, Animal


class ProducerForm(forms.ModelForm):
    district = forms.ModelChoiceField(queryset=District.objects.get_queryset())
    local_body = forms.ModelChoiceField(queryset=LocalBody.objects.get_queryset())
    ward = forms.ModelChoiceField(queryset=Ward.objects.get_queryset())

    def clean_local_body(self):
        """
        This ensures that the district has the selected local body
        """

        district = self.cleaned_data['district']
        local_body = self.cleaned_data['local_body']

        if local_body.district != district:
            raise ValidationError(f'f{district.name} don\'t have {local_body.name}')

        return local_body

    def clean_ward(self):
        """
        This ensures that the local body has the selected ward
        """

        local_body = self.cleaned_data['local_body']
        ward = self.cleaned_data['ward']

        if ward.local_body != local_body:
            raise ValidationError(f'f{local_body.name} don\'t have {ward.number}')

        return ward

    class Meta:
        model = Producer
        fields = ('first_name', 'last_name', 'contact_number', 'google_map_location')


class AdditionalProducerForm(forms.ModelForm):
    milk_source = forms.ModelChoiceField(queryset=Animal.objects.get_queryset(), required=True)
    litre_to_sell = forms.IntegerField(required=True)
    rate_per_litre = forms.IntegerField(required=True)

    class Meta:
        model = Producer
        fields = ('milk_source', 'litre_to_sell', 'rate_per_litre')
