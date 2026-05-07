from django.db import models
from django.contrib.auth.models import AbstractUser

# Таблица 1: Пользователь
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('librarian', 'Библиотекарь'),
        ('reader', 'Читатель'),
    )
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader', verbose_name='Роль')

# Таблица 8: Издательство
class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')
    def __str__(self):
        return self.name
# Таблица 9: Жанр
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

# Таблица 3: Автор
class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_year = models.SmallIntegerField(verbose_name='Год рождения')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Страна')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Таблица 2: Книга (включая связь с авторами - Таблица 5)
class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, verbose_name='Издательство')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
    authors = models.ManyToManyField(Author, verbose_name='Авторы') # Связь Автор-Книга
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на обложку")
    def __str__(self):
        return self.title

# Таблица 7: Экземпляр книги
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name='Инвентарный номер')
    condition = models.CharField(max_length=50, verbose_name='Состояние')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')

# Таблица 4: Резервация
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('wait', 'В ожидании'),
        ('cancelled', 'Отменена'),
        ('active', 'Выполнена'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    reservation_date = models.DateField(auto_now_add=True, verbose_name='Дата резервации')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wait', verbose_name='Статус')

# Таблица 6: Выдача
class Borrowing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('returned', 'Возвращена'),
        ('overdue', 'Просрочена'),
    )
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, verbose_name='Экземпляр')
    reader = models.ForeignKey(User, related_name='borrowed_books', on_delete=models.CASCADE, verbose_name='Читатель')
    librarian = models.ForeignKey(User, related_name='issued_books', on_delete=models.SET_NULL, null=True, verbose_name='Библиотекарь')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
    due_date = models.DateField(verbose_name='Плановая дата возврата')
    return_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата возврата')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')