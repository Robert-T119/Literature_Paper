from django.shortcuts import render
from .Data_Fetching import extract_papers_from_openalex_search, generate_date_ranges
from .Text_Processing import clean_text  # Assuming you have a clean_text function or similar
from .Constants import concept_list

def paper_finder_view(request):
    results = []
    
    if request.method == "POST":
        selected_urls = request.POST.getlist('concepts')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Fetching papers based on selected concepts and date range
        all_papers = []
        for concept_id in selected_urls:
            for date in generate_date_ranges(start_date, end_date):
                search_url = f'https://api.openalex.org/works?filter=concept.id:{concept_id},from_publication_date:{date},to_publication_date:{date}'
                papers_for_date = extract_papers_from_openalex_search(search_url, 1000, date)  # Limit of 1000 as an example
                all_papers.extend(papers_for_date)

        
        # Processing the fetched papers (adapt as needed)
        processed_papers = [clean_text(paper) for paper in papers]
        
        results = processed_papers

    return render(request, 'literature_finder/finder_form.html', {'results': results, 'concept_list': concept_list})
