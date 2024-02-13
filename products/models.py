from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, default="Chairs")
    image = models.ImageField(upload_to='category', default='category.png')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title
