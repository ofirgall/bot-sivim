#!/usr/bin/env python3

import json
import requests
import logging
from typing import Callable, List, Tuple
from requests.adapters import HTTPAdapter, Retry

HTTP_ADAPTER = HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.1))

COMPANIES = []

def get_fiber_data(city: str, street: str, house_num: int) -> List[Tuple[str, bool]]:
    return [(company, check(city, street, house_num)) for company, check in COMPANIES]


def fiber_company(func: Callable[[str, str, int], bool]):
    global COMPANIES
    COMPANIES.append((func.__name__, func))

    return func

@fiber_company
def bezeq(city: str, street: str, house_num: int) -> bool:
    logging.info('getting city and street id')
    city_id, street_id, session = bezeq_cellcom_get_city_and_street_id(city, street)
    logging.info(f'city_id: {city_id} street_id: {street_id}')

    payload = {
        "CityId": str(city_id),
        "StreetId": str(street_id),
        "House": str(house_num),
        "Street": street,
        "City": city,
        "Entrance":""
    }
    resp = session.post('http://www.bezeq.co.il/umbraco/api/FormWebApi/CheckAddress', data=payload)
    resp.raise_for_status()
    content = json.loads(resp.content)
    logging.debug(content)

    return content['Status'] == 1

@fiber_company
def partner(city: str, street: str, house_num: int) -> bool:
    return False

@fiber_company
def cellcom(city: str, street: str, house_num: int) -> bool:
    logging.info('getting city and street id')
    city_id, street_id, _ = bezeq_cellcom_get_city_and_street_id(city, street)
    logging.info(f'city_id: {city_id} street_id: {street_id}')

    resp = requests.get(f'https://digital-api.cellcom.co.il/api/Fiber/GetFiberAddressStatus/{city_id}/{street_id}/{house_num}/1')

    resp.raise_for_status()
    content = json.loads(resp.content)
    logging.debug(content)

    for entry in content['Body']['dataInfoList']:
        if entry['tashtitType'] is not None:
            return True

    return False


def bezeq_cellcom_get_city_and_street_id(city: str, street: str) -> Tuple[int, int, requests.Session]:
    session = requests.Session()
    session.mount('http://www.bezeq.co.il', HTTP_ADAPTER)

    logging.info('Getting city id')
    resp = session.get(f'http://www.bezeq.co.il/umbraco/api/FormWebApi/GetAutoCompleteAddressValue?SearchText={city}&SearchType=0&City=')
    resp.raise_for_status()

    content = json.loads(resp.content)
    logging.debug(content)
    city_id = int(content[0]['id'])

    logging.info(f'Getting street id, city_id: {city_id}')
    resp = session.get(f'http://www.bezeq.co.il/umbraco/api/FormWebApi/GetAutoCompleteAddressValue?SearchText={street}&SearchType=1&City={city_id}')
    resp.raise_for_status()

    content = json.loads(resp.content)
    logging.debug(content)
    street_id = int(content[0]['id'])

    return city_id, street_id, session
