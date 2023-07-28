from typing import List
import json

from .models import District, LocalBody


def get_wards(local_body: LocalBody) -> List[dict]:
    wards = []
    for ward in local_body.ward_set.all():
        wards.append({
            'id': ward.id,
            'number': ward.number
        })

    return wards


def get_local_bodies(district: District) -> List[dict]:
    local_bodies = []

    for local_body in district.localbody_set.all():
        local_bodies.append({
            'id': local_body.id,
            'name': local_body.name,
            'wards': get_wards(local_body)
        })

    return local_bodies


def get_districts() -> List[dict]:
    districts = []
    for district in District.objects.all():
        districts.append({
            'id': district.id,
            'name': district.name,
            'local_bodies': get_local_bodies(district)
        })

    return districts


def create_address_json() -> json:
    return json.dumps({
        "districts": get_districts()
    })
