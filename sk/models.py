from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100, default=" ")
    
    def __str__(self):
        return self.title