from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from library.models import Book


def book_list(request):
    books = Book.objects.all().prefetch_related('authors').select_related('genre')
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})