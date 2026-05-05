from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all().select_related('author', 'genre')
    return render(request, 'library/book_list.html', {'books': books})