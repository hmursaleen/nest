from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blogs.models import BlogPost
from comments.models import Comment

User = get_user_model()

class CommentCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = BlogPost.objects.create(title='Test Post', slug='dont-mess', content='Post content', author=self.user)
        self.url = reverse('comments:add_comment', kwargs={'slug': self.post.slug})

    def test_create_comment(self):
        self.client.login(username='testuser', password='password')
        data = {
            'content': 'This is a test comment.',
            'parent': '',  # Omit the parent or set it to an empty string if there's no parent
        }
        response = self.client.post(self.url, data)
        
        # Check that the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertIsNone(comment.parent)  # Ensure it's a top-level comment
        self.assertEqual(response.status_code, 302)  # Check for successful redirect

    def test_create_reply(self):
        self.client.login(username='testuser', password='password')
        parent_comment = Comment.objects.create(post=self.post, author=self.user, content='Parent comment')
        data = {
            'content': 'This is a reply to the parent comment.',
            'parent': parent_comment.id,  # Pass the ID of the parent comment
        }
        response = self.client.post(self.url, data)

        # Filter the comment based on the parent and content
        reply_comment = Comment.objects.filter(parent=parent_comment).last()
        
        # Check that the reply was created
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(reply_comment.content, 'This is a reply to the parent comment.')
        self.assertEqual(reply_comment.author, self.user)
        self.assertEqual(reply_comment.post, self.post)
        self.assertEqual(reply_comment.parent, parent_comment)  # Ensure it's a reply to the parent comment
        self.assertEqual(response.status_code, 302)  # Check for successful redirect









'''
class CommentUpdateViewTest(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.other_user = User.objects.create_user(
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
        self.update_url = reverse('comments:comment_update', kwargs={'pk': self.comment.pk})
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
        self.assertRedirects(response, f"{reverse('login')}?next={self.update_url}")  # Redirect to login page

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
'''







'''
class CommentDeleteViewTest(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.other_user = User.objects.create_user(
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
        self.delete_url = reverse('comments:comment_delete', kwargs={'pk': self.comment.pk})
        self.post_detail_url = reverse('blogs:post_detail', kwargs={'slug': self.post.slug})

    def test_delete_comment_success(self):
        """Test that the comment author can successfully delete the comment."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.post_detail_url)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_by_non_author(self):
        """Test that a user who is not the author cannot delete the comment."""
        self.client.login(username='otheruser', password='password')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_not_logged_in(self):
        """Test that a user who is not logged in cannot delete the comment."""
        response = self.client.post(self.delete_url)
        login_url = reverse('login')
        expected_url = f"{login_url}?next={self.delete_url}"
        self.assertRedirects(response, expected_url)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
'''