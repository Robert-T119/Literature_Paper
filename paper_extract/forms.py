from django import forms

class PDFUploadForm(forms.Form):
    uploaded_pdf = forms.FileField()
