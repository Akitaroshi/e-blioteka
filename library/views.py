from django.shortcuts import render, get_object_or_404  # <--- ПРОВЕРЬ ТУТ
from django.core.paginator import Paginator
from .models import Book, Genre

def book_list(request):
    books_queryset = Book.objects.all().prefetch_related('authors').select_related('genre')
    genres = Genre.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        books_queryset = books_queryset.filter(title__icontains=search_query)

    genre_id = request.GET.get('genre', '')
    if genre_id:
        books_queryset = books_queryset.filter(genre_id=genre_id)

    paginator = Paginator(books_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'genres': genres,
        'search_query': search_query,
        'selected_genre': genre_id,
    }
    return render(request, 'library/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})