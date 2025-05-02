from flask import Flask, render_template, jsonify
from utils.weather import get_weather_data
from utils.stocks import get_stock_data
from utils.news import get_space_news
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def weather():
    weather_data = get_weather_data()
    return jsonify(weather_data)

@app.route('/api/stocks')
def stocks():
    stock_data = get_stock_data()
    return jsonify(stock_data)

@app.route('/api/news')
def news():
    news_data = get_space_news()
    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True) 