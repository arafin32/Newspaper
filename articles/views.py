from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Article, Comment


def home_view(request):
    """
    Renders the homepage with the 5 most recent blog posts.
    """
    articles = Article.objects.order_by("-id")[:5]
    return render(request, "home.html", {"articles": articles})


def article_detail_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.filter(articles=article).order_by('-id') # Assuming 'articles' is the ForeignKey name in Comment model
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, "article_detail.html", context)


@login_required
def add_comment_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content: # Basic validation
            Comment.objects.create(
                content=content,
                articles=article, # Assuming 'articles' is the correct related name
                user=request.user
            )
            return redirect('articles:article_detail', article_id=article.id)
        else:
            # Optionally, add a message about empty comment
            # For now, just redirect back or render the detail page with an error
            # comments = Comment.objects.filter(articles=article).order_by('-id')
            # context = {
            #     'article': article,
            #     'comments': comments,
            #     'comment_error': 'Comment cannot be empty.'
            # }
            # return render(request, "article_detail.html", context)
            return redirect('articles:article_detail', article_id=article.id) # Simpler: just redirect
    else:
        # If not POST, redirect to article detail page
        return redirect('articles:article_detail', article_id=article.id)
