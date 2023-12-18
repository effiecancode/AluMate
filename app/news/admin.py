from django.contrib import admin

from app.news.models import (
    Comment,
    Like,
    Post,
)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "posted_by",
        "status",
        "created_at",
        "likes_count",
        "comments_count",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "posted_by",
        "status",
        "created_at",
        "likes_count",
        "comments_count",
    )
    readonly_fields = ("likes_count", "comments_count")


class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "liked_by", "created_at")
    list_filter = ("post", "liked_by", "created_at")
    search_fields = ("post", "liked_by", "created_at")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "text", "created_at")
    list_filter = ("post", "author", "created_at")
    search_fields = ("post", "author", "created_at")


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
