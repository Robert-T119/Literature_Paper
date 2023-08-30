from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import UploadedPDF
from .Hybrid_method import extract_doi_from_pdf_using_ocr

def upload_pdf_view(request):
    all_doi_results = []
    all_pdfs = UploadedPDF.objects.all()  
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('pdf_file')
            for file in files:
                instance = UploadedPDF(pdf_file=file)
                instance.save()
                
                # Extract DOIs from the uploaded PDF
                extracted_dois = extract_doi_from_pdf_using_ocr(instance.pdf_file.path)
                all_doi_results.extend(extracted_dois)
            
            # Pass the extracted DOIs to the template
            return render(request, 'paper_extract/upload.html', {'form': form, 'dois': all_doi_results})
    else:
        form = PDFUploadForm()
    return render(request, 'paper_extract/upload.html', {'form': form, 'all_pdfs': all_pdfs})

