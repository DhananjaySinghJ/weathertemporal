import requests

def get_weather(city_name, weather_api_key):
    """
    Retrieves weather data for a specified city using the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city for which weather data is requested.
        weather_api_key (str): The API key for accessing the OpenWeatherMap API.

    Returns:
        dict: A dictionary containing weather data for the specified city.
    """
    # Construct the URL for the OpenWeatherMap API request
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={weather_api_key}"
    # Send GET request to the API and retrieve JSON response
    response = requests.get(complete_url)
    data = response.json()
    return data
