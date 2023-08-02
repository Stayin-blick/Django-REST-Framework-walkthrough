from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testing1')

    def test_can_list_post(self):
        testuser = User.objects.get(username='testuser')
        Post.objects.create(owner=testuser, title='auto test')
        Response = self.client.get('/posts/')
        self.assertEqual(Response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='testuser', password='testing1')
        Response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(Response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        Response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(Response.status_code, status.HTTP_403_FORBIDDEN)
