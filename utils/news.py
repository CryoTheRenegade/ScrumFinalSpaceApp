import os
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def get_space_news():
    api_key = os.getenv('NEWS_API_KEY')
    
    # Fallback news articles
    fallback_articles = [
        {
            'title': 'NASA Announces New Mars Mission',
            'description': 'NASA reveals plans for a new Mars exploration mission scheduled for 2026.',
            'url': 'https://www.nasa.gov',
            'source': {'name': 'NASA'},
            'publishedAt': datetime.now().isoformat()
        },
        {
            'title': 'SpaceX Successfully Launches Starlink Mission',
            'description': 'SpaceX completes another successful Starlink satellite deployment.',
            'url': 'https://www.spacex.com',
            'source': {'name': 'SpaceX'},
            'publishedAt': datetime.now().isoformat()
        },
        {
            'title': 'Blue Origin Tests New Rocket Engine',
            'description': 'Blue Origin conducts successful test of their new BE-4 rocket engine.',
            'url': 'https://www.blueorigin.com',
            'source': {'name': 'Blue Origin'},
            'publishedAt': datetime.now().isoformat()
        }
    ]
    
    if not api_key:
        return {
            'articles': fallback_articles,
            'timestamp': datetime.now().isoformat(),
            'note': 'Using fallback data - News API key not configured'
        }
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Get news from the last 24 hours
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Search for space-related news
        response = newsapi.get_everything(
            q='space exploration OR NASA OR SpaceX OR Blue Origin',
            from_param=from_date,
            language='en',
            sort_by='relevancy'
        )
        
        if response.get('status') == 'ok' and response.get('articles'):
            return {
                'articles': response['articles'][:5],  # Return top 5 articles
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'articles': fallback_articles,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using fallback data - No articles found'
            }
            
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return {
            'articles': fallback_articles,
            'timestamp': datetime.now().isoformat(),
            'note': 'Using fallback data due to connection issues'
        } 