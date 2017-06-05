"""
Настройки поверх файла config.py, которые находятся не под репозиторием.

Размещаем тут секретную часть (пароли и ключи)
и специфику конкретной установки (production, test, stage, dev)
"""

from config import EMAIL_DOWNLOAD, LOGGING_SERVER

# Храним кэш в оперативной памяти
CACHE_TYPE = 'simple'

SECRET_KEY = '***_replace_me_***'
SQLALCHEMY_DATABASE_URI = 'postgresql://sphere_user:******@localhost/my_project'
MAIL_PASSWORD = '***_secret_***'
EMAIL_DOWNLOAD['price_from_supplier']['password'] = '***_replace_me_***'
SMS_PASSWORD = '***_replace_me_***'

# Брокером для асинхронных сообщений используем sqlite в корне
CELERY_BROKER_URL = 'amqp://sphere_user:*********@localhost:5672/localhost_my_project'

# Логи шлем как dev
LOGGING_SERVER['project_name'] = 'sphere_dev'
LOGGING_SERVER['api_key'] = '***_replace_me_***'
