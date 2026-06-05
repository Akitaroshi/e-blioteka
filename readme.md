Создание и активация виртуального окружения

**Для Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```


### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка базы данных (Миграции)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```
### Наполнение БД
```bash
python manage.py seed_books
```
### Запуск сервера
```bash
python manage.py runserver
```

После запуска сервер будет доступен по адресу: **http://127.0.0.1:8000/**  
Админ-панель: **http://127.0.0.1:8000/admin/**

---
