# Email Service

## Описание

**Email Service** — это Django-приложение для создания и управления email-рассылками. Оно позволяет пользователям настраивать рассылки, отслеживать их статус и вести учет подписчиков.

## Функциональность

- Управление подписчиками (удаление и импорт из CSV)
- Создание и отправка email-рассылок
- Использование Celery для асинхронной отправки писем
- Поддержка шаблонов для писем
- Логирование отправки и открытия писем

## Структура проекта

```
email-service/                        # Корневая директория проекта
├── manage.py                         # Скрипт для управления проектом
├── email-service/                    # Основная директория проекта (settings, urls, wsgi)
│   ├── settings.py                   # Настройки проекта
│   ├── urls.py                       # Главный URL-роутер
│   └── celery.py                     # Конфигурация Celery
├── emails/                           # Приложение для рассылок
│   ├── admin.py                      # Админка для моделей
│   ├── models.py                     # Модели (Subscriber, Mailing, MailingLog)
│   ├── tasks.py                      # Задачи Celery
│   ├── forms.py
│   ├── urls.py                       # URL-роуты приложения
│   ├── views.py                      # Логика представлений
│   └── templates/                    # Шаблоны для приложения
│       ├── emails/
│       │   ├── homepages.html        # Главная страница
│       │   ├── create_email.html     # Форма создания рассылки
│       │   ├── email_list.html       # Список рассылок
│       │   └── subscriber_list.html  # Список подписчиков
│       └── mailing/
│           ├── templates_email-2.html
│           └── templates_email.html
├── static/                           # Статические файлы
│   └── js/
│       └── scripts.js                # Скрипты для AJAX и Bootstrap
├── templates/                        # Глобальные шаблоны
│   └── base.html                     # Базовый шаблон
├── README.md
├── .env.example                      # Пример файла переменных окружения
├── .gitignore                         # Игнорируемые файлы
└── requirements.txt                   # Список зависимостей проекта
```

## Установка и настройка

### 1. Клонирование репозитория

```sh
git clone https://github.com/your-repo/email-service.git
cd email-service
```

### 2. Создание виртуального окружения

Для **Python 2.7**:
```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate  # Для macOS / Linux
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```sh
cp .env.example .env
nano .env  # или используйте любой текстовый редактор
```

### 5. Применение миграций и создание суперпользователя
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Запуск статики
```sh
python manage.py collectstatic
```

### 7. Запуск проекта
```sh
python manage.py runserver
```

## Установка и запуск Redis

### macOS (Homebrew)
```sh
brew install redis
brew services start redis
```

### Ubuntu/Debian
```sh
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis
sudo systemctl start redis
```

### Windows
1. Скачайте [Redis для Windows](https://github.com/microsoftarchive/redis/releases).
2. Разархивируйте и запустите `redis-server.exe`.

## Запуск Celery
```sh
celery -A email-service worker --loglevel=info
```

## Важные библиотеки

- **Django** – веб-фреймворк для серверной части приложения.
- **Celery** – управление задачами для асинхронной отправки email-рассылок.
- **Redis** – брокер сообщений для Celery.
- **pandas** – анализ данных.
- **numpy** – научные вычисления.

## Используемые технологии

- **Python/Django** — Backend
- **Celery + Redis** — Асинхронные задачи
- **Bootstrap + jQuery** — UI
- **SQLite/PostgreSQL** — База данных
