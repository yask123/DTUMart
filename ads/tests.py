from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone

from .models import Year, Branch, Ad
from django.contrib.auth.models import User


class ModelsTests(TestCase):

    def test_creating_ad(self):
        """
        tests creating ad with user, branch and year
        """
        test_user=User.objects.create_user('test_foo', password='test_bar')

        test_year = Year(year = 'III')
        test_branch = Branch(branch = 'COE')
        test_ad = Ad(by=test_user)
        test_ad.title = 'Test title'
        self.assertIs(test_ad.title, 'Test title')

    def test_call_view_denies_anonymous(self):
        """
        tests if anonymous users tries to post an Ad or view the Ad form
        """
        response = self.client.get('/post-ad', follow=True)
        self.assertEqual(str(response.redirect_chain[0][0]), '/post-ad/')
        self.assertEqual(response.redirect_chain[0][1], 301)
        self.assertEqual(str(response.redirect_chain[1][0]), '/loginpage/?next=/post-ad/')

        response = self.client.post('/post-ad', follow=True)
        self.assertEqual(str(response.redirect_chain[0][0]), '/post-ad/')
        self.assertEqual(response.redirect_chain[0][1], 301)
        self.assertEqual(str(response.redirect_chain[1][0]), '/loginpage/?next=/post-ad/')

    def test_call_view_loads(self):
        """
        tests if authenticated user is able to load the form
        """
        self.client.login(username='bhrigu', password='owlcity1995')  # defined in fixture or with factory in setUp()
        response = self.client.get('post-ad/')
        self.assertEqual(response.status_code, 200)

    def test_call_view_fails_blank(self):
        """
        tests if blank data is submitted
        """
        self.client.login(username='bhrigu', password='owlcity1995')
        response = self.client.post('/post-ad', {}) # blank data dictionary
        self.assertEqual(response, "Something went wrong. Couldn't submit your post")
