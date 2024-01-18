import requests

API_URL = "https://endoflife.date/api/"


class EOLApi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json"})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.close()

    def close(self):
        self.session.close()

    def _get_results(self, endpoint) -> dict:
        res = self.session.get(endpoint)
        res.raise_for_status()
        return res.json()

    def get_product_details(self, product: str) -> dict:
        endpoint = f"{API_URL}/{product}.json"
        return self._get_results(endpoint)

    def get_single_cycle_details(self, product: str, cycle: str) -> dict:
        endpoint = f"{API_URL}/{product}/{cycle}.json"
        return self._get_results(endpoint)

    def get_all_products(self):
        endpoint = f"{API_URL}/all.json"
        return self._get_results(endpoint)
