# 🌤️ AtmosPy

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](pyproject.toml)

A modern, type-safe Python client library for accessing weather data through the WeatherAPI.com service. AtmosPy provides a clean, intuitive interface for retrieving current weather conditions and forecasts with comprehensive error handling and data validation.

## ✨ Features

- 🌍 **Current Weather Data**: Get real-time weather information for any location
- 📅 **Weather Forecasts**: Access up to 14-day weather forecasts
- 🔒 **Type Safety**: Full type hints and dataclass-based models
- ⚠️ **Error Handling**: Comprehensive custom exceptions for robust error management
- 🌐 **Multi-language Support**: Get weather data in multiple languages
- ✅ **Input Validation**: Built-in validation for dates and parameters
- 🧪 **Well Tested**: Comprehensive test suite included

## 🚀 Installation

```bash
pip install atmospy
```

## 📋 Requirements

- Python 3.10 or higher
- An API key from [WeatherAPI.com](https://www.weatherapi.com/) (free tier available)

## 🔧 Quick Start

### Basic Usage

```python
from atmospy import WeatherClient

# Initialize the client with your API key
client = WeatherClient(api_key="your_api_key_here")

# Get current weather
current_weather = client.get_current_weather("London")
print(f"Temperature in {current_weather.location.name}: {current_weather.current.temp_c}°C")
print(f"Condition: {current_weather.current.condition.text}")

# Get weather forecast
forecast = client.get_forecast("New York", days=5)
for day in forecast.forecast.forecastday:
    print(f"Date: {day.date}")
    print(f"Max: {day.day.maxtemp_c}°C, Min: {day.day.mintemp_c}°C")
    print(f"Condition: {day.day.condition.text}")
```

### Multi-language Support

```python
# Get weather data in Spanish
weather_es = client.get_current_weather("Madrid", language="es")
print(f"Condición: {weather_es.current.condition.text}")
```

### Forecast with Specific Date

```python
from datetime import datetime, timedelta

# Get forecast for a specific date (within 14 days)
future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
forecast = client.get_forecast("Tokyo", days=1, dt=future_date)
```

## 📚 API Reference

### WeatherClient

The main client class for interacting with the WeatherAPI service.

#### Constructor

```python
WeatherClient(api_key: str)
```

**Parameters:**
- `api_key` (str): Your WeatherAPI.com API key

**Raises:**
- `MissingAPIKeyError`: If the API key is empty or None

#### Methods

##### get_current_weather

```python
get_current_weather(city_name: str, language: str = None) -> WeatherData
```

Retrieve current weather data for a specified location.

**Parameters:**
- `city_name` (str): Name of the city or location
- `language` (str, optional): Language code for the response (e.g., 'en', 'es', 'fr')

**Returns:**
- `WeatherData`: Object containing current weather information

**Raises:**
- `MissingParamsError`: If city_name is empty or None
- `APIRequestError`: If the API request fails

##### get_forecast

```python
get_forecast(city_name: str, days: int, dt: str = None) -> WeatherData
```

Retrieve weather forecast for a specified location.

**Parameters:**
- `city_name` (str): Name of the city or location
- `days` (int): Number of forecast days (1-14)
- `dt` (str, optional): Specific date in YYYY-MM-DD format (within 14 days from today)

**Returns:**
- `WeatherData`: Object containing forecast information

**Raises:**
- `MissingParamsError`: If required parameters are missing
- `ValueError`: If days is not between 1-14 or date format is invalid
- `APIRequestError`: If the API request fails

## 🏗️ Data Models

AtmosPy uses strongly-typed dataclasses to represent weather data:

### WeatherData
Main container for all weather information
- `location`: Location details
- `current`: Current weather conditions  
- `forecast`: Forecast data (when available)

### Location
Geographical information
- `name`, `region`, `country`: Location identifiers
- `lat`, `lon`: Coordinates
- `tz_id`: Timezone identifier
- `localtime`: Local time

### Current
Current weather conditions
- `temp_c`, `temp_f`: Temperature in Celsius/Fahrenheit
- `condition`: Weather condition details
- `is_day`: Day/night indicator
- `last_updated`: Last update timestamp

### Forecast
Forecast information with daily and hourly breakdowns
- `forecastday`: List of daily forecasts
  - `day`: Daily summary (max/min temps, condition, precipitation)
  - `astro`: Astronomical data (sunrise, sunset)
  - `hour`: Hourly weather data

## ⚠️ Exception Handling

AtmosPy provides specific exceptions for different error scenarios:

```python
from atmospy import WeatherClient, exceptions

try:
    client = WeatherClient(api_key="")
except exceptions.MissingAPIKeyError:
    print("Please provide a valid API key")

try:
    weather = client.get_current_weather("")
except exceptions.MissingParamsError:
    print("City name is required")
except exceptions.APIRequestError as e:
    print(f"API Error {e.status_code}: {e}")
```

### Exception Types

- `MissingAPIKeyError`: API key is missing or invalid
- `MissingParamsError`: Required parameters are missing
- `APIRequestError`: API request failed (includes HTTP status code)

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install pytest

# Run tests
pytest tests/
```

## 📖 Examples

### Complete Weather Dashboard Example

```python
from atmospy import WeatherClient, exceptions
from datetime import datetime

def weather_dashboard(api_key: str, city: str):
    try:
        client = WeatherClient(api_key=api_key)
        
        # Current weather
        current = client.get_current_weather(city)
        print(f"\n🌍 Current Weather in {current.location.name}, {current.location.country}")
        print(f"🌡️ Temperature: {current.current.temp_c}°C ({current.current.temp_f}°F)")
        print(f"☁️ Condition: {current.current.condition.text}")
        print(f"🕐 Local Time: {current.location.localtime}")
        
        # 3-day forecast
        forecast = client.get_forecast(city, days=3)
        print(f"\n📅 3-Day Forecast:")
        
        for day in forecast.forecast.forecastday:
            print(f"\n📆 {day.date}")
            print(f"   🌡️ High: {day.day.maxtemp_c}°C | Low: {day.day.mintemp_c}°C")
            print(f"   ☁️ {day.day.condition.text}")
            print(f"   🌧️ Rain Chance: {day.day.daily_chance_of_rain}%")
            print(f"   🌅 Sunrise: {day.astro.sunrise} | 🌇 Sunset: {day.astro.sunset}")
            
    except exceptions.MissingAPIKeyError:
        print("❌ Error: Please provide a valid API key")
    except exceptions.APIRequestError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Usage
if __name__ == "__main__":
    API_KEY = "your_api_key_here"
    weather_dashboard(API_KEY, "London")
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WeatherAPI.com](https://www.weatherapi.com/) for providing the weather data API
- Built with ❤️ using Python dataclasses and type hints

## 📧 Contact

**Author:** OriC28  
**Email:** orianacolina.perea@gmail.com

---

*Made with 🌤️ by [OriC28](mailto:orianacolina.perea@gmail.com)*