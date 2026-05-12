from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Таблица 8: Издательство
class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "издательство"
        verbose_name_plural = "Издательства"

# Таблица 9: Жанр
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "Жанры"

# Таблица 3: Автор
class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_year = models.SmallIntegerField(verbose_name='Год рождения')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Страна')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "Авторы"

# Таблица 2: Книга
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название') # Увеличил до 200, 50 маловато
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, verbose_name='Издательство')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
    authors = models.ManyToManyField(Author, verbose_name='Авторы')
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на обложку")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "Книги"

# Таблица 7: Экземпляр книги
class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name='Инвентарный номер')
    condition = models.CharField(max_length=50, verbose_name='Состояние')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')

    def __str__(self):
        return f"{self.book.title} [№{self.inventory_number}]"

    class Meta:
        verbose_name = "экземпляр"
        verbose_name_plural = "Экземпляры книг"

# Таблица 4: Резервация
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('wait', 'В ожидании'),
        ('cancelled', 'Отменена'),
        ('active', 'Выполнена'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    reservation_date = models.DateField(auto_now_add=True, verbose_name='Дата резервации')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wait', verbose_name='Статус')

    def __str__(self):
        return f"Резерв: {self.book.title} для {self.user.username}"

    class Meta:
        verbose_name = "резервация"
        verbose_name_plural = "Резервации"

# Таблица 6: Выдача
class Borrowing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('returned', 'Возвращена'),
        ('overdue', 'Просрочена'),
    )
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, verbose_name='Экземпляр')
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='borrowed_books', on_delete=models.CASCADE, verbose_name='Читатель')
    librarian = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issued_books', on_delete=models.SET_NULL, null=True, verbose_name='Библиотекарь')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
    due_date = models.DateField(verbose_name='Плановая дата возврата')
    return_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата возврата')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')

    def __str__(self):
        return f"Выдача: {self.copy.book.title} ({self.reader.username})"

    class Meta:
        verbose_name = "выдача"
        verbose_name_plural = "Выдачи"