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
