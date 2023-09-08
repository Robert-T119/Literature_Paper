from django.shortcuts import render
from .Data_Fetching import extract_papers_from_openalex_search, generate_date_ranges
from .Text_Processing import clean_text, lowercase_text, tokenize_text, remove_stopwords, lemmatize_tokens, is_relevant, run_prediction, get_embedding
from .Constants import concept_list
import pandas as pd
from openai.embeddings_utils import cosine_similarity
from django.http import FileResponse,HttpResponse
from django.conf import settings
import os

def paper_finder_view(request):
    papers_to_send = []  # Initialize here

    if request.method == "POST":
        selected_urls = request.POST.getlist('concepts')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        target_embedding_word = request.POST.get('target_embedding_word')


        # Fetching papers
        papers = []
        for concept_id in selected_urls:
            for date in generate_date_ranges(start_date, end_date):
                search_url = f'https://api.openalex.org/works?filter=concept.id:{concept_id},from_publication_date:{date},to_publication_date:{date}'
                papers_for_date = extract_papers_from_openalex_search(search_url, 1000, date)  # Limit of 1000 as an example
                papers.extend(papers_for_date)

        # Pre-process the papers
        df = pd.DataFrame(papers, columns=["DOI", "Title", "Authors", "Publication Date", "Abstract", "Concepts"])
        df['Cleaned Abstract'] = df['Abstract'].apply(clean_text).apply(lowercase_text)
        df['Tokens'] = df['Cleaned Abstract'].apply(tokenize_text).apply(remove_stopwords).apply(lemmatize_tokens)
        df['Is Relevant'] = df['Cleaned Abstract'].apply(is_relevant)
        
        # Filter Relevant Papers
        sofc_relevant_papers = df[df['Is Relevant']]

        # OpenAI Processing
        separator = "\n\n###\n\n"
        sofc_model_name = "ada:ft-personal-2023-07-29-19-02-14"
        sofc_predictions = run_prediction(sofc_model_name, sofc_relevant_papers['Cleaned Abstract'] + separator)
        sofc_relevant_papers['SOFC Predictions'] = sofc_predictions

        sofc_positive_papers = sofc_relevant_papers[sofc_relevant_papers['SOFC Predictions'] == 'positive']
        sofc_materials_model_name = "ada:ft-personal-2023-07-27-12-26-20"
        sofc_materials_predictions = run_prediction(sofc_materials_model_name, sofc_positive_papers['Cleaned Abstract'] + separator)
        sofc_positive_papers['SOFC Materials Predictions'] = sofc_materials_predictions

        # Text Embeddings and Similarity Score
        target_embedding = get_embedding(target_embedding_word)
        sofc_positive_papers['embedding'] = sofc_positive_papers['Abstract'].apply(get_embedding)
        sofc_positive_papers['similarity_score'] = sofc_positive_papers['embedding'].apply(lambda x: cosine_similarity(x, target_embedding))
        sofc_positive_papers = sofc_positive_papers.sort_values('similarity_score', ascending=False)

        # Save Results to Excel
        export_columns = ["DOI", "Title", "Authors", "Publication Date", "Abstract", "SOFC Predictions", "SOFC Materials Predictions", "similarity_score"]
        sofc_positive_papers_export = sofc_positive_papers[export_columns]
        sofc_positive_papers_export.to_excel('media/output.xlsx', index=False)

        papers_to_send = sofc_positive_papers.to_dict(orient='records')

        for paper in papers_to_send:
            paper['SOFC_Predictions'] = paper.pop('SOFC Predictions')
            paper['SOFC_Materials_Predictions'] = paper.pop('SOFC Materials Predictions')

        return render(request, 'Paper_Finder/finder_form.html', {'papers': papers_to_send, 'concept_list': concept_list})
    else:
        return render(request, 'Paper_Finder/finder_form.html', {'concept_list': concept_list})

def download_output_xlsx(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'output.xlsx')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
        return response
    else:
        return HttpResponse('File not found.', content_type='text/plain')