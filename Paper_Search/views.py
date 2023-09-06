from django.shortcuts import render
import requests
from django.core.paginator import Paginator

def search_papers(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', 1)
    results = []

    if query:
        api_url = f"https://api.openalex.org/works?filter=title.search:{query}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', [])

    # Use Django's paginator
    paginator = Paginator(results, 10)
    current_page_results = paginator.get_page(page)

    return render(request, 'Paper_Search/search_results.html', {
        'query': query,
        'results': current_page_results,
    })
