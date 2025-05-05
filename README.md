# Space Corp Dashboard

A real-time dashboard displaying space-related data including weather conditions on Earth and Mars, space stock prices, and space news.

## Features

- **Real-time Weather Data**
  - Earth weather using OpenWeatherMap API
  - Mars weather using NASA's InSight API
  - Historical weather data for both planets
  - Interactive weather charts

- **Space Stock Information**
  - Real-time stock prices for space companies
  - Historical price data
  - Interactive stock charts

- **Space News**
  - Latest space-related news articles
  - Article summaries and links

- **Dynamic UI**
  - Reorderable dashboard cards
  - Responsive design
  - Dark theme optimized for space data visualization

## API Keys Required

The application requires the following API keys:

1. **NASA API Key**
   - Used for Mars weather data from the InSight mission
   - Get your free API key at: https://api.nasa.gov/
   - Add to `.env` file as: `NASA_API_KEY=your_key_here`

2. **OpenWeatherMap API Key**
   - Used for Earth weather data
   - Get your free API key at: https://openweathermap.org/api
   - Add to `.env` file as: `OPENWEATHER_API_KEY=your_key_here`

3. **Alpha Vantage API Key**
   - Used for stock market data
   - Get your free API key at: https://www.alphavantage.co/
   - Add to `.env` file as: `ALPHA_VANTAGE_API_KEY=your_key_here`

4. **News API Key**
   - Used for space news articles
   - Get your free API key at: https://newsapi.org/
   - Add to `.env` file as: `NEWS_API_KEY=your_key_here`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd space-corp-dashboard
```

2. Install Pipenv if you haven't already:
```bash
pip install pipenv
```

3. Install dependencies using Pipenv:
```bash
pipenv install
```

4. Create a `.env` file in the root directory and add your API keys:
```env
NASA_API_KEY=your_nasa_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_api_key
NEWS_API_KEY=your_news_api_key
```

5. Run the application:

On Windows:
```bash
pipenv run python app.py
```

On Unix/MacOS:
```bash
pipenv run python app.py
```

The dashboard will be available at `http://localhost:5000`

## Troubleshooting

If you encounter any issues:

1. Make sure you're in the correct directory
2. Try running `pipenv shell` first, then run `python app.py`
3. If you get permission errors, try running your terminal as administrator
4. If you see Node.js deprecation warnings, these are related to the IDE and can be safely ignored
5. If you don't have an API key, the application will use simulated data

## API Rate Limits

- **NASA API**: 1,000 requests per hour with a DEMO_KEY
- **OpenWeatherMap**: 60 calls/minute for free tier
- **Alpha Vantage**: 5 API calls per minute and 500 calls per day for free tier
- **News API**: 100 requests per day for free tier

The application includes fallback data generation when API limits are reached.

## Features in Detail

### Mars Weather Data
- Real-time temperature, wind speed, and atmospheric pressure
- Current sol (Martian day) information
- Historical data for the past 7 sols
- Data sourced from NASA's InSight mission

### Earth Weather Data
- Current temperature, conditions, humidity, and wind speed
- Historical data for the past 7 days
- Location-based weather information

### Stock Information
- Real-time stock prices for major space companies
- Price changes and trading volume
- Historical price charts
- Company information and news

### News Feed
- Latest space-related news articles
- Article summaries with source attribution
- Direct links to full articles
- Automatic updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 