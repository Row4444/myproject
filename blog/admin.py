from django.contrib import admin

# Register your models here.
from blog.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'author', 'post', 'date')
    list_filter = ('date', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
