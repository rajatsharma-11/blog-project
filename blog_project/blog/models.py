from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (('draft', 'DRAFT'), ('published', 'PUBLISHED'))
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=264, unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=None)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.published.year, self.published.strftime('%m'),
                                            self.published.strftime('%d'), self.slug])


# MOdel Related To Comments Section

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Commented By {} on {}'.format(self.name, self.post)
