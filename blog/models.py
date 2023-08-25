from django.db import models
from django.conf import settings
from django.utils import timezone
from autoslug import AutoSlugField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    image = models.ImageField(upload_to='cat')
    slug = AutoSlugField(populate_from='name', unique=True, default=None, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    image = models.ImageField(upload_to='cat')

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    text = models.TextField()
    feature_img = models.ImageField(upload_to='post/feture',blank=True, null=True)
    thumbnail_img = models.ImageField(upload_to='post/thumbnail',blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, default=None, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date',]

