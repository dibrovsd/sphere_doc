Установка системы
==========================

Раздел описывает установку на сервер зависимостей и самой системы. Процесс описывается в консольном режиме через терминал или его эмулятор
из-под учетной записи супер-пользователя (root)

Установка программного обеспечения
------------------------------------
Выполним команды

.. code-block:: bash

    apt-get update
    apt-get install gcc make build-essential git supervisor tmux  \
        postgresql libpq-dev libaio-dev libssl-dev libffi-dev \
        libxml2-dev libxslt-dev \
        cython3 python-dev python3-dev python-pip python-virtualenv python-pycurl \
        gnutls-dev curl libcurl4-gnutls-dev \
        libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev \
        libsasl2-dev \
        uwsgi uwsgi-plugin-python3 \
        memcached libmemcached-dev nginx rabbitmq-server \
        imagemagick libmagickwand-dev libmagickcore-dev

Установка виртуального окружения
------------------------------------
Виртуальное окружение, это виртуальный контейнер, куда устанавливаются пакеты python.
Мы не рекомендуем устанавливать их в систему, для того, чтобы можно было на одном сервере установить несколько систем, которые требуют различный набор библиотек
и, возможно, различные их версии. Чтобы избежать конфликтов, зависимости лучше изолировать друг от друга, устанавливая их в виртуальные окружения.
Переходим под учетную запись пользователя, из-под которой будет работать сервер (в данном случае, "www") и устанавливаем все от имени этого пользователя.

Предварительно нужно взять файл :download:`requirements.txt </files/requirements.txt>` с описанием python - библиотек, которые нужно установить и загрузить его в корень домашней директории www

.. code-block:: bash

    su www
    cd

    virtualenv ~/.virtualenv/sphere --python=python3
    source ~/.virtualenv/sphere/bin/activate
    pip install -U pip
    pip install -U setuptools
    pip install -r ~/requirements.txt

Инициализация базы данных
------------------------------------

Для этого, находясь под учетной записью root, перейдем к пользователю postgresql и создадим пользователя, под которым приложение будет соединяться и базу данных, в которой будут храниться данные приложения

.. code-block:: bash

    su postgres
    psql

    CREATE USER sphere_user PASSWORD '******';


    create database my_project;

    alter database my_project owner to my_project;
    alter database my_project set timezone = 'UTC';
    alter database my_project set default_transaction_isolation = 'read committed';
    alter database my_project set client_encoding = 'UTF8';

    \q


Создание базового приложения
-------------------------------

Скачайте минимальный :download:`шаблон</files/my_project.tar>` системы со всеми настройками и разархивируйте
в директорию my_project.

.. note::

    Директория может быть любой. Но дальнейшее описание конфигурации будет, исходя из того,
    что вы распаковали систему в /home/www/my_project

Внутри директории /home/www/my_project сделайте `символьную ссылку <https://ru.wikipedia.org/wiki/Символьная_ссылка>`_ с именем /home/www/my_project/sphere на ядро Сфера BPMS

Редактирование конфигурации.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Откроем файл ``nano /home/www/my_project/conf_local.py``
и в переменной SQLALCHEMY_DATABASE_URI запишем пароль к базе данных, который мы задали, создавая пользователя базы данных sphere_user

``SQLALCHEMY_DATABASE_URI = 'postgresql://sphere_user:****@localhost/my_project'``
Мы рекомендуем опции, которые содержат пароли не хранить в репозитории (файл config.py находится в репозитории),
а размещать в секции, которая находится вне его. В случае, если кто-то получит не санкционированный доступ к репозиторию с системой,
он не сможет выполнить подключиться к данным.

Тестовый запуск
------------------------------------------

На этом шаге, у нас есть пустая база данных, которая не содержит таблиц,
стартовый набор файлов конфигурации, скриптов и шаблонов.
Нам нужно создать в базе данных нужную структуру таблиц (пока пустых)
и создать первого пользователя с правами администратора.
И попробовать запустить систему в режиме отладки через встроенный отладочный сервер.

Перейдем в директорию /home/www/my_project, куда мы положили наш проект.

Для управления системой, используется файл **manage.py**, запуская который с различными опциями, мы можем выполнять
с системой различные действия.
Для просмотра доступных действий, выполните этот файл ``./manage.py``

Создаем структуру таблиц
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Выполним команду ``./manage.py db upgrade``.
После этого, в базе данных будет создана необходимая стркутура.

Создадим учетную запись супер-пользователя
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Это пользователь, который сможет войти в систему через браузер, имеет по умолчанию полный доступ ко всем разделам системы.
``./manage.py create_superuser <e-mail> <пароль>``

Запустим систему
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``./manage.py runserver -h 0.0.0.0``
Опция -h разрешит подключиться к отладочному серверу снаружи сервера. По умолчанию, предполагается, что отладочный сервер запускается на машине разработчика.
Поэтому, чтобы открыть систему в браузере снаружи сервера, нужно разрешить ему принимать подключения извне.

Далее, в браузере зайдите на *IP_СЕРВЕРА:5000* и, если всё успешно, вы увидите окно приветствия системы.
Вы можете выполнить вход в нее, используя параметры, которые вы использовали в команде "create_superuser"

Итак, мы убедились, что сделали все правильно и система работает, кнопки нажимаются, вход производится.
Но система работает, пока у вас запущен отладочный сервер, который вы запускаете вручную.
К тому же, система не может в таком режиме выдерживать больших нагрузок, потому что отладочный сервер может обслужить только один запрос
за раз и дает большую нагрузку на систему, потому что хранит в себе много информации, полезной для разработчика системы, но совсем не нужной для оператора, который просто работает в системе.

Запуск в рабочем режиме
------------------------------------------

К этому шагу, у нас есть минимальная система, мы создали в базе данных таблицы и убедились,
что система запускается и работает.

Сейчас мы настроим систему, чтобы она автоматически запускалась вместе с сервером,
могла одновременно обрабатывать несколько запросов от пользователей и запустим менеджеры фоновых операций

Запустим систему через uWSGI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Этот сервер будет принимать запросы от WEB-сервера nginx (о нем чуть ниже), обрабатывать их и отдавать ему ответ.

Для этого, создадим файл конфигурации ``nano /etc/uwsgi/apps-available/my_project.ini``

.. code-block:: ini

    [uwsgi]
    plugins = python3
    chdir = /home/www/my_project
    virtualenv = /home/www/.virtualenv/sphere
    chmod-socket = 777
    module = wsgi:application
    processes = 3
    master = True
    vacuum = True
    max-requests = 5000
    uid = www
    gid = www
    touch-reload = /home/www/my_project/touch_reload
    buffer-size = 32768

Разместим символическую ссылку в раздел запущеных приложений, перезапустим uWSGI сервер и посмотрим, запустилось ли наше приложение под сервером.

.. code-block:: bash

    ln -s /etc/uwsgi/apps-available/my_project.ini /etc/uwsgi/apps-enabled/my_project.ini
    service uwsgi restart
    service uwsgi status

Если видим там работающее приложение, значит все идет правильно.

.. code-block:: none

    root@virtualbox-sphere:~# service uwsgi status
    ● uwsgi.service - LSB: Start/stop uWSGI server instance(s)
       Loaded: loaded (/etc/init.d/uwsgi)
       Active: active (running) since Wed 2017-04-26 21:39:17 MSK; 18s ago
      Process: 22720 ExecStop=/etc/init.d/uwsgi stop (code=exited, status=0/SUCCESS)
      Process: 22759 ExecStart=/etc/init.d/uwsgi start (code=exited, status=0/SUCCESS)
       CGroup: /system.slice/uwsgi.service
               ├─22870 /usr/bin/uwsgi --ini /usr/share/uwsgi/conf/default.ini --ini /etc/uwsgi/apps-enabled/my_project.ini --daemonize /var/log/uwsgi/app/my_project.log
               ├─22895 /usr/bin/uwsgi --ini /usr/share/uwsgi/conf/default.ini --ini /etc/uwsgi/apps-enabled/my_project.ini --daemonize /var/log/uwsgi/app/my_project.log
               ├─22896 /usr/bin/uwsgi --ini /usr/share/uwsgi/conf/default.ini --ini /etc/uwsgi/apps-enabled/my_project.ini --daemonize /var/log/uwsgi/app/my_project.log
               └─22897 /usr/bin/uwsgi --ini /usr/share/uwsgi/conf/default.ini --ini /etc/uwsgi/apps-enabled/my_project.ini --daemonize /var/log/uwsgi/app/my_project.log

    Apr 26 21:39:17 virtualbox-sphere systemd[1]: Starting LSB: Start/stop uWSGI server instance(s)...
    Apr 26 21:39:17 virtualbox-sphere uwsgi[22759]: Starting app server(s): uwsgi -> . done.
    Apr 26 21:39:17 virtualbox-sphere systemd[1]: Started LSB: Start/stop uWSGI server instance(s).
    root@virtualbox-sphere:~#

Конфигурирование nginx
^^^^^^^^^^^^^^^^^^^^^^^^
nginx - это простой web-сервер, который будет непосредственно принимать запросы пользователей и пересылать их нашему uWSGI серверу с приложением.
Зачем все эти сложности?

Кроме динамического содержимого, есть много файлов сервера, которые никак не меняются и храняться в директориях как есть, файлы стилей, скрипты JavaScript, файлы, которые загружены пользователями.
Чтобы отдавать все это, не требуется сервера uWSGI (хотя он тоже это может делать, конечно). Но он будет тратить на это гараздо больше усилий, чем nginx.
Поэтому возникло вот такое распределение обязанностей. Сервер nginx принимает запросы и, может сжимать html-код, чтобы быстрее его отдавать через медленную сеть, какие-то запросы может обслужить сам.
А запросы, которые требуют какой-то логики системы, переадресует к uWSGI.
Если на сервере живут несколько приложений на 80-м или 443-м порту (http / https), то nginx по имени домена, на который пришел запрос, может разобраться и
перенаправить запрос в нужное приложение.

Для этого, создадим файл конфигурации ``nano /etc/nginx/sites-available/my_project``
Приведем самый простой случай, когда на сервере развернута только эта система и она развернута по http.
В этом случае, все входящие запросы на 80-й порт (порт по умолчанию для http) мы обрабатываем нашим приложением.
Запросы, которые пришли на /lib/media/, это запросы на получение файлов, загруженных пользователями.
Их мы отдаем через nginx сразу, не нагружая uwsgi без необходимости.

.. code-block:: nginx

    server {

        root /home/www/my_project/;
        listen       80 default;
        access_log off;

        client_max_body_size 50m;

        location /lib/media/ {
            alias /home/www/my_project/media/;
        }

        location /lib/static/ {
            alias /home/www/my_project/sphere/lib/static/;
        }

        location / {
            include uwsgi_params;

            uwsgi_buffering off;
            uwsgi_pass unix:///run/uwsgi/app/my_project/socket;
            uwsgi_read_timeout 300;
            uwsgi_connect_timeout 300;
        }

    }

Разместим символическую ссылку в раздел запущеных приложений, перезапустим сервер nginx

.. code-block:: bash

    ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enabled/my_project
    rm /etc/nginx/sites-available/default
    service nginx restart

Проверим в браузере работу нашего приложения http://IP_СЕРВЕРА/


Запуск фоновых процессов
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Часть работы система откладывает "на потом", чтоб сделать ее, не в фоновом режиме, когда представится возможность.
Это операции по сохранению логов по редактированию карточек в приложении bps, логгированию каждого запроса пользователя.
Есть еще операции, которые выполняются по расписанию, используя эти же фоновые проецессы.
Например, проверить просроченные дела, проверить задачи, по которым пользователи выставили себе оповещения и разослать их по операторам и так далее.

Для всего этого, мы используем проект celery, который тесно интегрирован в систему и его остается просто запустить, чтоб он начал работать.
Запускаем все это через supervisor

Настроим транспорт, через который будут передаваться задания между процессом, который выполняет работу и системой, которая будет ставить ему задачи

.. code-block:: bash

    rabbitmqctl add_user sphere_user *********
    rabbitmqctl add_vhost localhost_my_project
    rabbitmqctl set_permissions -p localhost_my_project sphere_user ".*" ".*" ".*"

И пароль, который мы ввели при создании пользователя пропишем в настройку транспорта брокера фоновых процессов
``nano /home/www/my_project/conf_local.py``
````

Cоздадим файл конфигурации ``nano /etc/supervisor/conf.d/my_project.conf``

.. code-block:: ini

    [program:my_project]
    directory=/home/www/my_project
    command=/home/www/.virtualenv/sphere/bin/celery -A sphere worker --beat -E --loglevel=warning -n celery_my_project
    user=www
    numprocs=1
    autostart=true
    autorestart=true
    startsecs=10
    stopwaitsecs=600
    killasgroup=true

После этого перезагрузим supervisor и убедимся, что наше приложение работает

.. code-block:: bash

    supervisorctl reload

.. code-block:: none

    supervisorctl status

    root@virtualbox-sphere:~# supervisorctl status
    my_project                       **RUNNING**    pid 23518, uptime 0:00:12
    root@virtualbox-sphere:~#

    # Из под учетной записи www из директории /home/www/my_project
    celery status -b 'amqp://sphere_user:*********@localhost:5672/localhost_my_project'

    (sphere)www@virtualbox-sphere:~/my_project$
    (sphere)www@virtualbox-sphere:~/my_project$ celery status -b 'amqp://sphere_user:*********@localhost:5672/localhost_my_project'
    celery@celery_my_project: OK

    **1 node online.**
    (sphere)www@virtualbox-sphere:~/my_project$

На этом все. У нас есть приложение, которое работает. В нем есть учетная запись супер-пользователя и запущен менеджер фоновых операций.
Чтобы убедиться, что все работает и запускается при загрузки сервера, перезапустим его и после запуска, проверим работающее приложение в браузере

.. code-block:: bash

    reboot
