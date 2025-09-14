

class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"

    def _make_request(self, endpoint: str):
        pass

    def get_current_weather(self, city_name: str, country_code: str = None):
        pass

    def get_forecast(self, city_name: str, country_code: str, days: int = None):
        pass

    