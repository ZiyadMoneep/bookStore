from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView


# Create your tests here.


class HomePageTest(SimpleTestCase):

    def setUp(self):
        url = reverse('pages:home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_templates(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contain_correct_html(self):
        self.assertContains(self.response, 'Homepage')

    def test_homepage_does_not_contain_correct_html(self):
        self.assertNotContains(self.response, 'Hi there!, I am wrong text')

# Check that the name of the view used to resolve '/' matches HomePageView
    def test_homepage_url_resolve_HomePageView(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTest(SimpleTestCase):

    def setUp(self):
        url = reverse('pages:about')
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_templates(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_aboutpage_contain_correct_html(self):
        self.assertContains(self.response, 'About Page')

    def test_aboutpage_does_not_contain_correct_html(self):
        self.assertNotContains(self.response, 'Hi there!, I am wrong text')

    # Check that the name of the view used to resolve '/' matches HomePageView
    def test_aboutpage_url_resolve_HomePageView(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)