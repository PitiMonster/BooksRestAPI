from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import IntegrityError

from .models import Book
from .serializers import BookSerializer
from .utils import handle_book_data


def provide_data(request):
    return render(request, 'restAPI/postView.html')

class BooksView(APIView):

    def get(self, request, bookId : int = None):

        # if bookId provided then return specified book
        if bookId is not None:
            book = get_object_or_404(Book, pk=int(bookId))
            response = BookSerializer(book).data
            return Response({'response':response}, status=status.HTTP_200_OK)

        # otherwise return book set depending on other parameters
        all_books = Book.objects.all()

        authors = request.query_params.getlist('author')            # extract all authors
        dates = request.query_params.getlist('published_date')      # extract all dates
        sort = request.query_params.get('sort', 'published_date') # extract sort type

        if authors:
            res_authors = Book.objects.none()

            # combine all authors qss into one qs
            for a in authors:
                curr_author_books = all_books.filter(authors__contains=a)
                res_authors |= curr_author_books

            all_books = res_authors

        if dates:
            res_dates = Book.objects.none()

            # combine all dates qss into one qs
            for d in dates:
                curr_date_books = all_books.filter(year=d)
                res_dates |= curr_date_books

            all_books = res_dates

        if sort == '-published_date':
            all_books = all_books.order_by('-year')

        response = BookSerializer(all_books, many=True).data
        return Response({'response':response}, status=status.HTTP_200_OK)

    def post(self, request):

        # extract data, set type to dict
        data = eval(request.POST.get('data')
                    .replace(': true', ': True')
                    .replace(': false', ': False')
                    )

        try:
            # if data contains list of books
            items = data['items']
        except:
            # if data contains one book
            if isinstance(data, list):
                items = data
            else:
                items = []
                items.append(data)

        for i in items:

            book_data = handle_book_data(i)
      
            book = Book(**book_data)

            try:
                book.save()
            except IntegrityError:
                Book.objects.get(title=book.title).delete()
                book.save()
            except Exception as e:
                response = 'Wrong data provided!'
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = 'Completed successfully'
        return Response(response, status=status.HTTP_201_CREATED)
