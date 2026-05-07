from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Book, Genre

def book_list(request):
    # 1. Получаем все книги изначально
    books_queryset = Book.objects.all().prefetch_related('authors').select_related('genre')
    genres = Genre.objects.all() # Для выпадающего списка фильтров

    # 2. Логика ПОИСКА
    search_query = request.GET.get('search', '')
    if search_query:
        books_queryset = books_queryset.filter(title__icontains=search_query)

    # 3. Логика ФИЛЬТРАЦИИ по жанру
    genre_id = request.GET.get('genre', '')
    if genre_id:
        books_queryset = books_queryset.filter(genre_id=genre_id)

    # 4. Логика ПАГИНАЦИИ (по 6 книг на странице)
    paginator = Paginator(books_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,      # Теперь в шаблон отдаем объект страницы, а не весь список
        'genres': genres,
        'search_query': search_query,
        'selected_genre': genre_id,
    }
    return render(request, 'library/book_list.html', context)