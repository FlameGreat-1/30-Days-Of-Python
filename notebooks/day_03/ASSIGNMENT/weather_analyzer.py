import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

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

def process_current_weather(data):
    return {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description']
    }

def process_historical_data(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def analyze_current_weather(data):
    return f"Current weather in {data['city']}: {data['temperature']}°C, {data['description']}"

def analyze_historical_data(df):
    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    
    return {
        'average_temperature': round(avg_temp, 2),
        'max_temperature': max_temp,
        'min_temperature': min_temp
    }

def plot_temperature_trend(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['temp'])
    plt.title('Temperature Trend')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('temperature_trend.png')
    plt.close()

def plot_temperature_distribution(df):
    plt.figure(figsize=(10, 6))
    df['temp'].hist(bins=20)
    plt.title('Temperature Distribution')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.savefig('temperature_distribution.png')
    plt.close()

def main():
    print("Starting main function...")
    city = "Lagos"  # Default city name
    days = 30  # Default number of days for historical data

    print(f"\nWeather Analysis for {city}")
    print("=" * 30)

    print("Fetching current weather...")
    current_data = fetch_current_weather(city)
    print("Processing current weather...")
    processed_current = process_current_weather(current_data)
    print("Analyzing current weather...")
    current_analysis = analyze_current_weather(processed_current)
    print("\nCurrent Weather:")
    print(current_analysis)

    print("Fetching historical data...")
    historical_data = fetch_historical_data(city, days)
    print("Processing historical data...")
    df = process_historical_data(historical_data)
    print("Analyzing historical data...")
    historical_analysis = analyze_historical_data(df)
    
    print(f"\nHistorical Weather Analysis (Last {days} days):")
    for key, value in historical_analysis.items():
        print(f"{key.replace('_', ' ').title()}: {value}°C")

    print("Generating temperature trend plot...")
    plot_temperature_trend(df)
    print("\nTemperature trend plot saved as 'temperature_trend.png'")
    
    print("Generating temperature distribution plot...")
    plot_temperature_distribution(df)
    print("Temperature distribution plot saved as 'temperature_distribution.png'")

    print("Main function completed.")

if __name__ == "__main__":
    print("Script started.")
    main()
    print("Script ended.")
