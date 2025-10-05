from atmospy.models import WeatherData, Location, Current, Forecast
from atmospy.functions import validate_format, validate_datetime, get_object_to
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch


class TestFunctions(unittest.TestCase):

    def test_validate_format(self):
        self.assertTrue(validate_format("2025-10-20"))
        self.assertFalse(validate_format("20-10-2025"))
        self.assertFalse(validate_format("not a date"))
        self.assertFalse(validate_format("2025-13-01"))

    @patch('atmospy.functions.datetime')
    def test_validate_datetime(self, mock_datetime):
        mock_now = datetime(2025, 10, 5)
        mock_datetime.now.return_value = mock_now
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(
            *args, **kw)

        self.assertIsNone(validate_datetime("2025-10-10"))

        # Test invalid format
        with self.assertRaisesRegex(ValueError, "The date must be in the format YYYY-MM-DD."):
            validate_datetime("10-05-2025")

        # Test date in the past
        with self.assertRaisesRegex(ValueError, "The date must be between today and the next 14 days."):
            validate_datetime("2025-10-04")

        # Test date too far in the future
        with self.assertRaisesRegex(ValueError, "The date must be between today and the next 14 days."):
            validate_datetime("2025-10-25")

    def test_get_object_to(self):
        # Test with valid full response
        response_full = {
            'location': {'name': 'London'},
            'current': {'temp_c': 15.0},
            'forecast': {'forecastday': []}
        }
        weather_data = get_object_to(response_full)
        self.assertIsInstance(weather_data, WeatherData)
        self.assertIsInstance(weather_data.location, Location)
        self.assertIsInstance(weather_data.current, Current)
        self.assertIsInstance(weather_data.forecast, Forecast)
        self.assertEqual(weather_data.location.name, 'London')

        # Test with valid minimal response (no forecast)
        response_minimal = {
            'location': {'name': 'Paris'},
            'current': {'temp_c': 18.0}
        }
        weather_data_minimal = get_object_to(response_minimal)
        self.assertIsInstance(weather_data_minimal, WeatherData)
        self.assertIsNone(weather_data_minimal.forecast)
        self.assertEqual(weather_data_minimal.location.name, 'Paris')

        # Test with missing 'location' key
        with self.assertRaisesRegex(KeyError, "Response must contain 'location' and 'current' keys."):
            get_object_to({'current': {'temp_c': 15.0}})

        # Test with missing 'current' key
        with self.assertRaisesRegex(KeyError, "Response must contain 'location' and 'current' keys."):
            get_object_to({'location': {'name': 'London'}})


if __name__ == '__main__':
    unittest.main()
