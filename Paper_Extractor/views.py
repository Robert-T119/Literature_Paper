from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import UploadedPDF
from .Hybrid_method import extract_doi_from_pdf_using_ocr, get_paper_info, extract_doi_from_pdf_text
from django.urls import reverse
import os
from django.conf import settings

def upload_pdf_view(request):
    all_pdfs = UploadedPDF.objects.all()  
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('pdf_file')
            for file in files:
                instance = UploadedPDF(pdf_file=file)
                instance.save()
            
            return redirect('Paper_Extractor:upload_pdf')
    else:
        form = PDFUploadForm()
    return render(request, 'Paper_Extractor/upload.html', {'form': form, 'all_pdfs': all_pdfs})

def delete_pdf_view(request, pdf_id):
    pdf_to_delete = UploadedPDF.objects.get(id=pdf_id)
    file_path = os.path.join(settings.MEDIA_ROOT, pdf_to_delete.pdf_file.name)
    
    # Delete the file from the filesystem
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete the database record
    pdf_to_delete.delete()
    
    return redirect(reverse('Paper_Extractor:upload_pdf'))

def extract_dois_view(request):
    all_doi_results = []
    all_paper_info = []
    all_pdfs = UploadedPDF.objects.all()

    for pdf in all_pdfs:
        # Step 1: Extract DOI using the original text-based method
        primary_doi = extract_doi_from_pdf_text(pdf.pdf_file.path)
        
        # Step 2: Fetch details from OpenAlex
        if primary_doi:
            paper_details = get_paper_info(primary_doi)
            # If authors are not "N/A", we assume the fetched data is valid
            valid_data = paper_details[0] != "N/A"
        else:
            valid_data = False

        # Step 3: If OpenAlex returns N/A or no DOI was found in step 1, use the OCR-based method
        if not valid_data:
            extracted_dois = extract_doi_from_pdf_using_ocr(pdf.pdf_file.path)
            primary_doi = extracted_dois[0] if extracted_dois else None
            if primary_doi:
                paper_details = get_paper_info(primary_doi)

        if primary_doi:
            all_doi_results.append(primary_doi)
            all_paper_info.append({
                'doi': primary_doi,
                'title': paper_details[2],
                'authors': paper_details[0],
                'abstract': paper_details[4],
                'publication_date': paper_details[1],
                'concepts': paper_details[3],
                'referenced_works': paper_details[5],
                'related_works': paper_details[6]
            })

    return render(request, 'Paper_Extractor/upload.html', {'dois': all_doi_results, 'papers': all_paper_info, 'all_pdfs': all_pdfs})
