from desafio.core.forms import UploadForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r

__author__ = 'lucas'


class UploadTestGet(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='hello', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        self.resp_invalid = self.client.get(r('upload'))
        self.client.login(username='testuser', password='hello')
        self.resp = self.client.get(r('upload'))

    def test_get_user_invalid(self):
        """ GET  /upload must return status code 200 """
        self.assertEqual(302, self.resp_invalid.status_code)

    def test_get_user_valid(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_user_valid(self):
        self.assertTemplateUsed(self.resp, 'upload.html')

    def test_html(self):
        """HTML must contains input tags"""
        tags = (('<form',1),
                ('<input', 3),
                ('type="submit"',1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have upload form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, UploadForm)


class UploadTestPostValid(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='hello', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        self.client.login(username='testuser', password='hello')
        with open('example_input.tab') as data:
            self.resp = self.client.post(r('upload'), {'file': data})

    def test_post(self):
        self.assertContains(self.resp, "Receita Total : 95")


class UploadTestPostInValid(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='hello', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('hello')
        self.user.save()
        self.client.login(username='testuser', password='hello')
        self.resp = self.client.post(r('upload'), {'file': {}})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

