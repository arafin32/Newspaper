from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify # For username if needed, or just use simple ones
import time # For checking updated_at changes

from .models import Article, Comment

# Helper function to create a user if not using setUpTestData for all users
def create_user(username="testuser", password="password"):
    return User.objects.create_user(username=username, password=password)

class ArticleModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user that can be used by tests in this class or other classes
        cls.test_user = User.objects.create_user(username="testauthor", password="testpassword")

    def test_article_creation_with_author(self):
        """Test that an Article can be created with an author and timestamps are set."""
        now = timezone.now()
        article = Article.objects.create(
            title="Test Article Title",
            content="Test article content.",
            publish_date=now.date(),
            author=self.test_user
        )
        self.assertEqual(article.author, self.test_user)
        self.assertEqual(article.title, "Test Article Title")
        self.assertIsNotNone(article.created_at)
        self.assertIsNotNone(article.updated_at)
        self.assertTrue(article.created_at >= now) # Should be around now
        self.assertTrue(article.updated_at >= now) # Should be around now
        self.assertEqual(article.created_at, article.updated_at) # Initially should be same

    def test_article_updated_at_changes(self):
        """Test that updated_at timestamp changes when an article is updated."""
        article = Article.objects.create(
            title="Original Title",
            content="Original content.",
            publish_date=timezone.now().date(),
            author=self.test_user
        )
        original_created_at = article.created_at
        original_updated_at = article.updated_at

        # Ensure there's a slight delay for timestamp comparison to be meaningful
        time.sleep(0.01)

        article.content = "Updated content."
        article.save()
        article.refresh_from_db() # Reload from DB to get the new updated_at set by auto_now

        self.assertEqual(article.created_at, original_created_at) # created_at should not change
        self.assertTrue(article.updated_at > original_updated_at)


class HomeViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="hometestuser", password="password")

    def _create_article(self, title="Test Article", days_offset=0, author=None):
        """Helper to create an article."""
        if author is None:
            author = self.user
        return Article.objects.create(
            title=title,
            content="Some content for " + title,
            publish_date=timezone.now().date() - timezone.timedelta(days=days_offset),
            author=author
        )

    def test_home_view_status_code_and_content_with_articles(self):
        """Test home view with articles."""
        article1 = self._create_article(title="Article Alpha", days_offset=1)
        article2 = self._create_article(title="Article Beta", days_offset=0)

        response = self.client.get(reverse('articles:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article1.title)
        self.assertContains(response, article2.title)
        # The view orders by "-id", so Beta (created later) should appear before Alpha if IDs are sequential
        # self.assertTrue(response.content.decode().find(article2.title) < response.content.decode().find(article1.title))

    def test_home_view_no_articles(self):
        """Test home view when no articles exist."""
        response = self.client.get(reverse('articles:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles found.")


class ArticleDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="detailtestuser", password="password")
        cls.article = Article.objects.create(
            title="Detailed Test Article",
            content="Content for detailed view.",
            publish_date=timezone.now().date(),
            author=cls.user
        )
        cls.commenter = User.objects.create_user(username="commenter", password="password")
        cls.comment1 = Comment.objects.create(
            articles=cls.article,
            user=cls.commenter,
            content="This is the first comment."
        )
        cls.comment2 = Comment.objects.create(
            articles=cls.article,
            user=cls.user, # Article author can also comment
            content="This is the second comment by the author."
        )

    def test_article_detail_view_status_and_content(self):
        """Test article detail view displays article and its comments."""
        url = reverse('articles:article_detail', args=[self.article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.article.content)
        self.assertContains(response, self.article.author.username)
        self.assertContains(response, self.comment1.content)
        self.assertContains(response, self.comment1.user.username)
        self.assertContains(response, self.comment2.content)
        self.assertContains(response, self.comment2.user.username)

    def test_article_detail_view_404_not_found(self):
        """Test article detail view returns 404 for a non-existent article ID."""
        non_existent_id = self.article.id + 999
        url = reverse('articles:article_detail', args=[non_existent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AddCommentViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User to perform the commenting
        cls.commenting_user = User.objects.create_user(username="commentinguser", password="password123")
        # Another user to be the author of the article
        cls.article_author = User.objects.create_user(username="articleauthor", password="password123")

    def setUp(self):
        # Create a fresh article for each test method
        self.article = Article.objects.create(
            title="Article for Commenting",
            content="This article will be commented on.",
            publish_date=timezone.now().date(),
            author=self.article_author
        )

    def test_add_comment_authenticated_user_success(self):
        """Test an authenticated user can successfully post a comment."""
        self.client.login(username="commentinguser", password="password123")
        comment_content = "This is a test comment."
        url = reverse('articles:add_comment', args=[self.article.id])

        response = self.client.post(url, {'content': comment_content})

        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertRedirects(response, reverse('articles:article_detail', args=[self.article.id]))

        self.assertTrue(Comment.objects.filter(articles=self.article, content=comment_content, user=self.commenting_user).exists())
        self.assertEqual(Comment.objects.count(), 1)


    def test_add_comment_authenticated_user_empty_comment(self):
        """Test posting an empty comment by an authenticated user."""
        self.client.login(username="commentinguser", password="password123")
        url = reverse('articles:add_comment', args=[self.article.id])

        response = self.client.post(url, {'content': ''}) # Empty content

        self.assertEqual(response.status_code, 302) # View redirects if content is empty
        self.assertRedirects(response, reverse('articles:article_detail', args=[self.article.id]))
        self.assertFalse(Comment.objects.filter(articles=self.article, user=self.commenting_user).exists()) # No comment should be created
        self.assertEqual(Comment.objects.count(), 0)


    def test_add_comment_unauthenticated_user_redirects_to_login(self):
        """Test an unauthenticated user is redirected to login page when trying to comment."""
        # Ensure client is logged out (default state for a new client, but explicit is good)
        self.client.logout()

        comment_content = "Unauthenticated comment attempt."
        url = reverse('articles:add_comment', args=[self.article.id])

        response = self.client.post(url, {'content': comment_content})

        self.assertEqual(response.status_code, 302) # Should redirect to login

        # Construct the expected login URL with a 'next' parameter
        # The add_comment_view is decorated with @login_required, which will set the 'next'
        expected_login_url = f"{reverse('login')}?next={url}"
        self.assertRedirects(response, expected_login_url)

        self.assertFalse(Comment.objects.filter(articles=self.article, content=comment_content).exists())
        self.assertEqual(Comment.objects.count(), 0)
