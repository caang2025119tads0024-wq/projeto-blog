from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostDetailViewTests(TestCase):
    def test_post_detail_renders_post_content(self):
        user = get_user_model().objects.create_user(
            username='autor',
            email='autor@example.com',
            password='senha123'
        )
        post = Post.objects.create(
            title='Primeiro post',
            slug='primeiro-post',
            author=user,
            body='Conteúdo completo do post.',
            status=Post.Status.PUBLISHED,
        )

        response = self.client.get(reverse('blog:post_detail', args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Primeiro post')
        self.assertContains(response, 'Conteúdo completo do post.')
