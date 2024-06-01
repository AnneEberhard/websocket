import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Chat

User = get_user_model()


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('index')

    def test_index_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/index.html')

    def test_index_view_without_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')


class RoomViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.chat = Chat.objects.create(room_name='Test Room', slug='test-room')
        self.url = reverse('room', kwargs={'room_slug': self.chat.slug})

    def test_room_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertIn('messages', response.context)

    def test_room_view_with_no_room(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('room', kwargs={'room_slug': 'no-room'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Chat.objects.filter(slug='no-room').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])

    def test_login_failure(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['success'])
