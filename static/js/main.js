// Function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Function to create an error message element
function createErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-warning';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
    `;
    return errorDiv;
}

// Function to update weather data
async function updateWeather() {
    try {
        const response = await fetch('/api/weather');
        const data = await response.json();
        
        const weatherContainer = document.getElementById('weather-container');
        weatherContainer.innerHTML = '';
        
        for (const [planet, weather] of Object.entries(data)) {
            const weatherCard = document.createElement('div');
            weatherCard.className = 'weather-card';
            
            let noteHtml = '';
            if (weather.note) {
                noteHtml = `<div class="alert alert-info mt-2">${weather.note}</div>`;
            }
            
            weatherCard.innerHTML = `
                <h3>${planet.charAt(0).toUpperCase() + planet.slice(1)}</h3>
                <div class="temperature">${weather.temperature}°C</div>
                <div>Condition: ${weather.condition}</div>
                <div>Humidity: ${weather.humidity}%</div>
                <div>Wind Speed: ${weather.wind_speed} km/h</div>
                <div class="refresh-time">Last updated: ${formatDate(weather.timestamp)}</div>
                ${noteHtml}
            `;
            weatherContainer.appendChild(weatherCard);
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
        const weatherContainer = document.getElementById('weather-container');
        weatherContainer.innerHTML = '';
        weatherContainer.appendChild(createErrorMessage('Unable to fetch weather data. Please try again later.'));
    }
}

// Function to update stock data
async function updateStocks() {
    try {
        const response = await fetch('/api/stocks');
        const data = await response.json();
        
        const stocksContainer = document.getElementById('stocks-container');
        stocksContainer.innerHTML = '';
        
        let hasValidData = false;
        
        for (const [symbol, stock] of Object.entries(data)) {
            if (stock.error) continue;
            
            hasValidData = true;
            const stockCard = document.createElement('div');
            stockCard.className = 'stock-card';
            const changeClass = stock.change >= 0 ? 'positive' : 'negative';
            const changeSymbol = stock.change >= 0 ? '+' : '';
            
            let noteHtml = '';
            if (stock.note) {
                noteHtml = `<div class="alert alert-info mt-2">${stock.note}</div>`;
            }
            
            stockCard.innerHTML = `
                <h3>${stock.name}</h3>
                <div class="stock-price">$${stock.current_price.toFixed(2)}</div>
                <div class="stock-change ${changeClass}">
                    ${changeSymbol}${stock.change.toFixed(2)}%
                </div>
                <div>Volume: ${stock.volume.toLocaleString()}</div>
                <div class="refresh-time">Last updated: ${formatDate(stock.timestamp)}</div>
                ${noteHtml}
            `;
            stocksContainer.appendChild(stockCard);
        }
        
        if (!hasValidData) {
            stocksContainer.appendChild(createErrorMessage('Unable to fetch stock data. Please try again later.'));
        }
    } catch (error) {
        console.error('Error fetching stock data:', error);
        const stocksContainer = document.getElementById('stocks-container');
        stocksContainer.innerHTML = '';
        stocksContainer.appendChild(createErrorMessage('Unable to fetch stock data. Please try again later.'));
    }
}

// Function to update news data
async function updateNews() {
    try {
        const response = await fetch('/api/news');
        const data = await response.json();
        
        const newsContainer = document.getElementById('news-container');
        newsContainer.innerHTML = '';
        
        if (data.error) {
            newsContainer.appendChild(createErrorMessage(data.error));
            return;
        }
        
        if (!data.articles || data.articles.length === 0) {
            newsContainer.appendChild(createErrorMessage('No news articles available.'));
            return;
        }
        
        let noteHtml = '';
        if (data.note) {
            noteHtml = `<div class="alert alert-info mb-3">${data.note}</div>`;
            newsContainer.innerHTML = noteHtml;
        }
        
        data.articles.forEach(article => {
            const newsCard = document.createElement('div');
            newsCard.className = 'news-card';
            newsCard.innerHTML = `
                <div class="news-title">${article.title}</div>
                <div class="news-source">${article.source.name}</div>
                <p>${article.description}</p>
                <a href="${article.url}" target="_blank" class="btn btn-primary btn-sm">Read More</a>
                <div class="refresh-time">Published: ${formatDate(article.publishedAt)}</div>
            `;
            newsContainer.appendChild(newsCard);
        });
    } catch (error) {
        console.error('Error fetching news data:', error);
        const newsContainer = document.getElementById('news-container');
        newsContainer.innerHTML = '';
        newsContainer.appendChild(createErrorMessage('Unable to fetch news data. Please try again later.'));
    }
}

// Update all data initially
updateWeather();
updateStocks();
updateNews();

// Update data every 5 minutes
setInterval(() => {
    updateWeather();
    updateStocks();
    updateNews();
}, 300000); 