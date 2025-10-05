from datetime import datetime, timedelta
from atmospy.models import *

""" 
Module for validating date strings in 'YYYY-MM-DD' format and ensuring they fall within a specified range.
Functions:
    validate_format(dt: str) -> bool:
        Checks if the input string matches the 'YYYY-MM-DD' date format.
    validate_datetime(dt: str):
        Validates that the input string is in 'YYYY-MM-DD' format and represents a date between today and the next 14 days.
"""


def validate_format(dt: str) -> bool:
    """
    Validates whether a given string matches the date format 'YYYY-MM-DD'.
    Args:
        dt (str): The date string to validate.
    Returns:
        bool: True if the string matches the format, False otherwise.
    """

    try:
        datetime.strptime(dt, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_datetime(dt: str) -> None | ValueError:
    """
    Validates that the input date string is in the format 'YYYY-MM-DD' and falls within the range from today to the next 14 days.
    Parameters:
        dt (str): The date string to validate.
    Raises:
        ValueError: If the date string is not in the correct format or is not within the allowed date range.
    """
    if not validate_format(dt):
        raise ValueError("The date must be in the format YYYY-MM-DD.")

    today = datetime.now().date()
    final_date = today + timedelta(days=14)
    input_date = datetime.strptime(dt, "%Y-%m-%d").date()

    if not (today <= input_date <= final_date):
        raise ValueError(
            "The date must be between today and the next 14 days.")


def get_object_to(response: dict) -> WeatherData | KeyError:
    """
    Converts a response dictionary into a WeatherData object.
    Args:
        response (dict): A dictionary containing weather data with keys such as 'location', 'current', and optionally 'forecast'.
    Returns:
        WeatherData: An instance of WeatherData populated with the provided response data.
    Raises:
        KeyError: If required keys ('location' or 'current') are missing from the response.
    """
    if 'location' not in response or 'current' not in response:
        raise KeyError("Response must contain 'location' and 'current' keys.")
    data = WeatherData(location=Location(**response.get('location')), current=Current(
        **response.get('current')))
    if 'forecast' in response:
        data.forecast = Forecast(**response.get('forecast'))
    return data
