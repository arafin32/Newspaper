from django.contrib import admin

# Register your models here.
from articles.models import Articles, Comment


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "publish_date")


admin.site.register(Articles, ArticlesAdmin)




class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "articles")


admin.site.register(Comment, CommentAdmin)