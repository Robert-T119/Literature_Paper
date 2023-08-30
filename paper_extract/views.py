from django.shortcuts import render
from paper_extract.Hybrid_method import process_uploaded_pdf

def upload_and_extract_view(request):
    context = {}
    if request.method == "POST" and request.FILES['uploaded_pdf']:
        uploaded_pdf = request.FILES['uploaded_pdf']
        
        # Use the modified function to process the uploaded PDF
        paper_info = process_uploaded_pdf(uploaded_pdf)
        
        doi, authors, publication_date, title, concepts, abstract, referenced_works, related_works = paper_info

        # Add the extracted information to the context
        context.update({
            'doi': doi,
            'authors': authors,
            'publication_date': publication_date,
            'title': title,
            'concepts': concepts,
            'abstract': abstract,
            'referenced_works': referenced_works,
            'related_works': related_works,
        })

    return render(request, 'paper_extract/upload.html', context)
