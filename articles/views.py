from django.shortcuts import render

# Create your views here.
from .models import Article


def home_view(request):
    """
    Renders the homepage with the 5 most recent blog posts.
    """
    articles = Article.objects.order_by("-id")[:5]
    return render(request, "home.html", {"articles": articles})
