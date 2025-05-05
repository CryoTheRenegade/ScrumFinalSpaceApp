from flask import Flask, render_template, jsonify, send_file, session, request, redirect, url_for
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive mode
import seaborn as sns
from utils.stocks import get_stock_data, get_historical_stock_data
from utils.weather import get_weather_data, get_historical_weather_data
from utils.news import get_space_news

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

# Default card order
DEFAULT_CARD_ORDER = ['weather', 'stocks', 'news']

def get_card_order():
    """Get the current card order from session or return default order."""
    return session.get('card_order', DEFAULT_CARD_ORDER)

def set_card_order(new_order):
    """Set the new card order in session."""
    session['card_order'] = new_order

# Set dark theme for plots
plt.style.use('dark_background')
sns.set_theme(style="darkgrid")

def check_api_limits(data):
    """Check if any API calls have hit their limits."""
    api_limits = []
    
    # Check weather API limits
    if isinstance(data.get('weather_data'), dict):
        for planet, weather in data['weather_data'].items():
            if weather.get('note') and ('API limit' in weather['note'] or 'quota' in weather['note'].lower()):
                api_limits.append(f"Weather API ({planet}): {weather['note']}")
    
    # Check stock API limits
    if isinstance(data.get('stocks_data'), dict):
        for symbol, stock in data['stocks_data'].items():
            if stock.get('note') and ('API limit' in stock['note'] or 'quota' in stock['note'].lower()):
                api_limits.append(f"Stock API ({symbol}): {stock['note']}")
    
    # Check news API limits
    if isinstance(data.get('news_data'), dict) and data['news_data'].get('note'):
        if 'API limit' in data['news_data']['note'] or 'quota' in data['news_data']['note'].lower():
            api_limits.append(f"News API: {data['news_data']['note']}")
    
    return api_limits

def generate_stock_chart(symbol):
    """Generate a stock price history chart using Matplotlib."""
    try:
        # Get historical data
        historical_data = get_historical_stock_data(symbol)
        if not historical_data:
            return None

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot the data
        ax.plot(historical_data['timestamp'], historical_data['close'], 
                label='Close Price', linewidth=2)
        
        # Customize the plot
        ax.set_title(f'{symbol} Stock Price History', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    except Exception as e:
        print(f"Error generating stock chart: {e}")
        return None

def generate_weather_chart(planet):
    """Generate a weather history chart using Matplotlib."""
    try:
        # Get historical data
        historical_data = get_historical_weather_data(planet)
        if not historical_data:
            print(f"No historical data available for {planet}")
            return None

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract dates and temperatures
        try:
            # Extract data from the list of dictionaries
            dates = [data['date'] for data in historical_data]
            temperatures = [data['temperature'] for data in historical_data]
            
            # Convert string dates to datetime objects
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
            
            # Plot temperature data
            ax.plot(dates, temperatures, 
                    label='Temperature', linewidth=2)
            
            # Customize the plot
            ax.set_title(f'{planet.capitalize()} Temperature History', pad=20)
            ax.set_xlabel('Date')
            ax.set_ylabel('Temperature (°C)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return buf
            
        except (KeyError, ValueError) as e:
            print(f"Error processing weather data: {e}")
            return None
            
    except Exception as e:
        print(f"Error generating weather chart: {e}")
        return None

@app.route('/')
def index():
    """Render the main dashboard page."""
    # Get data for all sections
    weather_data = get_weather_data()
    stocks_data = get_stock_data()
    news_data = get_space_news()
    
    # Default selected planet for weather chart
    selected_planet = 'earth'
    
    # Check for API limits
    data = {
        'weather_data': weather_data,
        'stocks_data': stocks_data,
        'news_data': news_data
    }
    api_limits = check_api_limits(data)
    
    # Get current card order
    card_order = get_card_order()
    
    return render_template('index.html',
                         weather_data=weather_data,
                         stocks_data=stocks_data,
                         news_data=news_data,
                         selected_planet=selected_planet,
                         api_limits=api_limits,
                         card_order=card_order)

@app.route('/reorder', methods=['POST'])
def reorder():
    """Handle card reordering."""
    new_order = request.form.getlist('order[]')
    if new_order and all(card in DEFAULT_CARD_ORDER for card in new_order):
        set_card_order(new_order)
    return redirect(url_for('index'))

@app.route('/reset-order')
def reset_order():
    """Reset card order to default."""
    session.pop('card_order', None)
    return redirect(url_for('index'))

@app.route('/api/weather')
def weather():
    return jsonify(get_weather_data())

@app.route('/api/stocks')
def stocks():
    return jsonify(get_stock_data())

@app.route('/api/news')
def news():
    return jsonify(get_space_news())

@app.route('/charts/stocks/<symbol>')
def stock_chart(symbol):
    """Generate and return a stock price history chart."""
    chart_buffer = generate_stock_chart(symbol)
    if chart_buffer:
        return send_file(chart_buffer, mimetype='image/png')
    return jsonify({'error': 'Unable to generate stock chart'}), 500

@app.route('/charts/weather/<planet>')
def weather_chart(planet):
    """Generate and return a weather history chart."""
    chart_buffer = generate_weather_chart(planet)
    if chart_buffer:
        return send_file(chart_buffer, mimetype='image/png')
    return jsonify({'error': 'Unable to generate weather chart'}), 500

if __name__ == '__main__':
    app.run(debug=True) 