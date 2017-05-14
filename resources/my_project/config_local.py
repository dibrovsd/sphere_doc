"""
Настройки поверх файла config.py, которые находятся не под репозиторием.

Размещаем тут секретную часть (пароли и ключи)
и специфику конкретной установки (production, test, stage, dev)
"""

from config import EMAIL_DOWNLOAD, LOGGING_SERVER

# DEBUG = True  # Режим отладки

# Храним кэш в оперативной памяти
CACHE_TYPE = 'simple'

SECRET_KEY = '***_secret_***'
SQLALCHEMY_DATABASE_URI = 'postgresql://sphere_user:***_secret_***@localhost/sber'
MAIL_PASSWORD = '***_secret_***'
EMAIL_DOWNLOAD['sber@sbps.ru']['password'] = '***_secret_***'
SMS_PASSWORD = '***_secret_***'

# Брокером для асинхронных сообщений используем sqlite в корне
CELERY_BROKER_URL = 'sqla+sqlite:///celerydb.sqlite'

# Логи шлем как dev
LOGGING_SERVER['project_name'] = 'sphere_dev'
LOGGING_SERVER['api_key'] = '***_secret_***'
