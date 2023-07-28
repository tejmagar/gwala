from typing import List
import json

from django.views import View
from django.shortcuts import render

from .models import District, LocalBody, Ward
from .forms import ProducerForm


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class ProducerView(View):
    def get_wards(self, local_body: LocalBody) -> List[dict]:
        wards = []
        for ward in local_body.ward_set.all():
            wards.append({
                'id': ward.id,
                'number': ward.number
            })

        return wards

    def get_local_bodies(self, district: District) -> List[dict]:
        local_bodies = []

        for local_body in district.localbody_set.all():
            local_bodies.append({
                'id': local_body.id,
                'name': local_body.name,
                'wards': self.get_wards(local_body)
            })

        return local_bodies

    def get_districts(self) -> List[dict]:
        districts = []
        for district in District.objects.all():
            districts.append({
                'id': district.id,
                'name': district.name,
                'local_bodies': self.get_local_bodies(district)
            })

        return districts

    def create_address_json(self) -> json:
        return json.dumps({
            "districts": self.get_districts()
        })

    def get(self, request):
        addresses = self.create_address_json()

        return render(request, 'producer.html', {
            'form': ProducerForm,
            'addresses': addresses
        })
