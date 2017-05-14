Конфигурация системы
====================================

Данный раздел описывает возможные значения конфигурационного файла ``config.py`` который размещается
в корневом разделе вашей конфигурации.

Опции Flask-framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Это базовые опции системы, которые описывают

- Время неактивности сессии, после которой нужно снова входить в систему
- Максимальный размер контента, который система отдает или принимает
- Работает ли сервер в режиме тестирования или отладки

И прочие опции, которые задают режим работы сервера.
Обязательно следует указать опцию ``SECRET_KEY``, которую уставить в случайными символами не менее 50 символов.

http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values


Опции SQLAlchemy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Настройка соединения с базами данных. Есть соединение по умолчанию, через которое работает система.
Также, можно задавать дополнительные соединения к другим базам и системам для интеграции,
выполнеия запросов к другим базам данных других систем, построения отчетов и так далее
http://flask-sqlalchemy.pocoo.org/2.1/config/

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = 'postgresql://sphere_user:*****@localhost/stoa_sqla'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Для снижения нагрузки. Не генерирует события SQLA
    SQLALCHEMY_BINDS = {
        'reports': 'postgresql://sphere_reports:*****@localhost/stoa_sqla',  # Система отчетов работает через отдельную ограниченную учетную запись
        'reports_mssql': 'mssql://sphere_reports:*****@localhost/stoa_sqla',  # Описание отдельного источника данных к другой базе данных
    }

Опции Celery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Эта часть отвечает за выполнения различных операций в фоновом режиме и по расписанию с какой-то периодичностью.
Это может быть полезно, если есть какая-то длительная операция, которую можно отложить на потом, чтобы не заставлять пользователя ждать.
И есть операции напоминания о просроченных задачах, истекающих строках и автоматических операциях синхронизации, которые нужно выполнять время от времени
http://docs.celeryproject.org/en/latest/userguide/configuration.html

.. code-block:: python

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
        'sphere_conf.bps.projects.service.tasks',
        'sphere.bps.plugins.tasks.tasks'
    )

    from celery.schedules import crontab

    CELERYBEAT_SCHEDULE = {
        'base_recall_notify': {
            'task': 'base.tasks.recall_notify',
            'schedule': crontab(hour='9-22', minute='*/30'),  # с 9 до 22 каждые 30 минут
        },
        'api_update_stoa_master': {
            'task': 'api.tasks.update_stoa_master',
            'schedule': crontab(hour=7, minute=0),  # В 7 часов утра
        },
        'api_update_autotrade_catalog': {
            'task': 'api.tasks.update_autotrade_catalog',
            'schedule': crontab(day_of_week=6, hour=2, minute=0),  # В 2 часов утра в субботу
        },
        'email_load_price_from_supplier': {
            'task': 'sphere.email.tasks.load_emails',
            'schedule': crontab(hour='9-22', minute='*/30'),
            'kwargs': {'load_profile': 'price_from_supplier'},  # При запуске передать в метод аргументы
        },
    }

Опции Flask-Babel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Эта часть отвечает за отображение интерфейса для разных языков с возможностью переключения между ними
https://pythonhosted.org/Flask-Babel/ но обычно используется такой набор:

.. code-block:: python

    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Moscow'
    DATE_FORMAT = 'dd.MM.yyyy'  # Формат по умолчанию для дат
    DATETIME_FORMAT = 'dd.MM.yyyy H:mm' # Формат по умолчанию для дат с временем

Опции Flask-Cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Настройки хранилища, в которое можно положить какие-то данные, чтобы не вычислять их при каждом запросе.
Это может сильно ускорить работу системы.

https://pythonhosted.org/Flask-Cache/#configuring-flask-cache
Приведем пример настройки для использования через memcached

.. code-block:: python

    CACHE_TYPE = 'memcached'
    CACHE_KEY_PREFIX = 'sphere_'  # Чтобы не путались данные от разных систем
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']  # Серверов может быть несколько

Опции Flask-DebugToolbar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Этот модуль для работы системы не нужен, но он существенно облегчает понимание того, что происходит в системе внутри.
Имеет смысл для запуска системы в отладочном режиме. Там есть возможность просмотра какие запросы к базе данных
выполняются и где, какие текущие опции конфигурации, и т.п.
Активируется только при работе сервера в режиме отладки ``DEBUG = True``

https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration
Пример настройки

.. code-block:: python

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

Опции СфераBPMS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``USER_SECURITY`` Настройки безопасности операторов. Опциональный параметр.
    Но если указан, то нужно указать все параметры внутри него

.. code-block:: python

    USER_SECURITY = {
        'password_expire_days': 30,  # Срок жизни пароля в днях, после которого его нужно менять
        # Правило проверки качества пароля
        'password_validate': {
            'pattern': re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'),  # Шаблон
            'message': 'Как минимум, одна буква и цифра, 6 символов'  # Сообщение, если не подошел
        },
        'save_login_location': True,  # Сохранять местоположение при входе или нет
    }

- ``APPS`` Список установленных приложений в виде пути к пакету с приложением и url_prefix а, в которое монтируется приложение.
    Приложения можно подключать как из ядра (стандартная поставка), так и разрабатывать свои (смотри раздел "Приложение для СфераBPS" TBD: Описать)

.. code-block:: python

    APPS = (
        ('base', None),  # При отсутствии url_prefix, приложение монтируется в корневой url https://domain.com/
        ('sphere.lib', '/lib'),  # Общий функционал для всех приложений, в т.ч. и ядра
        ('sphere.auth', '/auth'),  # Приложение аутентификации. Операции с пользователем системы
        ('sphere.logs', '/logs'),  # Аггрегатор логов
        ('sphere.email', '/email'),  # Скачивание и отправка и Email, в том числе и универсальный графический интерфейс для генерации письма
        ('sphere.sms', '/sms'),  # Отправка SMS, в том числе и GUI
        ('sphere.reports', '/reports'),  # Приложение генерации отчетов, в том числе и по другим базам данных
        ('sphere.pdf_maker', '/pdf_maker'),  # Генератор и редактор pdf

        ('sphere.bps', '/bps'),  # Приложениие, которое управляет проектами BPS
        ('sphere.bps.plugins.files', '/bps_files'),  # Плагин файлов BPS
        ('sphere.bps.plugins.tasks', '/bps_tasks'),  # Плагин задач BPS

        # Проект BPS является приложением и может содержать в себе произвольный функционал, не охватываемый ядром BPS
        ('sphere_conf.bps.projects.client', '/client'),

        # Дополнительные приложения, которые можно писать и переносить между конфигурациями
        ('sphere_conf', '/sphere_conf'),  # Обязательное приложение уровня конфигурации. Содержит логику, которая поставляет данные в ядро
        ('api', '/api'),  # Самописное приложение для примера
    )

- Работа с почтой (отправка и скачивание)

.. code-block:: python

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

- Настройка СМС - сервиса (Необязательные настройки, оставьте закоментированными если не хотите пользоваться СМС - сервисами)

.. code-block:: python

    SMS_LOGIN = '********'
    SMS_PASSWORD = '********'
    SMS_SENDER = '********'
    SMS_PROVIDER = 'prostor'
    SMS_SUPPRESS_SENDING = True  # Не отправлять сообщения на самом деле (для отладки)

.. note::

    В качестве СМС провайдера система "Сфера" может использовать провайдеров `"Простор" <https://prostor-sms.ru>`_ или `"Smsc" <https://smsc.ru>`_

Логгирование
^^^^^^^^^^^^^^^^
Настройка `Logging handlers <https://docs.python.org/2/library/logging.handlers.html>`_:

.. code-block:: python

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

Прочие опции
^^^^^^^^^^^^^^^^

- ``BRAND = 'Ваша компания'`` Бренд компании, который показывается в навигационной панели и в подписи к вкладкам браузера.

- ``SITE_URL = 'http://mysite.ru'`` URL текущей установки для генерации ссылок на открытие карточек системы в email-сообщениях.

- ``BASE_DIR = os.path.abspath('.')`` Абсолютный путь, от которого далее строятся все относительные пути

- ``MEDIA_DIR = os.path.join(BASE_DIR, 'media')`` Абсолютный путь к директории, где лежат файлы, которые появляются в процессе работы системы (сканы, которые загружают пользователи, скачиваемые системой письма и так далее).

- ``THUMBNAIL_DUMMY = os.path.join(BASE_DIR, 'sphere/lib/static/thumbnail_dummy.jpeg')`` Абсолютный путь к изображению - заглушке, которая появляется, если preview файла невозможно или еще не подготовлено

- ``TEMPLATE_FOLDERS`` Опциональный аргумент. Используется, если вам нужно подменить какие-либо шаблоны из ядра системы, интерфейса администратора, чтобы на всех страницах был какой-то одинаковый контент, например

- ``STATIC_VERSION = 1`` Версия скриптов и стилей, которая будет обновляться в браузере клиентов. Вы можете выставлять ее вручную, или воспользоваться вот таким автоматическим вариантом, который зависит от номера ревизии и будет при кажой новой ревизии выставлять новую версию автоматически

.. code-block:: python

    from git import Repo
    repo = Repo(BASE_DIR)

    STATIC_VERSION = repo.head.object.hexsha


Конфигурация конкретной установки системы
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Одна и та же система часто устанавливается в нескольких местах:

- ``Production`` Рабочая версия системы, на которой обычно и работают операторы
- ``Stage`` Стабильная версия для проверки функционала заказчиком, к выкладыванию на Production.
- ``Development`` Самый новый функционал (не стабильный и не проверенный до конца). Используется для внутреннго тестирования разработчиками

И бывает нужно немного скорректировать настройки (название БД, брокер асиохронных операций) для установки,
но без внесения изменений в код системы.

Для этого предусмотрена возможность подмены переменных конфигурации без внесения изменения в код системы (репозиторий)

Нужно рядом с файлом ``config.py`` разместить файл ``config_local.py``, который находится не под управлением системы контроля версий
В файл ``config.py`` в самой нижней его части (это важно) добавить и часть опций разместить в нем.

.. code-block:: python

    from config_local import *

Эти опции перекрывают опции конфигурации, но при этом, без внесения изменений в код системы.
