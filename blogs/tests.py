from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from blogs.models import BlogPost, Tag
from blogs.forms import BlogPostForm

class BlogPostListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create tags
        tag1 = Tag.objects.create(name='Django')
        tag2 = Tag.objects.create(name='Python')

        # Create 15 blog posts for pagination testing
        for i in range(15):
            post = BlogPost.objects.create(
                title=f'Blog Post {i}',
                content='This is a test post content',
                author=cls.user,
            )
            post.tags.add(tag1, tag2)


    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 10)

    def test_lists_all_posts(self):
        # Get second page and confirm it has the remaining 5 posts
        response = self.client.get(reverse('blogs:post_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)

    def test_post_ordering(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        for i in range(len(posts) - 1):
            self.assertTrue(posts[i].created_at >= posts[i+1].created_at)









class BlogPostCreateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='password')

        # Create a tag for testing
        cls.tag = Tag.objects.create(name='Test Tag')

    def test_redirect_if_not_logged_in(self):
        # Try to access the create view without being logged in
        response = self.client.get(reverse('blogs:post_create'))
        self.assertRedirects(response, '/accounts/login/?next=/post/new/')

    def test_logged_in_user_can_access_create_view(self):
        # Log in as a valid user
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('blogs:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_form.html')

    def test_successful_post_creation(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password')

        # Data to create a valid blog post
        post_data = {
            'title': 'Test Blog Post',
            'content': 'This is a test post content.',
            'tags': [self.tag.id]  # Select a valid tag
        }

        # Submit the post creation form
        response = self.client.post(reverse('blogs:post_create'), data=post_data)

        # Check that the user is redirected to the post detail page after creation
        self.assertRedirects(response, reverse_lazy('blogs:post_detail', kwargs={'pk': BlogPost.objects.first().pk}))

        # Verify that the post is created in the database
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, 'Test Blog Post')
        self.assertEqual(post.content, 'This is a test post content.')
        self.assertEqual(post.author, self.user)
        self.assertIn(self.tag, post.tags.all())

    def test_form_validation_for_missing_tags(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password')

        # Invalid data (no tags selected)
        invalid_data = {
            'title': 'Test Blog Post',
            'content': 'This post has no tags.',
            'tags': []  # No tags selected
        }

        # Submit the form with invalid data
        response = self.client.post(reverse('blogs:post_create'), data=invalid_data)
        form = response.context.get('form')

        # Check that the form contains an error for the 'tags' field
        self.assertFalse(form.is_valid())
        self.assertIn('Please select at least one tag.', form.errors['tags'])

    def test_form_fields_rendered_properly(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('blogs:post_create'))

        # Check that the correct form fields are rendered in the response
        self.assertContains(response, 'Enter post title here')
        self.assertContains(response, 'Write your content here...')
        self.assertContains(response, 'form-control w-full border border-gray-300 rounded-md shadow-sm')









class BlogPostDeleteViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user and another user for testing access control
        cls.author = User.objects.create_user(username='author', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')

        # Create a tag and a blog post
        cls.tag = Tag.objects.create(name='Test Tag')
        cls.post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test post.',
            author=cls.author
        )
        cls.post.tags.add(cls.tag)

    def test_redirect_if_not_logged_in(self):
        # Try to delete a post without being logged in
        response = self.client.get(reverse('blogs:post_delete', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/post/{self.post.pk}/delete/')

    def test_logged_in_but_not_author(self):
        # Log in as a user who is not the author of the post
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('blogs:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden access

    def test_author_can_access_delete_view(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')
        response = self.client.get(reverse('blogs:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_confirm_delete.html')

    def test_successful_post_deletion(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')
        response = self.client.post(reverse('blogs:post_delete', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, reverse_lazy('blogs:post_list'))

        # Verify that the post has been deleted
        with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(pk=self.post.pk)

    def test_delete_view_redirects_after_deletion(self):
        # Log in as the author of the post and delete it
        self.client.login(username='author', password='password')
        response = self.client.post(reverse('blogs:post_delete', kwargs={'pk': self.post.pk}))

        # Verify that the user is redirected to the blog post list
        self.assertRedirects(response, reverse('blogs:post_list'))

        # Verify that the post count is zero (the post is deleted)
        self.assertEqual(BlogPost.objects.count(), 0)










class BlogPostUpdateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user (author) and another user for access control
        cls.author = User.objects.create_user(username='author', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')

        # Create a tag and a blog post
        cls.tag = Tag.objects.create(name='Test Tag')
        cls.post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test post.',
            author=cls.author
        )
        cls.post.tags.add(cls.tag)

    def test_redirect_if_not_logged_in(self):
        # Try to access the update view without being logged in
        response = self.client.get(reverse('blogs:post_update', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/post/{self.post.pk}/edit/')

    def test_logged_in_but_not_author(self):
        # Log in as a user who is not the author of the post
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('blogs:post_update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden access

    def test_author_can_access_update_view(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')
        response = self.client.get(reverse('blogs:post_update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_update_form.html')

    def test_successful_post_update(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')

        # Data to update the post
        updated_data = {
            'title': 'Updated Blog Post',
            'content': 'This is an updated test post.',
            'tags': [self.tag.id]  # Use the existing tag
        }

        response = self.client.post(reverse('blogs:post_update', kwargs={'pk': self.post.pk}), data=updated_data)
        self.assertRedirects(response, reverse_lazy('blogs:post_detail', kwargs={'pk': self.post.pk}))

        # Verify that the post is updated in the database
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Blog Post')
        self.assertEqual(self.post.content, 'This is an updated test post.')

    def test_form_validation_for_missing_tags(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')

        # Post data with missing tags
        invalid_data = {
            'title': 'Invalid Post Update',
            'content': 'This update is missing tags.',
            'tags': []  # No tags selected
        }

        response = self.client.post(reverse('blogs:post_update', kwargs={'pk': self.post.pk}), data=invalid_data)
        form = response.context.get('form')

        # Check that the form contains an error for the 'tags' field
        self.assertFalse(form.is_valid())
        self.assertIn('Please select at least one tag.', form.errors['tags'])

    def test_update_view_renders_correct_form(self):
        # Log in as the author of the post
        self.client.login(username='author', password='password')
        response = self.client.get(reverse('blogs:post_update', kwargs={'pk': self.post.pk}))

        # Check if the form is rendered with the correct fields
        form = response.context.get('form')
        self.assertIsInstance(form, BlogPostForm)
        self.assertContains(response, 'Enter post title here')
        self.assertContains(response, 'Write your content here...')








class TagDetailViewPaginationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_user(username='testuser', password='12345')

        # Create a tag
        cls.tag = Tag.objects.create(name="Django")

        # Create multiple blog posts (more than 10 to test pagination)
        number_of_posts = 15  # More than the paginate_by (10)
        for i in range(number_of_posts):
            post = BlogPost.objects.create(
                title=f"Test Post {i+1}",
                content="This is test content.",
                author=cls.user,
            )
            post.tags.add(cls.tag)

    def test_pagination_is_correct(self):
        # Get the first page of tag detail view
        response = self.client.get(reverse('blogs:tag_detail', kwargs={'name': 'Django'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 10)  # Expecting 10 posts per page

        # Get the second page of tag detail view
        response = self.client.get(reverse('blogs:tag_detail', kwargs={'name': 'Django'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 5)  # Expecting 5 posts on second page (total 15)

    def test_invalid_page_number(self):
        # Test requesting a non-existing page
        response = self.client.get(reverse('blogs:tag_detail', kwargs={'name': 'Django'}) + '?page=999')
        self.assertEqual(response.status_code, 404)  # Page not found for invalid page number

    def test_no_posts_for_tag(self):
        # Test for a tag with no posts
        new_tag = Tag.objects.create(name="NoPostsTag")
        response = self.client.get(reverse('blogs:tag_detail', kwargs={'name': 'NoPostsTag'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts found for this tag.")











from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.tag = Tag.objects.create(name='django')
        self.client.login(username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user).access_token
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_blog_post(self):
        data = {
            "title": "Test Blog Post",
            "content": "This is a test blog post.",
            "tags": [self.tag.name]
        }
        response = self.client.post('/api/blogs/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(BlogPost.objects.get().title, "Test Blog Post")

    def test_get_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="Existing Blog Post", content="This is an existing blog post.",
            author=self.user
        )
        blog_post.tags.add(self.tag)
        response = self.client.get(f'/api/blogs/posts/{blog_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], blog_post.title)

    def test_update_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="Update Blog Post", content="This is a blog post to be updated.",
            author=self.user
        )
        blog_post.tags.add(self.tag)
        data = {
            "title": "Updated Blog Post",
            "content": "This blog post has been updated.",
            "tags": [self.tag.name]
        }
        response = self.client.put(f'/api/blogs/posts/{blog_post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_post.refresh_from_db()
        self.assertEqual(blog_post.title, "Updated Blog Post")

    def test_delete_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="Delete Blog Post", content="This blog post will be deleted.",
            author=self.user
        )
        blog_post.tags.add(self.tag)
        response = self.client.delete(f'/api/blogs/posts/{blog_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)
