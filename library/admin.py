from django.contrib import admin
from .models import User, Author, Publisher, Genre, Book, BookCopy, Reservation, Borrowing

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Reservation)
admin.site.register(Borrowing)