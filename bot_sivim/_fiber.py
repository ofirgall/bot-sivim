#!/usr/bin/env python3

import json
import requests
from typing import Callable, List, Tuple

COMPANIES = []

def get_fiber_data(city: str, street: str, house_num: int) -> List[Tuple[str, bool]]:
    return [(company, check(city, street, house_num)) for company, check in COMPANIES]


def fiber_company(func: Callable[[str, str, int], bool]):
    global COMPANIES
    COMPANIES.append((func.__name__, func))

    return func

@fiber_company
def bezeq(city: str, street: str, house_num: int) -> bool:
    city_id, street_id = bezeq_cellcom_get_city_and_street_id(city, street)

    payload = {
        "CityId": str(city_id),
        "StreetId": str(street_id),
        "House": str(house_num),
        "Street": street,
        "City": city,
        "Entrance":""
    }
    resp = requests.post('https://www.bezeq.co.il/umbraco/api/FormWebApi/CheckAddress', data=payload)
    resp.raise_for_status()
    content = json.loads(resp.content)

    return content['Status'] == 1

@fiber_company
def partner(city: str, street: str, house_num: int) -> bool:
    return False

@fiber_company
def cellcom(city: str, street: str, house_num: int) -> bool:
    return True


def bezeq_cellcom_get_city_and_street_id(city: str, street: str) -> Tuple[int, int]:
    resp = requests.get(f'https://www.bezeq.co.il/umbraco/api/FormWebApi/GetAutoCompleteAddressValue?SearchText={city}&SearchType=0&City=')
    resp.raise_for_status()

    content = json.loads(resp.content)
    city_id = int(content[0]['id'])

    resp = requests.get(f'https://www.bezeq.co.il/umbraco/api/FormWebApi/GetAutoCompleteAddressValue?SearchText={street}&SearchType=1&City={city_id}')
    resp.raise_for_status()

    content = json.loads(resp.content)
    street_id = int(content[0]['id'])

    return city_id, street_id
