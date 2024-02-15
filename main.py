from api import EOLApi

API = EOLApi()


def batch(iterable, n=1):
    """
    Generator that yields slices of the iterable, each of size n.

    Args:
        iterable: The iterable to slice.
        n (int): The size of each slice.

    Yields:
        slice: Slices of the iterable, each of size n.
    """
    length = len(iterable)
    for split in range(0, length, n):
        yield iterable[split : min(split + n, length)]


def get_all_products_from_api():
    """
    Fetches all products from the API.

    Returns:
        list: A list of all products.
    """
    return API.get_all_products()


def get_product_details_from_api(product: str, majors_only: bool):
    """
    Fetches the details of a product from the API.

    Args:
        product (str): The name of the product.
        majors_only (bool): Whether to only include major versions.

    Returns:
        list: A list of product details.
    """
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
    """
    Fetches the details of a single cycle of a product from the API.

    Args:
        product (str): The name of the product.
        cycle (str): The name of the cycle.

    Returns:
        dict: The details of the cycle.
    """
    return API.get_single_cycle_details(product=product, cycle=cycle)
