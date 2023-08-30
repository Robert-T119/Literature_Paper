from django import forms
from .models import UploadedPDF

class PDFUploadForm(forms.ModelForm):
    pdf_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="Upload PDFs")

    class Meta:
        model = UploadedPDF
        fields = ['pdf_file']

