from dataclasses import dataclass
from typing import Optional, List

"""
This module defines data models for representing weather information using Python dataclasses.
Classes:
    Condition:
        Represents weather condition details such as description, icon, and code.
    Current:
        Represents current weather data including temperature, last updated time, day/night status, and condition.
    Location:
        Represents geographical location details including name, region, country, coordinates, timezone, and local time.
    Day:
        Represents daily weather summary including max/min temperatures, condition, precipitation, and chances of rain/snow.
    Astro:
        Represents astronomical data such as sunrise and sunset times.
    Hour:
        Represents hourly weather data including time, temperature, condition, feels-like temperature, and chance of rain.
    ForecastDay:
        Represents a single day's forecast including date, daily summary, astronomical data, and hourly breakdown.
    Forecast:
        Represents a weather forecast containing multiple forecast days.
    WeatherData:
        Represents the complete weather data including location, current conditions, and forecast.
"""


@dataclass
class Condition:
    text: Optional[str] = None
    icon: Optional[str] = None
    code: Optional[int] = None


@dataclass
class Current:
    last_updated_epoch: Optional[int] = None
    last_updated: Optional[str] = None
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None
    is_day: Optional[int] = None
    condition: Optional[Condition] = None


@dataclass
class Location:
    name: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz_id: Optional[str] = None
    localtime_epoch: Optional[int] = None
    localtime: Optional[str] = None


@dataclass
class Day:
    maxtemp_c: Optional[float] = None
    mintemp_c: Optional[float] = None
    maxtemp_f: Optional[float] = None
    mintemp_f: Optional[float] = None
    condition: Optional[Condition] = None
    total_precip_mm: Optional[float] = None
    daily_chance_of_rain: Optional[int] = None
    daily_chance_of_snow: Optional[int] = None


@dataclass
class Astro:
    sunrise: Optional[str] = None
    sunset: Optional[str] = None


@dataclass
class Hour:
    time: Optional[str] = None
    temp_c: Optional[float] = None
    condition: Optional[Condition] = None
    feelslike_c: Optional[float] = None
    chance_of_rain: Optional[int] = None


@dataclass
class ForecastDay:
    date: str
    date_epoch: int
    day: Day
    astro: Astro
    hour: List[Hour]


@dataclass
class Forecast:
    forecastday: List[ForecastDay]


@dataclass
class WeatherData:
    location: Optional[Location] = None
    current: Optional[Current] = None
    forecast: Optional[Forecast] = None
