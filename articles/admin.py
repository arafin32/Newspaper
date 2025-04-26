from django.contrib import admin

# Register your models here.
from articles.models import Article, Comment


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "publish_date")


admin.site.register(Article, ArticlesAdmin)




class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "articles")


admin.site.register(Comment, CommentAdmin)
