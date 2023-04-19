from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        app_label = "core"

    def __str__(self):
        return self.title