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

# # Настройка отправки почты
# MAIL_USERNAME = ' '
# MAIL_PASSWORD = ' '
# MAIL_HOST = ' '
# MAIL_PORT =
# MAIL_SUPPRESS_SENDING = False  # Делать вид что отправили, но не отправлять (для отладки)

# Настройка скачивания почты
#
# EMAIL_DOWNLOAD = {
#     'mail@mail.ru': {
#         'host': ' ',
#         'port': ,
#         'login': ' ',
#         'password': ' ',
#         'folders': ['inbox'],
#     },
# }

# Отправка SMS-сообщений
# SMS_LOGIN = ' '
# SMS_PASSWORD = ' '
# SMS_SENDER = ' '
# SMS_PROVIDER = ' '
# SMS_SUPPRESS_SENDING = True  # Делать вид что отправили, но не отправлять (для отладки)

# Настройка менеджера фоновых операций и планировщика (add link)

CELERY_BROKER_URL = 'amqp://****:*******@localhost:5672/localhost'
CELERY_SEND_TASK_SENT_EVENT = True
CELERYD_CONCURRENCY = 1
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_SEND_EVENTS = True
CELERY_TIMEZONE = 'Europe/Moscow'
# CELERY_IMPORTS = (
#     'sphere.email.tasks',
# )

# Задачи для периодического выполнения
# CELERYBEAT_SCHEDULE = {
#     'email_load_emails': {
#         'task': 'sphere.email.tasks.load_emails',
#         'schedule': crontab(hour='9-20', minute='*/10'),
#         'kwargs': {'name': 'sber@sbps.ru'},
#     },
# }

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

# Настройка системы обработки логов
# LOGGING_SERVER = {
#     'project_name': 'sphere_*',
#     'url': 'https://logs.myserver.ru/',
#     'api_key': '*****'
# }

# Переходы по этим адресам не логгировать, чтоб не генерировать мусор
LOG_SUPPRESS_ENDPOINT = []

# Версия файлов статики, чтобы обновлять стили и скрипты при ее изменении
# Ее изменение генерирует другие ссылки к файлам статики и заставляет браузер не использовать кэш
STATIC_VERSION = 1

# Добавляем кастомные настройки для этой установки
from config_local import *
