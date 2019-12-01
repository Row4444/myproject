from django.db import models

from account.models import User
from mymainproj import settings

from ckeditor_uploader.fields import RichTextUploadingField


class BlogManager(models.Manager):
    def get_queryset(self):
        return super(BlogManager, self).get_queryset().filter(status='approve')


class Post(models.Model):
    STATUS_CHOICES = (
        ('unview', 'Unview'),
        ('approve', 'Approve'),
        ('decline', 'Decline')
    )

    title = models.CharField(max_length=140, unique=True)
    body = RichTextUploadingField(config_name='blog_editor')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='unview',

    )

    objects = models.Manager()  # default
    approved = BlogManager()  # custom manager  filter by 'approve'

    def get_url(self):
        return self.id

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return '{} : {}'.format(self.author.username, self.body)

