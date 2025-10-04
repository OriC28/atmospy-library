import requests

from functions import get_object_to, validate_datetime
from models import WeatherData
import exceptions

""" Module: client
--------------
This module provides the `WeatherClient` class for interacting with the WeatherAPI service.
It allows users to retrieve current weather and forecast data for a specified city.
Classes:
    WeatherClient: Handles API requests to fetch weather data.
Dependencies:
    - requests: For making HTTP requests.
    - functions.get_object_to: Converts API JSON responses to WeatherData objects.
    - functions.validate_datetime: Validates datetime strings.
    - models.WeatherData: Data model for weather information.
    - exceptions: Custom exception classes for error handling.
Exceptions:
    - exceptions.MissingAPIKeyError: Raised when API key is missing.
    - exceptions.MissingParamsError: Raised when required parameters are missing.
    - exceptions.APIRequestError: Raised when API request fails.
Usage Example:
    client = WeatherClient(api_key="your_api_key")
    current_weather = client.get_current_weather("London")
    forecast = client.get_forecast("London", days=3) """


class WeatherClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise exceptions.MissingAPIKeyError()
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"

    def _make_request(self, endpoint: str, params: dict) -> WeatherData:
        """
        Sends a GET request to the specified API endpoint with provided parameters.
        Args:
            endpoint (str): The API endpoint to send the request to. Must start with '/'.
            params (dict): Dictionary of query parameters to include in the request.
        Returns:
            WeatherData object: The WeatherData object containing the JSON response from the API if the request is successful.
        Raises:
            ValueError: If the endpoint does not start with '/'.
            exceptions.MissingParamsError: If params is empty or None.
            exceptions.APIRequestError: If the request fails or an exception occurs.
        """

        if not endpoint.startswith("/"):
            raise ValueError("Endpoint must start with /")

        if not params or len(params) == 0:
            raise exceptions.MissingParamsError()

        # Integrating endpoint with the entered parameters
        endpoint += "?" + \
            "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        # Creating the url for the request
        url = f"{self.base_url}{endpoint.strip()}&key={self.api_key}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                json_response = response.json()
                # Creating an object from the JSON returned by the API
                object_response = get_object_to(json_response)
                return object_response
        except:
            raise exceptions.APIRequestError(status_code=response.status_code)

    def get_current_weather(self, city_name: str, language: str = None) -> WeatherData:
        """
        Retrieves the current weather information for a specified city.
        Args:
            city_name (str): The name of the city to retrieve weather data for.
            language (str, optional): The language code for the response (e.g., 'en', 'es'). Defaults to None.
        Raises:
            exceptions.MissingParamsError: If the city_name parameter is missing or empty.
        Returns:
            WeatherData object: The current weather data for the specified city.
        """

        if not city_name or len(city_name) == 0:
            raise exceptions.MissingParamsError()
        return self._make_request('/current.json', params={'q': city_name, 'lang': language})

    def get_forecast(self, city_name: str, days: int, dt: str = None):
        if not city_name or len(city_name) == 0 or not days:
            raise exceptions.MissingParamsError()

        if days < 1 or days > 14:
            raise ValueError("Days must be between 1 and 14.")

        if dt:
            validate_datetime(dt)

        return self._make_request('/forecast.json', params={'q': city_name, 'days': days, 'dt': dt})
