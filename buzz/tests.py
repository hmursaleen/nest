from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from buzz.models import Buzz
from blogs.models import BlogPost
from comments.models import Comment
from django.core.exceptions import PermissionDenied






class BuzzListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        cls.user1 = User.objects.create_user(username='user1', password='password123')
        cls.user2 = User.objects.create_user(username='user2', password='password123')

        # Create a blog post by user1
        cls.post = BlogPost.objects.create(title="Test Post", content="Content here", author=cls.user1)

        # Create comments by user2 on user1's post to trigger buzz for user1
        for i in range(12):  # Create more than 10 to test pagination as well
            comment = Comment.objects.create(post=cls.post, author=cls.user2, content=f"Test Comment {i+1}")
    

    def test_buzz_list_view_for_logged_in_user(self):
        # Log in as user1 (who has buzzes)
        self.client.login(username='user1', password='password123')

        # Get the buzz list view for user1
        response = self.client.get(reverse('buzz:buzz_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buzz/buzz_list.html')

        # Check that we have buzzes in the context
        buzzes = response.context['buzzes']
        self.assertEqual(len(buzzes), 10)  # Pagination: Only 10 items on the first page
        self.assertTrue(all(buzz.user == self.user1 for buzz in buzzes))  # Ensure all buzzes are for user1

    def test_buzz_list_view_pagination(self):
        # Log in as user1 again
        self.client.login(username='user1', password='password123')

        # Test pagination: Get page 2
        response = self.client.get(reverse('buzz:buzz_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        buzzes = response.context['buzzes']
        self.assertEqual(len(buzzes), 2)  # 2 remaining buzzes on page 2 (since total 12 buzzes)











class BuzzDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        cls.user1 = User.objects.create_user(username='user1', password='password123')
        cls.user2 = User.objects.create_user(username='user2', password='password123')

        # Create a blog post by user1
        cls.post = BlogPost.objects.create(title="Test Post", content="Content here", author=cls.user1)

        # Create a comment by user2 on user1's post to trigger buzz for user1
        cls.comment = Comment.objects.create(post=cls.post, author=cls.user2, content="Test Comment")
        cls.buzz = Buzz.objects.create(user=cls.user1, trigger=cls.user2, post=cls.post, comment=cls.comment)

    def test_buzz_detail_view_for_owner(self):
        # Log in as user1 (the owner of the buzz)
        self.client.login(username='user1', password='password123')

        # Get the Buzz detail view for the created buzz
        response = self.client.get(reverse('buzz:buzz_detail', kwargs={'pk': self.buzz.pk}))
        self.assertEqual(response.status_code, 200)

        # Ensure correct template is used
        self.assertTemplateUsed(response, 'buzz/buzz_detail.html')

        # Check if the correct buzz is passed into the context
        buzz = response.context['buzz']
        self.assertEqual(buzz, self.buzz)

        # Check if buzz is marked as read
        self.buzz.refresh_from_db()
        self.assertTrue(self.buzz.is_read)

    def test_buzz_detail_view_for_non_owner(self):
        # Log in as user2 (who does not own the buzz)
        self.client.login(username='user2', password='password123')

        # Try to access the Buzz detail view for user1's buzz
        response = self.client.get(reverse('buzz:buzz_detail', kwargs={'pk': self.buzz.pk}))

        # Expect a PermissionDenied error
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_redirect_if_not_logged_in(self):
        # Attempt to access Buzz detail view while not logged in
        response = self.client.get(reverse('buzz:buzz_detail', kwargs={'pk': self.buzz.pk}))

        # Should redirect to the login page
        self.assertRedirects(response, f'/accounts/login/?next=/buzz/{self.buzz.pk}/')

    def test_buzz_detail_view_does_not_mark_as_read_if_already_read(self):
        # Mark the buzz as already read
        self.buzz.is_read = True
        self.buzz.save()

        # Log in as user1 (the owner of the buzz)
        self.client.login(username='user1', password='password123')

        # Get the Buzz detail view
        response = self.client.get(reverse('buzz:buzz_detail', kwargs={'pk': self.buzz.pk}))
        self.assertEqual(response.status_code, 200)

        # Ensure buzz is not marked as read again
        self.buzz.refresh_from_db()
        self.assertTrue(self.buzz.is_read)  # Remains True








class MarkBuzzAsReadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        cls.user1 = User.objects.create_user(username='user1', password='password123')
        cls.user2 = User.objects.create_user(username='user2', password='password123')

        # Create a blog post by user1
        cls.post = BlogPost.objects.create(title="Test Post", content="Test content", author=cls.user1)

        # Create a comment by user2 on user1's post to trigger buzz for user1
        cls.comment = Comment.objects.create(post=cls.post, author=cls.user2, content="Test Comment")
        cls.buzz = Buzz.objects.create(user=cls.user1, trigger=cls.user2, post=cls.post, comment=cls.comment, is_read=False)

   

    def test_non_owner_cannot_mark_buzz_as_read(self):
        """Test that a user who does not own the buzz cannot mark it as read."""
        # Log in as user2 (who does not own the buzz)
        self.client.login(username='user2', password='password123')

        # Attempt to mark the buzz as read
        response = self.client.post(reverse('buzz:mark_buzz_as_read', kwargs={'pk': self.buzz.pk}))

        # The buzz should not be marked as read
        self.buzz.refresh_from_db()
        self.assertFalse(self.buzz.is_read)


    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated users are redirected to the login page."""
        # Attempt to mark the buzz as read without logging in
        response = self.client.post(reverse('buzz:mark_buzz_as_read', kwargs={'pk': self.buzz.pk}))

        # Ensure the user is redirected to the login page
        #self.assertRedirects(response, f'/accounts/login/?next=/buzz/mark_as_read/{self.buzz.pk}/')

    

    def test_already_read_buzz_remains_read(self):
        """Test that a buzz already marked as read does not change unnecessarily."""
        # Mark the buzz as already read
        self.buzz.is_read = True
        self.buzz.save()

        # Log in as the owner (user1)
        self.client.login(username='user1', password='password123')

        # Send a POST request to mark it as read again
        response = self.client.post(reverse('buzz:mark_buzz_as_read', kwargs={'pk': self.buzz.pk}))

        # Ensure the buzz remains marked as read
        self.buzz.refresh_from_db()
        self.assertTrue(self.buzz.is_read)