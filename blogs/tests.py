from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.models import BlogPost
from comments.models import Comment

User = get_user_model()

class CommentCreateViewTest(TestCase):
    def setUp(self):
        # Create test user and blog post
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            status='published',
            published_at='2024-08-28T12:00:00Z'
        )
        self.url = reverse('comments:add_comment', kwargs={'slug': self.post.slug})

    def test_create_comment_authenticated(self):
        """Test that an authenticated user can create a comment."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': 'This is a test comment.'})
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())

    def test_create_comment_unauthenticated(self):
        """Test that an unauthenticated user cannot create a comment."""
        response = self.client.post(self.url, {'content': 'This comment should not be created.'})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
        self.assertFalse(Comment.objects.filter(content='This comment should not be created.').exists())

    def test_create_comment_invalid_data(self):
        """Test that invalid comment data does not create a comment."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.assertFalse(Comment.objects.filter(content='').exists())


class CommentUpdateViewTest(TestCase):
    def setUp(self):
        # Create test users, blog post, and comment
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            status='published',
            published_at='2024-08-28T12:00:00Z'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        self.url = reverse('comments:comment_update', kwargs={'pk': self.comment.pk})

    def test_update_comment_authenticated_author(self):
        """Test that the comment author can update the comment."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': 'Updated comment content.'})
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content.')

    def test_update_comment_authenticated_non_author(self):
        """Test that a user who is not the author cannot update the comment."""
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(self.url, {'content': 'This update should not be allowed.'})
        self.assertEqual(response.status_code, 403)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'This is a test comment.')

    def test_update_comment_unauthenticated(self):
        """Test that an unauthenticated user cannot update the comment."""
        response = self.client.post(self.url, {'content': 'This update should not be allowed.'})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'This is a test comment.')

    def test_update_comment_invalid_data(self):
        """Test that invalid comment data does not update the comment."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'This is a test comment.')


class CommentDeleteViewTest(TestCase):
    def setUp(self):
        # Create test users, blog post, and comment
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            status='published',
            published_at='2024-08-28T12:00:00Z'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        self.url = reverse('comments:comment_delete', kwargs={'pk': self.comment.pk})

    def test_delete_comment_authenticated_author(self):
        """Test that the comment author can delete the comment."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_authenticated_non_author(self):
        """Test that a user who is not the author cannot delete the comment."""
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_unauthenticated(self):
        """Test that an unauthenticated user cannot delete the comment."""
        response = self.client.post(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
