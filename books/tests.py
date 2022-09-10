from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Permission
# Create your tests here.
from django.urls import reverse, resolve

from books.models import Book, Review
from books.views import BookListView, BookDetailView


class BookTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(  # new
            username='reviewZiyad',
            email='reviewZiyad@email.com',
            password='test123'
        )
        self.special_permission = Permission.objects.get(codename='special_status')

        self.book = Book.objects.create(
            title='Harry potter',
            author='Ziyad',
            price='39.00',
        )
        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='An excellent review',
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry potter')
        self.assertEqual(f'{self.book.author}', 'Ziyad')
        self.assertEqual(f'{self.book.price}', '39.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='reviewZiyad@email.com', password='test123')
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewZiyad@email.com', password='test123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'An excellent review')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_list_view(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry potter')
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertNotContains(response, 'Hi there!, I am wrong text')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'An excellent review')  # new
        self.assertTemplateUsed(response, 'books/book_detail.html')

    # Check that the name of the view used to resolve '/' matches HomePageView
    def test_bookList_url_resolve_BookListView(self):
        view = resolve('/books/')
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)
