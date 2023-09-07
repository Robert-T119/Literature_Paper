from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

def paper_search_view(request):
    results = []
    direct_page = request.GET.get('direct_page', None)
    page_number = int(direct_page) if direct_page else int(request.GET.get('page', 1))
    papers_per_page = 10
    cursor = request.GET.get('cursor', None)
    sort_by = request.GET.get('sort_by', 'publication_date')  # default is sorting by publication date
    search_field = request.GET.get('search_field', 'title')  # default is searching by title
    search_query = request.GET.get('title_search', '')  # always get from the GET request
    
    if search_query:  # we're checking if search query is provided
        if int(page_number) <= 400:
            api_url = f"https://api.openalex.org/works?filter={search_field}.search:{search_query}&sort={sort_by}&per_page={papers_per_page}&page={page_number}"
        else:
            if not cursor:
                api_url = f"https://api.openalex.org/works?filter={search_field}.search:{search_query}&sort={sort_by}&per_page={papers_per_page}&cursor=*"
            else:
                api_url = f"https://api.openalex.org/works?filter={search_field}.search:{search_query}&sort={sort_by}&per_page={papers_per_page}&cursor={cursor}"
        
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            api_results = data.get('results', [])
            
            for paper in api_results:
                title = paper.get('title')
                doi = paper.get('doi')
                publication_date = paper.get('publication_date')
                authors = [authorship['author']['display_name'] for authorship in paper.get('authorships', [])]
                abstract_inverted = paper.get('abstract_inverted_index', {})
                if abstract_inverted:
                    abstract = ' '.join([word for word, pos in sorted([(word, positions[0]) for word, positions in abstract_inverted.items()], key=lambda x: x[1])])
                else:
                    abstract = "N/A"
                results.append({
                    'title': title,
                    'doi': doi,
                    'publication_date': publication_date,
                    'authors': authors,
                    'abstract': abstract
                })
            
            total_papers = data.get('meta', {}).get('count', 0)
            total_pages = -(-total_papers // papers_per_page)
            paginator = Paginator(range(total_pages), 1)
        else:
            paginator = Paginator([], 1)
    else:
        paginator = Paginator([], 1)

    try:
        page_results = paginator.page(page_number)
    except PageNotAnInteger:
        page_results = paginator.page(1)
    except EmptyPage:
        page_results = paginator.page(paginator.num_pages)
    
    return render(request, 'Paper_Search/search_page.html', {'results': results, 'page_results': page_results, 'search_query': search_query})
