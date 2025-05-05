from datetime import datetime, timedelta
import random
import os
import requests
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# NASA API key - Get one from https://api.nasa.gov/
NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')  # DEMO_KEY has limited requests

def get_historical_weather_data(location: str, days: int = 7) -> List[Dict[str, Any]]:
    """Fetch historical weather data for the specified location"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return get_simulated_historical_weather(location, days)
    
    try:
        # Get coordinates for the location
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data:
            raise Exception(f"Location {location} not found")
        
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        
        # Get historical data
        historical_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            timestamp = int(date.timestamp())
            
            url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&units=metric&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if 'current' in data:
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature': round(data['current']['temp'], 1),
                    'condition': data['current']['weather'][0]['main'],
                    'humidity': data['current']['humidity'],
                    'wind_speed': round(data['current']['wind_speed'], 1)
                })
        
        return historical_data
        
    except Exception as e:
        print(f"Error fetching historical weather data: {str(e)}")
        return get_simulated_historical_weather(location, days)

def get_simulated_historical_weather(location: str, days: int) -> List[Dict[str, Any]]:
    """Generate simulated historical weather data"""
    base_temp = 20 if location.lower() == 'earth' else -63
    base_humidity = 65 if location.lower() == 'earth' else 0
    base_wind = 10 if location.lower() == 'earth' else 30
    
    conditions = ['Sunny', 'Partly Cloudy', 'Clear'] if location.lower() == 'earth' else ['Dusty', 'Clear', 'Dust Storm']
    
    historical_data = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        temp_change = random.uniform(-2, 2)
        humidity_change = random.uniform(-5, 5)
        wind_change = random.uniform(-2, 2)
        
        historical_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': round(base_temp + temp_change, 1),
            'condition': random.choice(conditions),
            'humidity': round(base_humidity + humidity_change),
            'wind_speed': round(base_wind + wind_change, 1)
        })
    
    return historical_data

def get_weather_data():
    """Get current weather data for Earth and Mars."""
    weather_data = {}
    
    # Get Earth weather
    weather_data['earth'] = get_earth_weather()
    
    # Get Mars weather
    weather_data['mars'] = get_mars_weather()
    
    return weather_data

def get_earth_weather():
    """Get current weather data for Earth using OpenWeatherMap API."""
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            return {
                'temperature': 20,
                'condition': 'Sunny',
                'humidity': 65,
                'wind_speed': 10,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'note': 'Using simulated data (OpenWeatherMap API key not found)'
            }
        
        # Get weather for a specific location (e.g., New York)
        city = "New York"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'temperature': round(data['main']['temp']),
                'condition': data['weather'][0]['main'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6),  # Convert m/s to km/h
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {
                'temperature': 20,
                'condition': 'Sunny',
                'humidity': 65,
                'wind_speed': 10,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'note': f'Error fetching weather data: {data.get("message", "Unknown error")}'
            }
    except Exception as e:
        return {
            'temperature': 20,
            'condition': 'Sunny',
            'humidity': 65,
            'wind_speed': 10,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'note': f'Error: {str(e)}'
        }

def get_mars_weather():
    """Get current weather data for Mars using NASA's InSight API."""
    try:
        url = f"https://api.nasa.gov/insight_weather/?api_key={NASA_API_KEY}&feedtype=json&ver=1.0"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and 'sol_keys' in data:
            # Get the most recent sol (Martian day)
            latest_sol = data['sol_keys'][-1]
            sol_data = data[latest_sol]
            
            # Convert temperature from Celsius to Fahrenheit and back to Celsius
            # (NASA provides data in Fahrenheit)
            temp_f = (sol_data['AT']['av'] + sol_data['AT']['mn'] + sol_data['AT']['mx']) / 3
            temp_c = (temp_f - 32) * 5/9
            
            return {
                'temperature': round(temp_c, 1),
                'condition': 'Clear',  # Mars weather is typically clear
                'humidity': 0,  # Mars has very low humidity
                'wind_speed': round(sol_data['HWS']['av'] * 3.6, 1),  # Convert m/s to km/h
                'pressure': round(sol_data['PRE']['av'], 1),  # Pressure in Pa
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sol': latest_sol,  # Martian day
                'note': 'Data from NASA InSight Mission'
            }
        else:
            return {
                'temperature': -63,
                'condition': 'Clear',
                'humidity': 0,
                'wind_speed': 7,
                'pressure': 700,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'note': 'Using simulated Mars data (API limit reached or error)'
            }
    except Exception as e:
        return {
            'temperature': -63,
            'condition': 'Clear',
            'humidity': 0,
            'wind_speed': 7,
            'pressure': 700,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'note': f'Error: {str(e)}'
        }

def get_historical_weather_data(planet):
    """Get historical weather data for the specified planet."""
    if planet.lower() == 'mars':
        return get_historical_mars_weather()
    else:
        return get_historical_earth_weather()

def get_historical_mars_weather():
    """Get historical weather data for Mars using NASA's InSight API."""
    try:
        url = f"https://api.nasa.gov/insight_weather/?api_key={NASA_API_KEY}&feedtype=json&ver=1.0"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and 'sol_keys' in data:
            historical_data = []
            for sol in data['sol_keys']:
                sol_data = data[sol]
                # Convert temperature from Fahrenheit to Celsius
                temp_f = (sol_data['AT']['av'] + sol_data['AT']['mn'] + sol_data['AT']['mx']) / 3
                temp_c = (temp_f - 32) * 5/9
                
                # Calculate Earth date from sol
                earth_date = datetime.now() - timedelta(days=len(data['sol_keys']) - int(sol))
                
                historical_data.append({
                    'date': earth_date.strftime('%Y-%m-%d'),
                    'temperature': round(temp_c, 1),
                    'wind_speed': round(sol_data['HWS']['av'] * 3.6, 1),  # Convert m/s to km/h
                    'pressure': round(sol_data['PRE']['av'], 1),
                    'sol': sol
                })
            return historical_data
        else:
            return generate_simulated_mars_data()
    except Exception as e:
        print(f"Error fetching Mars historical data: {e}")
        return generate_simulated_mars_data()

def get_historical_earth_weather():
    """Get historical weather data for Earth."""
    # Generate simulated data for the past 7 days
    historical_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        historical_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': random.uniform(15, 25),
            'humidity': random.uniform(60, 80),
            'wind_speed': random.uniform(5, 15)
        })
    return historical_data

def generate_simulated_mars_data():
    """Generate simulated historical weather data for Mars."""
    historical_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        historical_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': random.uniform(-80, -40),  # Mars temperatures
            'wind_speed': random.uniform(5, 15),
            'pressure': random.uniform(600, 800)  # Mars pressure in Pa
        })
    return historical_data 