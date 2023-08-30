from django.db import models

class UploadedPDF(models.Model):
    file_name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
