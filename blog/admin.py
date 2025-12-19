from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_ = ('title', 'author', 'is_published', 'created_at')
    list_D = ('is_published', 'created_at', 'author')
    body = ('title', 'body')
    act = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        queryset.update(is_published=True)
    publish_posts.short_description = "Publish Post"

    def unpublish_posts(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_posts.short_description = "Remove Post"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_ = ('post', 'author', 'is_approved', 'created_at')
    list_D = ('is_approved', 'created_at', 'author')
    body = ('body',)

