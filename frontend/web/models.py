from django.db import models

class DocxFile(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255) 
    file = models.FileField(upload_to='docx_files/')
    
    def __str__(self):
        return self.name
