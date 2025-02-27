import requests
from django.shortcuts import render

def fetch_news(query, api_key):
    """
    Fetches news articles based on the query from the NewsData.io API.
    """
    url = "https://newsdata.io/api/1/news"
    params = {'apikey': api_key, 'q': query, 'language': 'en'}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        news_data = response.json()
        if 'results' in news_data:
            articles = news_data['results']
            return articles if articles else "No articles found."
        else:
            return "Error: Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"

def news_view(request):
    """
    Django view to display news articles related to a query.
    """
    api_key = 'pub_57142e2647bbf9af9ca85c949453359ff24de'  # ⚠️ Apna API key use kar!
    query = request.GET.get('query', 'technology')  # Default query 'technology'
    
    news_articles = fetch_news(query, api_key)

    if isinstance(news_articles, str):
        context = {'error': news_articles}
    else:
        context = {'articles': news_articles, 'query': query}

    return render(request, 'news_app/index.html', context)
