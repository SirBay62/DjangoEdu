from django.db import models
from django.urls import reverse_lazy, reverse

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    published_at= models.DateTimeField(null=True,blank=True,auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blogapp:article',kwargs={'pk':self.pk})
