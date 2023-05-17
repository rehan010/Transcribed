from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    audio_file = models.FileField(upload_to='audio')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    audio_text= models.TextField(default="")