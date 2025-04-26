from django.db import models

# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    publish_date = models.DateField()

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User


class Comment(models.Model):
    content = models.TextField()
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)