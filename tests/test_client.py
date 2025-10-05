from atmospy.models import WeatherData
from atmospy import exceptions
from atmospy.client import WeatherClient
import unittest
from unittest.mock import patch, Mock


class TestWeatherClient(unittest.TestCase):

    def test_init(self):
        # Test successful initialization
        client = WeatherClient(api_key="fake_key")
        self.assertEqual(client.api_key, "fake_key")
        self.assertEqual(client.base_url, "http://api.weatherapi.com/v1")

        # Test initialization with missing API key
        with self.assertRaises(exceptions.MissingAPIKeyError):
            WeatherClient(api_key="")

    @patch('atmospy.client.requests.get')
    def test_make_request_success(self, mock_get):
        # Mock the successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'location': {'name': 'Test City'},
            'current': {'temp_c': 10.0}
        }
        mock_get.return_value = mock_response

        client = WeatherClient(api_key="fake_key")
        response = client._make_request(
            "/current.json", params={'q': 'Test City'})

        self.assertIsInstance(response, WeatherData)
        self.assertEqual(response.location.name, 'Test City')
        mock_get.assert_called_once_with(
            "http://api.weatherapi.com/v1/current.json",
            params={'q': 'Test City', 'key': 'fake_key'},
            timeout=10
        )

    @patch('atmospy.client.requests.get')
    def test_make_request_http_error(self, mock_get):
        # Mock an API error response (e.g., 401 Unauthorized)
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = exceptions.APIRequestError(
            status_code=401, message="Invalid API key")
        mock_get.return_value = mock_response

        client = WeatherClient(api_key="fake_key")
        with self.assertRaises(exceptions.APIRequestError):
            client._make_request("/current.json", params={'q': 'Test City'})

    def test_get_current_weather(self):
        client = WeatherClient(api_key="fake_key")

        # Mock the internal _make_request method
        client._make_request = Mock(return_value="Success")

        # Test with valid city name
        client.get_current_weather(city_name="London")
        client._make_request.assert_called_once_with(
            '/current.json', params={'q': 'London', 'lang': None})

        # Test with missing city name
        with self.assertRaises(exceptions.MissingParamsError):
            client.get_current_weather(city_name="")

    def test_get_forecast(self):
        client = WeatherClient(api_key="fake_key")
        client._make_request = Mock(return_value="Success")

        # Test with valid parameters
        client.get_forecast(city_name="Tokyo", days=5, dt="2025-10-10")
        client._make_request.assert_called_once_with(
            '/forecast.json', params={'q': 'Tokyo', 'days': 5, 'dt': '2025-10-10'})

        # Test with missing city name
        with self.assertRaises(exceptions.MissingParamsError):
            client.get_forecast(city_name="", days=5)

        # Test with invalid days
        with self.assertRaises(ValueError):
            client.get_forecast(city_name="Tokyo", days=15)

        # Test with invalid date format (relies on validate_datetime)
        with self.assertRaises(ValueError):
            client.get_forecast(city_name="Tokyo", days=5, dt="2025/10/10")


if __name__ == '__main__':
    unittest.main()
