from django.db import models
from django.conf import settings
from django.utils import timezone
from autoslug import AutoSlugField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


SEX_CHOICES = (
    ('F', 'Female',),
    ('M', 'Male',),
    ('U', 'Unsure',),
)
RULE_CHOICES = (
    ('A', 'Author',),
    ('R', 'Reader',),
)
# Create your models here.

class User(AbstractUser):
    phone_no = models.CharField(max_length = 10, null=True,blank=True)
    gender = models.CharField(max_length=1,choices=SEX_CHOICES,)
    date_of_birth = models.DateField(null=True)
    company = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    user_img = models.ImageField(upload_to='user_img', blank=True, null=True)
    user_web =  models.URLField(max_length=250,null=True,blank=True)
    user_address = models.CharField(max_length=300) 
    rule = models.CharField(max_length=1,choices=RULE_CHOICES, null=True,blank=True)

    def __str__(self):
        return self.username

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',null=True)
    name = models.CharField(max_length=80)
    commenter_email = models.EmailField(max_length=200, blank=True)
    comment_content = models.TextField()
    commented_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('commented_date',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)