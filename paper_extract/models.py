from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploaded_pdfs/')
    upload_time = models.DateTimeField(auto_now_add=True)
