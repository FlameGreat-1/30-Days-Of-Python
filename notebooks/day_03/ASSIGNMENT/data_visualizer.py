import matplotlib.pyplot as plt

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
