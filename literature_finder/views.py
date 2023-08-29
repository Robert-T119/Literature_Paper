from django.shortcuts import render
from .Data_Fetching import extract_papers_from_openalex_search, generate_date_ranges
from .Text_Processing import clean_text, lowercase_text, tokenize_text, remove_stopwords, lemmatize_tokens, is_relevant
from .Constants import concept_list

def paper_finder_view(request):
    relevant_papers = []
    
    if request.method == "POST":
        selected_urls = request.POST.getlist('concepts')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Fetching papers based on selected concepts and date range
        papers = []
        for concept_id in selected_urls:
            for date in generate_date_ranges(start_date, end_date):
                search_url = f'https://api.openalex.org/works?filter=concept.id:{concept_id},from_publication_date:{date},to_publication_date:{date}'
                papers_for_date = extract_papers_from_openalex_search(search_url, 1000, date)  # Limit of 1000 as an example
                papers.extend(papers_for_date)

        for paper in papers:
            cleaned_abstract = clean_text(paper['Abstract'])
            lowered_abstract = lowercase_text(cleaned_abstract)
            tokenized_abstract = tokenize_text(lowered_abstract)
            non_stopwords_abstract = remove_stopwords(tokenized_abstract)
            lemmatized_abstract = lemmatize_tokens(non_stopwords_abstract)
            paper['Processed Abstract'] = lemmatized_abstract
            
        relevant_papers = [paper for paper in papers if is_relevant(paper['Processed Abstract'])]

    return render(request, 'literature_finder/finder_form.html', {'papers': relevant_papers})