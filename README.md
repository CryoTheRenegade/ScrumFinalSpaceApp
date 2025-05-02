# Space Corp Dashboard

A comprehensive dashboard for space exploration and research, providing real-time data visualization and monitoring capabilities.

## Features

- Real-time weather conditions display
- Space-related company stock prices
- Space exploration news feed
- Interactive data visualization
- Customizable dashboard layout

## Setup

1. Install Pipenv if you haven't already:
```bash
pip install pipenv
```

2. Install dependencies:
```bash
pipenv install
```

3. Create a `.env` file in the root directory with the following variables:
```
NEWS_API_KEY=your_news_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

To get an Alpha Vantage API key:
1. Go to https://www.alphavantage.co/support/#api-key
2. Fill out the form to get a free API key
3. Add the key to your `.env` file

4. Run the application:

On Windows:
```bash
pipenv run python app.py
```

On Unix/MacOS:
```bash
pipenv run python app.py
```

## Troubleshooting

If you encounter any issues:

1. Make sure you're in the correct directory
2. Try running `pipenv shell` first, then run `python app.py`
3. If you get permission errors, try running your terminal as administrator
4. If you see Node.js deprecation warnings, these are related to the IDE and can be safely ignored
5. If you don't have an Alpha Vantage API key, the application will use simulated stock data

## Project Structure

- `app.py`: Main Flask application
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `utils/`: Utility functions and API integrations
- `config.py`: Configuration settings

## Technologies Used

- Flask: Web framework
- Bootstrap: Frontend framework
- Chart.js: Data visualization
- NewsAPI: News feed integration
- Alpha Vantage: Stock data integration 