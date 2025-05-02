import os
from datetime import datetime
import time
import random
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

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
                current_price = float(data['05. price'][0])
                change_percent = float(data['10. change percent'].replace('%', ''))
                volume = int(data['06. volume'])
                
                # Get company overview
                overview, _ = fd.get_company_overview(symbol=company)
                company_name = overview['Name'][0]
                
                stock_data[company] = {
                    'name': company_name,
                    'current_price': current_price,
                    'change': change_percent,
                    'volume': volume,
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