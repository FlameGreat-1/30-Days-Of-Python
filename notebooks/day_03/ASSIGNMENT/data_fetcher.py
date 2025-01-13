import random
from datetime import datetime, timedelta

def fetch_current_weather(city):
    return {
        'name': city,
        'main': {
            'temp': round(random.uniform(-10, 40), 2),
            'humidity': random.randint(0, 100)
        },
        'weather': [{'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain', 'thunderstorm', 'snow', 'mist'])}]
    }

def fetch_historical_data(city, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    data = []
    current_date = start_date
    while current_date <= end_date:
        data.append({
            'date': current_date.strftime("%Y-%m-%d"),
            'temp': round(random.uniform(-10, 40), 2),
            'humidity': random.randint(0, 100),
            'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain', 'thunderstorm', 'snow', 'mist'])
        })
        current_date += timedelta(days=1)
    return data
