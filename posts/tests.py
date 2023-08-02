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


class PostDetailViewTest(APITestCase):
    def setUp(self):
        testuser1 = User.objects.create_user(
            username='testuser1', password='testing1'
            )
        testuser2 = User.objects.create_user(
            username='testuser2', password='testing1'
            )
        Post.objects.create(
            owner='testuser1', title='a title', content='testuser1 content'
        )
        Post.objects.create(
            owner='testuser2', title='a title', content='testuser2 content'
        )

    def test_can_retreieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retreieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='testuser1', password='testing1')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='testuser1', password='testing1')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
