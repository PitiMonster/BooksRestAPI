from django.test import TestCase, Client
from django.urls import reverse
import json

from restAPI.models import Book
from restAPI.serializers import BookSerializer
from restAPI.utils import create_query_url

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.books_list_url = reverse('books_list')
        self.book_view_url = reverse('book_view', args=[1])
        self.add_books_url = reverse('add_books')

        self.test_book1 = Book(
                                title='test1', 
                                published_date='2020-10-10',
                                authors=['test1','test2'], year=2020
                               )

        self.test_book2 = Book(
                                title='test2',
                                published_date='2010-10-10',
                                authors=['test2','test3'], year=2010
                               )                       
        
        self.test_book1.save()
        self.test_book2.save()

    def test_books_list_GET(self):
        response = self.client.get(self.books_list_url)
        self.assertEquals(response.status_code, 200)

    def test_books_list_ordering_GET(self):
        asc_url = create_query_url(self.books_list_url, [('sort','published_date')])
        desc_url = create_query_url(self.books_list_url, [('sort','-published_date')])

        # if order by published_date ascending
        response = self.client.get(asc_url)
        first_book_published_date = json.loads(response.content)['response'][0]['published_date']
        self.assertEquals(first_book_published_date, '2010-10-10')

        # if order by published_date descending
        response = self.client.get(desc_url)
        first_book_published_date = json.loads(response.content)['response'][0]['published_date']
        self.assertEquals(first_book_published_date, '2020-10-10')

    def test_books_list_year_filtering_GET(self):
        # one year provided
        url = create_query_url(self.books_list_url, [('published_date','2010')])
        response = self.client.get(url)
        books = json.loads(response.content)['response']
        self.assertEquals(len(books), 1)
        self.assertEquals(books[0]['published_date'], '2010-10-10')

        # two years provided
        url = create_query_url(self.books_list_url, [('published_date','2010'), ('published_date','2020')])
        response = self.client.get(url)
        books = json.loads(response.content)['response']
        self.assertEquals(len(books), 2)

    def test_books_list_author_filtering_GET(self):

        # one unique author provided
        url = create_query_url(self.books_list_url, [('author','test1')])
        response = self.client.get(url)
        books = json.loads(response.content)['response']
        self.assertEquals(len(books), 1)
        self.assertEquals(books[0]['authors'], "['test1', 'test2']")

        # two unique authors provided
        url = create_query_url(self.books_list_url, [('author','test1'), ('author','test3')])
        response = self.client.get(url)
        books = json.loads(response.content)['response']
        self.assertEquals(len(books), 2)

        # one common author provided
        url = create_query_url(self.books_list_url, [('author','test2')])
        response = self.client.get(url)
        books = json.loads(response.content)['response']
        self.assertEquals(len(books), 2)

    def test_book_view_GET(self):
        # book exists
        response = self.client.get(self.book_view_url)
        self.assertEquals(response.status_code, 200)

        # book does not exist
        response = self.client.get(reverse('book_view', args=[10]))
        self.assertEquals(response.status_code, 404)