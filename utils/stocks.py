import os
from datetime import datetime, timedelta
import time
import random
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

def get_historical_stock_data(symbol, days=30):
    """Fetch historical stock data for the specified number of days"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        return get_simulated_historical_data(symbol, days)
    
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        # Get daily data
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        
        # Convert to list of daily data points
        historical_data = []
        for date, row in data.iterrows():
            historical_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': float(row['1. open']),
                'high': float(row['2. high']),
                'low': float(row['3. low']),
                'close': float(row['4. close']),
                'volume': int(row['5. volume'])
            })
        
        # Return only the requested number of days
        return historical_data[-days:]
        
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {str(e)}")
        return get_simulated_historical_data(symbol, days)

def get_simulated_historical_data(symbol, days):
    """Generate simulated historical stock data"""
    base_price = {
        'SPCE': 1.50,
        'BA': 180.00,
        'LMT': 450.00,
        'NOC': 420.00,
        'RTX': 90.00
    }.get(symbol, 100.00)
    
    historical_data = []
    current_price = base_price
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i-1)).strftime('%Y-%m-%d')
        daily_change = random.uniform(-0.02, 0.02)
        current_price *= (1 + daily_change)
        
        historical_data.append({
            'date': date,
            'open': round(current_price * (1 + random.uniform(-0.01, 0.01)), 2),
            'high': round(current_price * (1 + random.uniform(0, 0.02)), 2),
            'low': round(current_price * (1 - random.uniform(0, 0.02)), 2),
            'close': round(current_price, 2),
            'volume': int(random.uniform(500000, 5000000))
        })
    
    return historical_data

def get_stock_data():
    # List of space-related companies
    companies = ['SPCE', 'BA', 'LMT', 'NOC', 'RTX']
    stock_data = {}
    
    # Fallback data in case of connection issues
    fallback_data = {
        'SPCE': {'name': 'Virgin Galactic', 'current_price': 1.50, 'change': -2.5, 'volume': 1000000},
        'BA': {'name': 'Boeing', 'current_price': 180.00, 'change': 1.2, 'volume': 5000000},
        'LMT': {'name': 'Lockheed Martin', 'current_price': 450.00, 'change': 0.8, 'volume': 2000000},
        'NOC': {'name': 'Northrop Grumman', 'current_price': 420.00, 'change': -0.5, 'volume': 1500000},
        'RTX': {'name': 'Raytheon Technologies', 'current_price': 90.00, 'change': 1.5, 'volume': 3000000}
    }
    
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("Alpha Vantage API key not found. Using simulated data.")
        return get_simulated_data(companies, fallback_data)
    
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        fd = FundamentalData(key=api_key, output_format='pandas')
        
        for company in companies:
            try:
                # Get real-time quote
                data, meta_data = ts.get_quote_endpoint(symbol=company)
                
                # Use iloc for position-based access and handle percentage conversion properly
                current_price = float(data['05. price'].iloc[0])
                change_percent_str = data['10. change percent'].iloc[0]
                change_percent = float(change_percent_str.strip('%'))
                volume = int(data['06. volume'].iloc[0])
                
                # Get company overview
                overview, _ = fd.get_company_overview(symbol=company)
                company_name = overview['Name'].iloc[0]
                
                # Get historical data
                historical_data = get_historical_stock_data(company)
                
                stock_data[company] = {
                    'name': company_name,
                    'current_price': current_price,
                    'change': change_percent,
                    'volume': volume,
                    'historical_data': historical_data,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add a small delay to avoid hitting API rate limits
                time.sleep(0.2)
                
            except Exception as e:
                print(f"Error fetching data for {company}: {str(e)}")
                stock_data[company] = {
                    'name': fallback_data[company]['name'],
                    'current_price': fallback_data[company]['current_price'],
                    'change': fallback_data[company]['change'],
                    'volume': fallback_data[company]['volume'],
                    'historical_data': get_simulated_historical_data(company, 30),
                    'timestamp': datetime.now().isoformat(),
                    'note': 'Using fallback data due to API issues'
                }
                
    except Exception as e:
        print(f"Error initializing Alpha Vantage: {str(e)}")
        return get_simulated_data(companies, fallback_data)
    
    return stock_data

def get_simulated_data(companies, fallback_data):
    """Generate simulated stock data when API is unavailable"""
    stock_data = {}
    for company in companies:
        try:
            base_price = fallback_data[company]['current_price']
            price_change = random.uniform(-0.02, 0.02)
            new_price = base_price * (1 + price_change)
            
            base_volume = fallback_data[company]['volume']
            volume_change = random.uniform(-0.1, 0.1)
            new_volume = int(base_volume * (1 + volume_change))
            
            stock_data[company] = {
                'name': fallback_data[company]['name'],
                'current_price': round(new_price, 2),
                'change': round(price_change * 100, 2),
                'volume': new_volume,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using simulated data due to API issues'
            }
        except Exception as e:
            print(f"Error generating data for {company}: {str(e)}")
            stock_data[company] = {
                'name': fallback_data[company]['name'],
                'current_price': fallback_data[company]['current_price'],
                'change': fallback_data[company]['change'],
                'volume': fallback_data[company]['volume'],
                'timestamp': datetime.now().isoformat(),
                'note': 'Using fallback data'
            }
    return stock_data 