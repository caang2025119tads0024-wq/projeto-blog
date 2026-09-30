from django.db import models

# Create your models here.

class Post(models.Model):
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()

    def _str_(self):
        return self.titulo