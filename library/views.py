from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all().prefetch_related('authors').select_related('genre', 'publisher')
    return render(request, 'library/book_list.html', {'books': books})