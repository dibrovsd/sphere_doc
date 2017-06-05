""" Основной конфигурационный файл. """

import os
from celery.schedules import crontab

# Абсолютный путь к корню установки и путь для хранения загружаемых файлов
BASE_DIR = os.path.abspath('.')

# Хранение и загрузка файлов
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Мб для файлов
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
THUMBNAIL_DUMMY = os.path.join(BASE_DIR, 'sphere/lib/static/thumbnail_dummy.jpeg')

DEBUG = False  # Режим отладки
TESTING = False  # Режим автотестов
PRESERVE_CONTEXT_ON_EXCEPTION = False

# Настройка соединения к БД
SQLALCHEMY_DATABASE_URI = ' '
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Ключ для просаливания всех хэшей
SECRET_KEY = '****************'

# Настройка отправки почты
MAIL_USERNAME = 'robot@sbps.ru'  # Логин
MAIL_PASSWORD = '********'
MAIL_HOST = 'smtp.mail.ru'
MAIL_PORT = 465
MAIL_SSL = True  # Использовать соединение SSL (По умолчанию "True")
MAIL_TLS = False  # Использовать соединение TLS (По умолчанию "False")
MAIL_SUPPRESS_SENDING = False  # Нужно ли подавить фактическую отправку почты (используется для отладки)

# Настройка скачивания почты (задание расписания смотрите в секции Celery - там есть пример под эту ситуацию)
EMAIL_DOWNLOAD = {
    'price_from_supplier': {
        'host': 'imap.mail.ru',
        'port': 993,
        'ssl': True,
        'tls': False,
        'load_email': 'price.vetro18@sbps.ru',  # Адрес почты может отличаться от логина
        'login': 'price.vetro18@sbps.ru',
        'password': '******',
        'folders': ['inbox'],  # Из каких папок выкачиваем почту
    }
}

# Отправка SMS-сообщений
SMS_LOGIN = '********'
SMS_PASSWORD = '********'
SMS_SENDER = '********'
SMS_PROVIDER = 'prostor'
SMS_SUPPRESS_SENDING = True  # Не отправлять сообщения на самом деле (для отладки)

# Настройка менеджера фоновых операций и планировщика (add link)

CELERY_BROKER_URL = 'amqp://sphere_user:*****@localhost:5672/localhost_stoa'  # Через что передаются задания фоновым процессам
CELERY_SEND_TASK_SENT_EVENT = True  # Чтобы можно было смотреть, что делает там celery сейчас
CELERY_SEND_EVENTS = True
CELERYD_CONCURRENCY = 1  # Кол-во одновременных обработчиков
CELERYD_HIJACK_ROOT_LOGGER = False  # Логи мы будем обрабатывать сами, поэтому выключим перехват логов самой celery
CELERY_ACCEPT_CONTENT = ['pickle']  # При передаче в фон, как будем запаковывать аргументы вызова
CELERY_TIMEZONE = 'Europe/Moscow'  # При запуске по расписанию, будем использовать время Москвы

# Настройки расписаний задач, которые выполняются
# Тут нужно перечислить все модули, где лежат задачи к celery
# Иначе они не будут видны планировщику, который сначала загружает все, а только потом работает с этим
CELERY_IMPORTS = (
    'sphere.email.tasks',
    # 'sphere_conf.bps.projects.service.tasks',
    # 'sphere.bps.plugins.tasks.tasks'
)

CELERYBEAT_SCHEDULE = {
    # 'base_recall_notify': {
    #     'task': 'base.tasks.recall_notify',
    #     'schedule': crontab(hour='9-22', minute='*/30'),  # с 9 до 22 каждые 30 минут
    # },
    # 'api_update_stoa_master': {
    #     'task': 'api.tasks.update_stoa_master',
    #     'schedule': crontab(hour=7, minute=0),  # В 7 часов утра
    # },
    # 'api_update_autotrade_catalog': {
    #     'task': 'api.tasks.update_autotrade_catalog',
    #     'schedule': crontab(day_of_week=6, hour=2, minute=0),  # В 2 часов утра в субботу
    # },
    # 'email_load_price_from_supplier': {
    #     'task': 'sphere.email.tasks.load_emails',
    #     'schedule': crontab(hour='9-22', minute='*/30'),
    #     'kwargs': {'load_profile': 'price_from_supplier'},  # При запуске передать в метод аргументы
    # },
}

# Локализация и форматирование
LANGUAGES = {
    'ru': 'Русский',
}
# настройка babel https://pythonhosted.org/Flask-Babel/
BABEL_DEFAULT_LOCALE = 'ru'
BABEL_DEFAULT_TIMEZONE = 'Europe/Moscow'
DATE_FORMAT = 'dd.MM.yyyy'
DATETIME_FORMAT = 'dd.MM.yyyy H:mm'

# Настройка системы кэширования https://pythonhosted.org/Flask-Cache/
CACHE_TYPE = 'memcached'
CACHE_KEY_PREFIX = 'sphere_'
CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']

# Панель отладки (включается только в режиме отладки) https://flask-debugtoolbar.readthedocs.io/en/latest/
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PANELS = [
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
]

# Бренд системы и адрес для обратных ссылок на документы, отправляемых в письмах
BRAND = 'Название'
SITE_URL = 'http://mysite.ru'

# Подключенные приложения
APPS = (
    # Ядро
    ('sphere.lib', '/lib'),
    ('sphere.auth', '/auth'),
    ('sphere.logs', '/logs'),
    ('sphere.email', '/email'),
    ('sphere.sms', '/sms'),
    ('sphere.reports', '/reports'),
    ('sphere.bps', '/bps'),
    ('sphere.bps.plugins.files', '/bps_files'),
    ('sphere.bps.plugins.tasks', '/bps_tasks'),

    ('sphere_conf', None),
    ('sphere_conf.bps.projects.correspondence', '/correspondence'),
)

LOGGING = [
    {
        'logger': 'sphere',
        'level': 'INFO',
        'handler': 'sphere.logs.handlers.SphereHandler',
    }
]

# Все логи отправляем в центральное хранилище, где они будут обработаны по своей логике
LOGGING_SERVER = {
    'project_name': 'sphere_*',
    'url': 'https://logs.myserver.ru/',
    'api_key': '*****'
}

# При запросе этих ресурсов, логи посещения не храним, чтобы не перегружать хранение истории посещения оператора
# не интересных нам адресов, которые мы не хотим фиксировать
LOG_SUPPRESS_ENDPOINT = ['lib.user_notification_new']

# Версия файлов статики, чтобы обновлять стили и скрипты при ее изменении
# Ее изменение генерирует другие ссылки к файлам статики и заставляет браузер не использовать кэш
STATIC_VERSION = 1

# Добавляем кастомные настройки для этой установки
from config_local import *
