#!/usr/bin/env python3


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
    return True

@fiber_company
def partner(city: str, street: str, house_num: int) -> bool:
    return False

@fiber_company
def cellcom(city: str, street: str, house_num: int) -> bool:
    return True
