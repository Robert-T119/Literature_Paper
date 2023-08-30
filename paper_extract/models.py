from django.db import models
import os

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploaded_pdfs/')
    upload_time = models.DateTimeField(auto_now_add=True)
    @property
    def file_name(self):
        return os.path.basename(self.pdf_file.name)
