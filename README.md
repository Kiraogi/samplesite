# Платформа объявлений

Веб-платформа для размещения и управления объявлениями, разработанная на Django.

## Возможности

- Аутентификация и авторизация пользователей
- Управление профилем пользователя
- Размещение и управление объявлениями
- Организация объявлений по категориям
- Функция поиска
- Поддержка пагинации
- Подтверждение email для новых пользователей

## Технический стек

- Python 3.x
- Django
- SQLite (база данных по умолчанию)
- HTML/CSS
- Bootstrap (для стилизации)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Kiraogi/samplesite.git
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
# Для Windows
.venv\Scripts\activate
# Для Unix или MacOS
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции базы данных:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

Приложение будет доступно по адресу `http://localhost:8000` или `http://127.0.0.1:8000`

## Структура проекта

- `main/` - Основная директория приложения
  - `views.py` - Содержит логику обработки запросов
  - `models.py` - Модели базы данных
  - `forms.py` - Определения форм
  - `templates/` - HTML шаблоны
  - `static/` - Статические файлы (CSS, JavaScript, изображения)

## Описание функциональности

### Управление пользователями
- Регистрация пользователей с подтверждением email
- Функционал входа/выхода
- Смена пароля
- Редактирование и удаление профиля

### Управление объявлениями
- Создание, просмотр, обновление и удаление объявлений
- Категоризация объявлений по рубрикам и подрубрикам
- Поиск объявлений по ключевым словам
- Пагинация списка объявлений

- [x] 💡Генерируем идеи (и баги): Разработчик старается, но иногда более продуктивен в генерации багов!
