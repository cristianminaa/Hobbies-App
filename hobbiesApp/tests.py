import os

from .models import *
from django.contrib import auth
from django.contrib.auth import authenticate
from .database import info
from django.test import TestCase

# These basic tests are to be used as an example for running tests in S2I
# and OpenShift when building an application image.


class PageViewModelTest(TestCase):
    def test_viewpage_model(self):
        pageview = PageView.objects.create(hostname='localhost')
        pagetest = PageView.objects.get(hostname='localhost')
        self.assertEqual(pagetest.hostname, 'localhost')


class PageViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


class DbEngine(TestCase):
    def setUp(self):
        os.environ['ENGINE'] = 'SQLite'

    def test_engine_setup(self):
        settings = info()
        self.assertEqual(settings['engine'], 'SQLite')
        self.assertEqual(settings['is_sqlite'], True)


TEST_USERNAME = 'john'
TEST_PASSWORD = 'user1234'
TEST_CITY = 'Copenhagen'
TEST_DOB = '1976-08-27'


class UserTestCase(TestCase):
    from django.contrib import auth

    # SIGNUP TEST 1
    def setUp(self):
        john = MyUser.objects.create(
            username=TEST_USERNAME, city=TEST_CITY, dob=TEST_DOB)
        john.set_password(TEST_PASSWORD)
        john.save()

    # SIGNUP TEST 2
    def test_users_count(self):
        self.assertEqual(MyUser.objects.all().count(), 1)

    # LOGIN TEST
    def test_password(self):
        user = self.auth.authenticate(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.assertIsNotNone(user)
