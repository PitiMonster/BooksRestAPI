from django.urls import re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    re_path(r'^books/$', views.BooksView.as_view(), name='books_list'),
    re_path(r'^books/(?P<bookId>\d+)/$', views.BooksView.as_view(), name='book_view'),
    re_path(r'^db/$', views.provide_data, name='provide_data'),
    re_path(r'^db/handle_data/$', views.BooksView.as_view(), name='add_books'),
]