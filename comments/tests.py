from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blogs.models import BlogPost, Tag
from comments.models import Comment

class CommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a blog post
        cls.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            content="Test content for the blog post.",
            author=cls.user
        )
    
    def setUp(self):
        # Log in the user before each test
        self.client.login(username='testuser', password='testpass')

    def test_create_comment(self):
        """Test that a logged-in user can create a comment."""
        url = reverse('comments:add_comment', kwargs={'pk': self.blog_post.pk})
        data = {
            'content': 'This is a test comment.'
        }
        response = self.client.post(url, data)

        # Ensure the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.blog_post)

        # Ensure the user is redirected to the blog post detail page
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'pk': self.blog_post.pk}))

    def test_create_comment_without_content(self):
        """Test that the comment cannot be created without content."""
        url = reverse('comments:add_comment', kwargs={'pk': self.blog_post.pk})
        data = {
            'content': ''  # Empty content
        }
        response = self.client.post(url, data)

        # Ensure the comment was not created
        self.assertEqual(Comment.objects.count(), 0)

        # Ensure the form is returned with errors
        self.assertEqual(response.status_code, 200)
        #self.assertFormError(response, 'form', 'content', "The comment cannot be empty.")

    def test_comment_form_display(self):
        """Test that the comment form is displayed properly."""
        url = reverse('comments:add_comment', kwargs={'pk': self.blog_post.pk})
        response = self.client.get(url)

        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the form is rendered in the template
        self.assertContains(response, 'Write your comment here...')
        self.assertContains(response, 'Submit Comment')

    def test_redirect_if_not_logged_in(self):
        """Test that the user is redirected to the login page if not logged in."""
        self.client.logout()
        url = reverse('comments:add_comment', kwargs={'pk': self.blog_post.pk})
        response = self.client.get(url)

        # Ensure the user is redirected to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={url}")








class CommentUpdateViewTest(TestCase):
    
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        
        # Create a blog post
        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            content="Test content",
            author=self.user1
        )

        # Create a comment
        self.comment = Comment.objects.create(
            post=self.blog_post,
            author=self.user1,
            content="Test comment content"
        )

        # URL for updating the comment
        self.url = reverse('comments:comment_update', kwargs={'pk': self.comment.pk})
    
    def test_get_comment_update_view_as_author(self):
        # Author should be able to access the update view
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_update_form.html')
        self.assertContains(response, "Update comment")
        self.assertContains(response, self.comment.content)

    def test_get_comment_update_view_as_non_author(self):
        # Non-author should be redirected and not allowed to update the comment
        self.client.login(username='user2', password='password2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect due to permission denial
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'pk': self.blog_post.pk}))

    def test_post_valid_data_as_author(self):
        # Author submits valid data to update the comment
        self.client.login(username='user1', password='password1')
        response = self.client.post(self.url, {'content': 'Updated comment content'}, follow=True)
        
        # Check if the comment content is updated
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content')

        # Ensure the user is redirected back to the blog post detail page
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'pk': self.blog_post.pk}))
    
    def test_post_invalid_data_as_author(self):
        # Author submits invalid data (empty content)
        self.client.login(username='user1', password='password1')
        response = self.client.post(self.url, {'content': ''})

        # Form should not be valid, and the form should be rendered again
        self.assertEqual(response.status_code, 200)
        #self.assertFormError(response, 'form', 'content', 'The comment cannot be empty.')

    def test_post_valid_data_as_non_author(self):
        # Non-author attempts to submit valid data, should be denied
        self.client.login(username='user2', password='password2')
        response = self.client.post(self.url, {'content': 'Non-author updated content'})

        # The comment should not be updated
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, 'Non-author updated content')

        # Non-author should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'pk': self.blog_post.pk}))







class CommentDeleteViewTest(TestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='author', email='author@example.com', password='password123')
        self.other_user = User.objects.create_user(username='other', email='other@example.com', password='password123')

        # Create a blog post
        self.post = BlogPost.objects.create(
            title='Sample Post',
            content='This is a sample post',
            author=self.user
        )

        # Create a comment by the author
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a sample comment'
        )

        # URL for deleting the comment
        self.delete_url = reverse('comments:comment_delete', kwargs={'pk': self.comment.pk})

    def test_comment_delete_view_access_by_author(self):
        # Author logs in
        self.client.login(username='author', password='password123')

        # Access the delete page
        response = self.client.get(self.delete_url)

        # Check if the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_confirm_delete.html')

    def test_comment_delete_view_access_denied_to_non_author(self):
        # Other user logs in
        self.client.login(username='other', password='password123')

        # Try to access the delete page
        response = self.client.get(self.delete_url)

        # Check if access is forbidden
        self.assertEqual(response.status_code, 403)

    def test_comment_delete_success(self):
        # Author logs in
        self.client.login(username='author', password='password123')

        # Submit the delete form (POST request)
        response = self.client.post(self.delete_url)

        # Check if the comment has been deleted
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

        # Check if the user is redirected to the post detail page after deletion
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'pk': self.post.pk}))

    def test_unauthorized_user_cannot_delete_comment(self):
        # Non-author tries to delete the comment
        self.client.login(username='other', password='password123')

        # Attempt to delete (POST request)
        response = self.client.post(self.delete_url)

        # Check if the comment still exists
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

        # Check if the response is forbidden (403)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_access_delete_view(self):
        # Anonymous user tries to access the delete view
        response = self.client.get(self.delete_url)

        # Redirect to login page
        self.assertRedirects(response, f'/accounts/login/?next={self.delete_url}')

    def test_anonymous_user_cannot_delete_comment(self):
        # Anonymous user tries to delete the comment (POST request)
        response = self.client.post(self.delete_url)

        # Check if the comment still exists
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

        # Check if the response is a redirect to the login page
        self.assertRedirects(response, f'/accounts/login/?next={self.delete_url}')









class ReplyCreateViewTest(TestCase):
    def setUp(self):
        """Set up reusable test data."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.post = BlogPost.objects.create(title='Test Post', content='Test content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Test comment')
        self.reply_url = reverse('comments:reply_comment', kwargs={'pk': self.comment.pk})

    def test_reply_creation_success(self):
        """Test if reply creation works for logged-in user."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.reply_url, {
            'content': 'This is a reply.'
        })
        
        # Check if the response is a redirect (HTTP 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the reply was created
        self.assertEqual(Comment.objects.count(), 2)
        reply = Comment.objects.get(parent=self.comment)
        self.assertIsNotNone(reply)
        self.assertEqual(reply.content, 'This is a reply.')
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.post, self.post)
        self.assertEqual(reply.parent, self.comment)

    def test_reply_creation_invalid_form(self):
        """Test reply creation fails with invalid form (empty content)."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.reply_url, {
            'content': ''  # Invalid content (empty)
        })
        
        # Check if the form is rendered again with errors (HTTP 200)
        self.assertEqual(response.status_code, 200)
        
        # Ensure no additional comments were created
        self.assertEqual(Comment.objects.count(), 1)

    def test_reply_creation_unauthenticated_user(self):
        """Test unauthenticated users cannot create replies."""
        response = self.client.post(self.reply_url, {
            'content': 'This is a reply.'
        })
        
        # Check that the unauthenticated user is redirected to login page (HTTP 302)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

        # Ensure no additional comments were created
        self.assertEqual(Comment.objects.count(), 1)

    def test_reply_creation_by_different_user(self):
        """Test if another logged-in user can reply."""
        self.client.login(username='otheruser', password='password123')
        response = self.client.post(self.reply_url, {
            'content': 'Reply by another user.'
        })
        
        # Check if the response is a redirect (HTTP 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if the reply by other user was created
        self.assertEqual(Comment.objects.count(), 2)
        reply = Comment.objects.get(parent=self.comment)
        self.assertEqual(reply.content, 'Reply by another user.')
        self.assertEqual(reply.author, self.other_user)
        self.assertEqual(reply.parent, self.comment)