import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import seaborn as sns

# Set the style for dark theme
plt.style.use('dark_background')
sns.set_palette("husl")

def generate_weather_chart(historical_data, planet):
    """Generate a weather chart for the given planet's historical data"""
    plt.figure(figsize=(10, 6))
    
    # Extract data
    dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in historical_data]
    temperatures = [d['temperature'] for d in historical_data]
    
    # Create the plot
    plt.plot(dates, temperatures, marker='o', linestyle='-', linewidth=2)
    
    # Customize the plot
    plt.title(f'{planet.capitalize()} Temperature History', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 string
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

def generate_stock_chart(historical_data, company_name):
    """Generate a stock chart for the given company's historical data"""
    plt.figure(figsize=(10, 6))
    
    # Extract data
    dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in historical_data]
    prices = [d['close'] for d in historical_data]
    
    # Create the plot
    plt.plot(dates, prices, marker='o', linestyle='-', linewidth=2)
    
    # Customize the plot
    plt.title(f'{company_name} Stock Price History', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 string
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str 