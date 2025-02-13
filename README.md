
```python 
email-service/                        # Корневая директория проекта
├── manage.py                         # Скрипт для управления проектом
├── email-service/                    # Основная директория проекта (settings, urls, wsgi)
│   ├── __init__.py
│   ├── settings.py                   # Настройки проекта
│   ├── urls.py                       # Главный URL-роутер
│   ├── wsgi.py
│   └── celery.py                     # Конфигурация Celery
├── emails/                           # Приложение для рассылок
│   ├── migrations/                   # Миграции базы данных
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                      # Админка для моделей
│   ├── apps.py
│   ├── models.py                     # Модели (Subscriber, Mailing, MailingLog)
│   ├── tasks.py                      # Задачи Celery
│   ├── urls.py                       # URL-роуты приложения
│   ├── views.py                      # Логика представлений
│   └── templates/                    # Шаблоны для приложения
│       └── emails/
│           ├── homepages.html        # Главная страница
│           ├── create_email.html     # Модальная форма создания рассылки 
│           ├── email_list.html       # Список рассылок с информация об подписчиках и отправленных письмах и их статусах
│           ├── subscriber_list.html  # Список подписчиков
│           └── email_template.html   # HTML-шаблон для письма
├── static/                           # Статические файлы (CSS, JS, изображения)
│   ├── css/
│   │   └── styles.css                # Кастомные стили для Bootstrap
│   └── js/
│       └── scripts.js                # Скрипты для AJAX и взаимодействия с Bootstrap
└── templates/                        # Глобальные шаблоны
    └── base.html                     # Базовый шаблон для всего проекта
```

