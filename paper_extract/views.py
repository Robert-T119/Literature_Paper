from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .Hybrid_method import extract_doi_from_pdf_using_ocr

def upload_pdf_view(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file here
            uploaded_pdf = request.FILES['uploaded_pdf']
            extracted_dois = extract_doi_from_pdf_using_ocr(uploaded_pdf)

            # Here, you can use the extracted DOIs as needed, or even pass them to the template.
            # For the sake of demonstration, we're redirecting to the same page.
            return redirect('upload_pdf')
    else:
        form = PDFUploadForm()

    return render(request, 'paper_extract/upload.html', {'form': form})
