from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import UploadedPDF
from .Hybrid_method import extract_doi_from_pdf_using_ocr, get_paper_info, extract_doi_from_pdf_text
from django.urls import reverse
import os
from django.conf import settings
import pandas as pd
from django.http import HttpResponse
import io

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
    if os.path.exists(file_path):
        os.remove(file_path)
    pdf_to_delete.delete()
    return redirect(reverse('Paper_Extractor:upload_pdf'))

def display_upload_page(request):
    all_pdfs = UploadedPDF.objects.all()
    return render(request, 'Paper_Extractor/upload.html', {'all_pdfs': all_pdfs})

def process_and_display_results(request):
    all_doi_results = []
    all_paper_info = []
    all_pdfs = UploadedPDF.objects.all()
    for pdf in all_pdfs:
        if not os.path.exists(pdf.pdf_file.path):
            continue
        primary_doi = extract_doi_from_pdf_text(pdf.pdf_file.path)
        if primary_doi:
            paper_details = get_paper_info(primary_doi)
            valid_data = paper_details[0] != "N/A"
        else:
            valid_data = False
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

def download_excel(request):
    all_paper_info = []
    all_pdfs = UploadedPDF.objects.all()
    for pdf in all_pdfs:
        if not os.path.exists(pdf.pdf_file.path):
            continue
        primary_doi = extract_doi_from_pdf_text(pdf.pdf_file.path)
        if primary_doi:
            paper_details = get_paper_info(primary_doi)
            valid_data = paper_details[0] != "N/A"
        else:
            valid_data = False
        if not valid_data:
            extracted_dois = extract_doi_from_pdf_using_ocr(pdf.pdf_file.path)
            primary_doi = extracted_dois[0] if extracted_dois else None
            if primary_doi:
                paper_details = get_paper_info(primary_doi)
        if primary_doi:
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
    df = pd.DataFrame(all_paper_info)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="extracted_papers.xlsx"'
    return response
