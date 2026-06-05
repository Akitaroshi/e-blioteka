from django.contrib import admin
from .models import Author, Publisher, Genre, Book, BookCopy, Reservation, Borrowing

admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(BookCopy)
admin.site.register(Reservation)
admin.site.register(Borrowing)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'isbn')

    search_fields = ('title', 'isbn')

    list_filter = ('genre', 'authors')

    ordering = ('title',)

    filter_horizontal = ('authors',)