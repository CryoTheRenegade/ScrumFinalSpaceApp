from datetime import datetime
import random

def get_weather_data():
    try:
        # This is a placeholder. In a real application, you would use a weather API
        # For demonstration, we'll return mock data with some randomness
        return {
            'earth': {
                'temperature': round(20 + random.uniform(-2, 2), 1),
                'condition': random.choice(['Sunny', 'Partly Cloudy', 'Clear']),
                'humidity': round(65 + random.uniform(-5, 5)),
                'wind_speed': round(10 + random.uniform(-2, 2)),
                'timestamp': datetime.now().isoformat()
            },
            'mars': {
                'temperature': round(-63 + random.uniform(-5, 5), 1),
                'condition': random.choice(['Dusty', 'Clear', 'Dust Storm']),
                'humidity': 0,
                'wind_speed': round(30 + random.uniform(-5, 5)),
                'timestamp': datetime.now().isoformat()
            }
        }
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        # Return fallback data
        return {
            'earth': {
                'temperature': 20,
                'condition': 'Sunny',
                'humidity': 65,
                'wind_speed': 10,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using fallback data due to connection issues'
            },
            'mars': {
                'temperature': -63,
                'condition': 'Dusty',
                'humidity': 0,
                'wind_speed': 30,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using fallback data due to connection issues'
            }
        } 