import pandas as pd

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
