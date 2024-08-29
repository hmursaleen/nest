from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.models import BlogPost
from comments.models import Comment

class CommentUpdateViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser', password='password'
        )
        
        # Create a blog post
        self.post = BlogPost.objects.create(
            title='Test Blog Post',
            slug='test-blog-post',
            content='This is a test blog post.',
            author=self.user
        )
        
        # Create a comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        
        # URLs
        self.update_url = reverse('comments:comment_update', kwargs={'pk': self.comment.pk, 'slug': self.post.slug})
        self.post_detail_url = reverse('blogs:post_detail', kwargs={'slug': self.post.slug})

    def test_update_comment_success(self):
        """Test that the comment author can successfully update the comment."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.update_url, {
            'content': 'Updated comment content.'
        })
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_detail_url)
        self.assertEqual(self.comment.content, 'Updated comment content.')

    def test_update_comment_by_non_author(self):
        """Test that a user who is not the author cannot update the comment."""
        self.client.login(username='otheruser', password='password')
        response = self.client.post(self.update_url, {
            'content': 'This should not work.'
        })
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertNotEqual(self.comment.content, 'This should not work.')

    def test_update_comment_not_logged_in(self):
        """Test that a user who is not logged in cannot update the comment."""
        response = self.client.post(self.update_url, {
            'content': 'This should not work either.'
        })
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, 'This should not work either.')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_update_comment_form_invalid(self):
        """Test that submitting an invalid form does not update the comment."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.update_url, {
            'content': ''  # Invalid content
        })
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertEqual(self.comment.content, 'This is a test comment.')  # Content remains unchanged
        self.assertContains(response, "This field is required.")  # Form error displayed
