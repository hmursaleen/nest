from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blogs.models import BlogPost, Tag
from datetime import datetime




class BlogPostListViewTests(TestCase):
    def setUp(self):
        # Create a user to associate with the blog posts
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Python')

        # Create blog posts
        self.post1 = BlogPost.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='This is the content of the first test post.',
            author=self.user,
            status='published',
            published_at=datetime.now()
        )
        self.post1.tags.add(self.tag1)

        self.post2 = BlogPost.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='This is the content of the second test post.',
            author=self.user,
            status='draft',
        )
        self.post2.tags.add(self.tag2)

        self.post3 = BlogPost.objects.create(
            title='Test Post 3',
            slug='test-post-3',
            content='This is the content of the third test post.',
            author=self.user,
            status='published',
            published_at=datetime.now()
        )
        self.post3.tags.add(self.tag1, self.tag2)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 2)

    def test_lists_all_published_posts(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 2)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post3.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_content_display(self):
        response = self.client.get(reverse('blogs:post_list'))
        self.assertContains(response, 'This is the content of the first test post.')
        self.assertContains(response, 'This is the content of the third test post.')







class BlogPostCreateViewTests(TestCase):

    def setUp(self):
        # Create a user to log in
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Python')

        # Set up the client and log in the user
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_create_post_url_exists_at_desired_location(self):
        response = self.client.get('/blogs/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_post_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_uses_correct_template(self):
        response = self.client.get(reverse('blogs:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_form.html')




    def test_create_post_form_valid(self):
	    data = {
	        'title': 'New Blog Post',
	        'slug': 'new-blog-post',
	        'content': 'This is a test blog post.',
	        'status': 'published',
	        'published_at': datetime.now(),
	        'tags': [self.tag1.id, self.tag2.id]
	    }
	    response = self.client.post(reverse('blogs:post_create'), data)
	    self.assertEqual(response.status_code, 302)  # Ensure it redirects after creation
	    self.assertTrue(BlogPost.objects.filter(slug='new-blog-post').exists())


    
    def test_redirect_after_create(self):
        data = {
            'title': 'Redirect Test Post',
            'slug': 'redirect-test-post',
            'content': 'This is a test blog post.',
            'status': 'published',
            'published_at': datetime.now(),
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post(reverse('blogs:post_create'), data)
        post = BlogPost.objects.get(slug='redirect-test-post')
        self.assertRedirects(response, reverse('blogs:post_detail', kwargs={'slug': post.slug}))

    



    def test_create_post_without_authentication(self):
        self.client.logout()
        data = {
            'title': 'Unauthenticated Post',
            'slug': 'unauthenticated-post',
            'content': 'This should not be created.',
            'status': 'published',
            'published_at': datetime.now(),
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post(reverse('blogs:post_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertRedirects(response, '/accounts/login/?next=/blogs/create/')
        self.assertFalse(BlogPost.objects.filter(slug='unauthenticated-post').exists())








class BlogPostDetailViewTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Python')

        # Create a blog post
        self.post = BlogPost.objects.create(
            title='Test Blog Post',
            slug='test-blog-post',
            content='This is a test blog post content.',
            author=self.user,
            status='published',
            published_at=datetime.now()
        )
        self.post.tags.add(self.tag1, self.tag2)

        # Set up the client
        self.client = Client()

    def test_blogpost_detail_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/blogs/{self.post.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_blogpost_detail_view_accessible_by_name(self):
        response = self.client.get(reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blogpost_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_detail.html')

    def test_blogpost_detail_view_displays_correct_post(self):
        response = self.client.get(reverse('blogs:post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

    def test_blogpost_detail_view_for_non_existent_post(self):
        response = self.client.get(reverse('blogs:post_detail', kwargs={'slug': 'non-existent-post'}))
        self.assertEqual(response.status_code, 404)








class BlogPostUpdateViewTests(TestCase):

    def setUp(self):
        # Create two users: one author and one non-author
        self.author = User.objects.create_user(username='author', password='testpassword')
        self.non_author = User.objects.create_user(username='nonauthor', password='testpassword')

        # Create some tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Python')

        # Create a blog post by the author
        self.post = BlogPost.objects.create(
            title='Original Blog Post',
            slug='original-blog-post',
            content='Original content of the blog post.',
            author=self.author,
            status='published',
            published_at=datetime.now()
        )
        self.post.tags.add(self.tag1, self.tag2)

        # Set up the client
        self.client = Client()

    def test_blogpost_update_view_accessible_by_author(self):
        self.client.login(username='author', password='testpassword')
        response = self.client.get(reverse('blogs:post_update', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blogpost_update_view_inaccessible_by_non_author(self):
        self.client.login(username='nonauthor', password='testpassword')
        response = self.client.get(reverse('blogs:post_update', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 403)

    def test_blogpost_update_view_uses_correct_template(self):
        self.client.login(username='author', password='testpassword')
        response = self.client.get(reverse('blogs:post_update', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_form.html')

    def test_blogpost_update_with_valid_data(self):
        self.client.login(username='author', password='testpassword')
        new_data = {
            'title': 'Updated Blog Post',
            'slug': 'updated-blog-post',
            'content': 'Updated content of the blog post.',
            'tags': [self.tag1.id, self.tag2.id],
            'status': 'published',
            'published_at': datetime.now(),
        }
        response = self.client.post(reverse('blogs:post_update', kwargs={'slug': self.post.slug}), new_data)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.title, 'Updated Blog Post')
        self.assertEqual(self.post.slug, 'updated-blog-post')
        self.assertEqual(self.post.content, 'Updated content of the blog post.')

    def test_blogpost_update_with_invalid_data(self):
        self.client.login(username='author', password='testpassword')
        invalid_data = {
            'title': '',  # Title is required
            'slug': '',  # Slug is required
            'content': '',
            'tags': [self.tag1.id, self.tag2.id],
            'status': 'published',
            'published_at': datetime.now(),
        }
        response = self.client.post(reverse('blogs:post_update', kwargs={'slug': self.post.slug}), invalid_data)
        self.assertEqual(response.status_code, 200)  # The form should re-render with errors
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'slug', 'This field is required.')









class BlogPostDeleteViewTests(TestCase):

    def setUp(self):
        # Create two users: one author and one non-author
        self.author = User.objects.create_user(username='author', password='testpassword')
        self.non_author = User.objects.create_user(username='nonauthor', password='testpassword')

        # Create some tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Python')

        # Create a blog post by the author
        self.post = BlogPost.objects.create(
            title='Original Blog Post',
            slug='original-blog-post',
            content='Original content of the blog post.',
            author=self.author,
            status='published',
            published_at=datetime.now()
        )
        self.post.tags.add(self.tag1, self.tag2)

        # Set up the client
        self.client = Client()

    def test_blogpost_delete_view_accessible_by_author(self):
        self.client.login(username='author', password='testpassword')
        response = self.client.get(reverse('blogs:post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blogpost_delete_view_inaccessible_by_non_author(self):
        self.client.login(username='nonauthor', password='testpassword')
        response = self.client.get(reverse('blogs:post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 403)

    def test_blogpost_delete_view_uses_correct_template(self):
        self.client.login(username='author', password='testpassword')
        response = self.client.get(reverse('blogs:post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blogpost_confirm_delete.html')

    def test_blogpost_successful_deletion(self):
        self.client.login(username='author', password='testpassword')
        response = self.client.post(reverse('blogs:post_delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogs:post_list'))

        # Ensure the post is deleted
        self.assertFalse(BlogPost.objects.filter(slug='original-blog-post').exists())
