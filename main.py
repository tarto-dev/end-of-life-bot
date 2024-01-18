from api import EOLApi
from datetime import datetime, timedelta

API = EOLApi()


def batch(iterable, n=1):
    length = len(iterable)
    for split in range(0, length, n):
        yield iterable[split : min(split + n, length)]


def get_all_products_from_api():
    return API.get_all_products()


def get_product_details_from_api(product: str, majors_only: bool):
    details = API.get_product_details(product=product)
    if majors_only:
        excluded_minors_products = []
        latest_major = 0
        for entry in details:
            if entry["cycle"].split(".")[0] != latest_major:
                excluded_minors_products.append(entry)
                latest_major = entry["cycle"].split(".")[0]

        details = excluded_minors_products
    return details


def get_single_cycle_details_from_api(product, cycle):
    return API.get_single_cycle_details(product=product, cycle=cycle)
