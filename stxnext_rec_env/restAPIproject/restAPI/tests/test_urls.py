from django.test import SimpleTestCase
from django.urls import reverse, resolve

from restAPI.views import BooksView, provide_data

class TestUrl(SimpleTestCase):

    def test_books_list_url_resolves(self):
        url = reverse('books_list')
        self.assertEquals(resolve(url).func.view_class, BooksView)

    def test_book_view_url_resolves(self):
        url = reverse('book_view', args=[1])
        self.assertEquals(resolve(url).func.view_class, BooksView)

    def test_provide_data_url_resolves(self):
        url = reverse('provide_data')
        self.assertEquals(resolve(url).func, provide_data)

    def test_add_books_url_resolves(self):
        url = reverse('add_books')
        self.assertEquals(resolve(url).func.view_class, BooksView)