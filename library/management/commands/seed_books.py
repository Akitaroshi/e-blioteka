from django.core.management.base import BaseCommand

from library.models import Author, Book, BookCopy, Genre, Publisher


BOOK_SEEDS = [
    {
        "title": "Мастер и Маргарита",
        "isbn": "9785000000001",
        "description": "Роман о добре, зле и свободе выбора в Москве 1930-х.",
        "genre": "Классика",
        "publisher": "АСТ",
        "authors": [{"first_name": "Михаил", "last_name": "Булгаков", "birth_year": 1891, "country": "Россия"}],
        "image_url": "https://covers.openlibrary.org/b/id/8231996-L.jpg",
    },
    {
        "title": "Преступление и наказание",
        "isbn": "9785000000002",
        "description": "Психологический роман о вине и нравственном возрождении.",
        "genre": "Классика",
        "publisher": "Эксмо",
        "authors": [{"first_name": "Федор", "last_name": "Достоевский", "birth_year": 1821, "country": "Россия"}],
        "image_url": "https://covers.openlibrary.org/b/id/7222246-L.jpg",
    },
    {
        "title": "Война и мир",
        "isbn": "9785000000003",
        "description": "Эпопея о судьбах людей на фоне наполеоновских войн.",
        "genre": "Классика",
        "publisher": "Азбука",
        "authors": [{"first_name": "Лев", "last_name": "Толстой", "birth_year": 1828, "country": "Россия"}],
        "image_url": "https://covers.openlibrary.org/b/id/8235116-L.jpg",
    },
    {
        "title": "Евгений Онегин",
        "isbn": "9785000000004",
        "description": "Роман в стихах о любви, времени и внутреннем взрослении.",
        "genre": "Поэзия",
        "publisher": "Просвещение",
        "authors": [{"first_name": "Александр", "last_name": "Пушкин", "birth_year": 1799, "country": "Россия"}],
        "image_url": "https://covers.openlibrary.org/b/id/10521273-L.jpg",
    },
    {
        "title": "Гарри Поттер и философский камень",
        "isbn": "9785000000005",
        "description": "История мальчика, который узнал, что он волшебник.",
        "genre": "Фэнтези",
        "publisher": "Росмэн",
        "authors": [{"first_name": "Джоан", "last_name": "Роулинг", "birth_year": 1965, "country": "Великобритания"}],
        "image_url": "https://covers.openlibrary.org/b/id/7884866-L.jpg",
    },
    {
        "title": "Властелин колец: Братство кольца",
        "isbn": "9785000000006",
        "description": "Начало великого путешествия по Средиземью.",
        "genre": "Фэнтези",
        "publisher": "АСТ",
        "authors": [{"first_name": "Джон", "last_name": "Толкин", "birth_year": 1892, "country": "Великобритания"}],
        "image_url": "https://covers.openlibrary.org/b/id/8231856-L.jpg",
    },
    {
        "title": "1984",
        "isbn": "9785000000007",
        "description": "Антиутопия о тотальном контроле и подавлении личности.",
        "genre": "Антиутопия",
        "publisher": "Эксмо",
        "authors": [{"first_name": "Джордж", "last_name": "Оруэлл", "birth_year": 1903, "country": "Великобритания"}],
        "image_url": "https://covers.openlibrary.org/b/id/153541-L.jpg",
    },
    {
        "title": "451 градус по Фаренгейту",
        "isbn": "9785000000008",
        "description": "Мир, в котором книги объявлены вне закона.",
        "genre": "Антиутопия",
        "publisher": "Азбука",
        "authors": [{"first_name": "Рэй", "last_name": "Брэдбери", "birth_year": 1920, "country": "США"}],
        "image_url": "https://covers.openlibrary.org/b/id/9259256-L.jpg",
    },
    {
        "title": "Убийство в Восточном экспрессе",
        "isbn": "9785000000009",
        "description": "Классический детектив о загадочном убийстве в поезде.",
        "genre": "Детектив",
        "publisher": "АСТ",
        "authors": [{"first_name": "Агата", "last_name": "Кристи", "birth_year": 1890, "country": "Великобритания"}],
        "image_url": "https://covers.openlibrary.org/b/id/8226191-L.jpg",
    },
    {
        "title": "Шерлок Холмс: Этюд в багровых тонах",
        "isbn": "9785000000010",
        "description": "Первая история о знаменитом сыщике Шерлоке Холмсе.",
        "genre": "Детектив",
        "publisher": "Азбука",
        "authors": [{"first_name": "Артур", "last_name": "Конан Дойл", "birth_year": 1859, "country": "Великобритания"}],
        "image_url": "https://covers.openlibrary.org/b/id/8108691-L.jpg",
    },
    {
        "title": "Три товарища",
        "isbn": "9785000000011",
        "description": "История дружбы, любви и потерь в послевоенной Германии.",
        "genre": "Роман",
        "publisher": "Эксмо",
        "authors": [{"first_name": "Эрих", "last_name": "Ремарк", "birth_year": 1898, "country": "Германия"}],
        "image_url": "https://covers.openlibrary.org/b/id/11153274-L.jpg",
    },
    {
        "title": "Цветы для Элджернона",
        "isbn": "9785000000012",
        "description": "Трогательный роман о разуме, человечности и выборе.",
        "genre": "Научная фантастика",
        "publisher": "АСТ",
        "authors": [{"first_name": "Дэниел", "last_name": "Киз", "birth_year": 1927, "country": "США"}],
        "image_url": "https://covers.openlibrary.org/b/id/10710768-L.jpg",
    },
    {
        "title": "Дюна",
        "isbn": "9785000000013",
        "description": "Космическая сага о власти, религии и экологии пустынной планеты.",
        "genre": "Научная фантастика",
        "publisher": "Азбука",
        "authors": [{"first_name": "Фрэнк", "last_name": "Герберт", "birth_year": 1920, "country": "США"}],
        "image_url": "https://covers.openlibrary.org/b/id/8107896-L.jpg",
    },
    {
        "title": "Алхимик",
        "isbn": "9785000000014",
        "description": "Притча о пути к своей мечте и поиске смысла.",
        "genre": "Роман",
        "publisher": "Эксмо",
        "authors": [{"first_name": "Пауло", "last_name": "Коэльо", "birth_year": 1947, "country": "Бразилия"}],
        "image_url": "https://covers.openlibrary.org/b/id/9254624-L.jpg",
    },
    {
        "title": "Тихий Дон",
        "isbn": "9785000000015",
        "description": "Эпическое полотно о судьбе донского казачества в эпоху перемен.",
        "genre": "Классика",
        "publisher": "Просвещение",
        "authors": [{"first_name": "Михаил", "last_name": "Шолохов", "birth_year": 1905, "country": "Россия"}],
        "image_url": "https://covers.openlibrary.org/b/id/10853039-L.jpg",
    },
]


class Command(BaseCommand):
    help = "Добавляет 15 книг в библиотеку с жанрами, авторами и экземплярами."

    def handle(self, *args, **options):
        created_books = 0
        created_copies = 0

        for idx, seed in enumerate(BOOK_SEEDS, start=1):
            genre, _ = Genre.objects.get_or_create(name=seed["genre"])
            publisher, _ = Publisher.objects.get_or_create(name=seed["publisher"])

            book, was_created = Book.objects.get_or_create(
                isbn=seed["isbn"],
                defaults={
                    "title": seed["title"],
                    "description": seed["description"],
                    "genre": genre,
                    "publisher": publisher,
                    "image_url": seed["image_url"],
                },
            )

            if was_created:
                created_books += 1
            else:
                changed = False
                if book.title != seed["title"]:
                    book.title = seed["title"]
                    changed = True
                if not book.description:
                    book.description = seed["description"]
                    changed = True
                if book.genre_id != genre.id:
                    book.genre = genre
                    changed = True
                if book.publisher_id != publisher.id:
                    book.publisher = publisher
                    changed = True
                if not book.image_url:
                    book.image_url = seed["image_url"]
                    changed = True
                if changed:
                    book.save()

            author_objs = []
            for author_seed in seed["authors"]:
                author, _ = Author.objects.get_or_create(
                    first_name=author_seed["first_name"],
                    last_name=author_seed["last_name"],
                    defaults={
                        "birth_year": author_seed["birth_year"],
                        "country": author_seed["country"],
                    },
                )
                author_objs.append(author)

            book.authors.set(author_objs)

            inventory_number = f"SEED-{idx:03d}"
            _, copy_created = BookCopy.objects.get_or_create(
                inventory_number=inventory_number,
                defaults={
                    "book": book,
                    "condition": "Отличное",
                    "is_available": idx % 4 != 0,
                },
            )
            if copy_created:
                created_copies += 1

        self.stdout.write(self.style.SUCCESS(f"Книги: создано {created_books}, всего сидов {len(BOOK_SEEDS)}."))
        self.stdout.write(self.style.SUCCESS(f"Экземпляры: создано {created_copies}."))
