import requests
from configs import API_URL


class EOLApi:
    def __init__(self):
        """
        Initialize a new EOLApi instance.
        """
        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json"})

    def __enter__(self):
        """
        Support for with statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        """
        Close the session when the with statement is done.
        """
        self.close()

    def close(self):
        """
        Close the current session.
        """
        self.session.close()

    def _get_results(self, endpoint) -> dict:
        """
        Send a GET request to the specified endpoint and return the JSON response.

        Args:
            endpoint (str): The API endpoint to send the GET request to.

        Returns:
            dict: The JSON response from the API.
        """
        res = self.session.get(endpoint)
        res.raise_for_status()
        return res.json()

    def get_product_details(self, product: str) -> dict:
        """
        Get the details of a specific product.

        Args:
            product (str): The name of the product.

        Returns:
            dict: The details of the product.
        """
        endpoint = f"{API_URL}/{product}.json"
        return self._get_results(endpoint)

    def get_single_cycle_details(self, product: str, cycle: str) -> dict:
        """
        Get the details of a specific cycle of a product.

        Args:
            product (str): The name of the product.
            cycle (str): The name of the cycle.

        Returns:
            dict: The details of the cycle.
        """
        endpoint = f"{API_URL}/{product}/{cycle}.json"
        return self._get_results(endpoint)

    def get_all_products(self):
        """
        Get the details of all products.

        Returns:
            dict: The details of all products.
        """
        endpoint = f"{API_URL}/all.json"
        return self._get_results(endpoint)
