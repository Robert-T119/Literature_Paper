from django.shortcuts import render
from .Data_Fetching import fetch_data  # Assuming fetch_data is the function to fetch papers
from .Constants import concept_list

def paper_finder_view(request):
    results = []  # Placeholder for the results
    
    if request.method == "POST":
        selected_urls = request.POST.getlist('concepts')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        results = fetch_data(selected_urls, start_date, end_date)  # Fetch papers using the provided function

    return render(request, 'literature_finder/finder_form.html', {'results': results, 'concept_list': concept_list})
