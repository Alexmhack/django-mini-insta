from django.db import models

class Feed(models.Model):
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='static/documents')
