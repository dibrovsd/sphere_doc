#!/usr/bin/env python
# coding=utf-8

"""
Файл для запуска системы через uWSGI в рабочем режиме.

Через него сервер общается с приложением.
Тут мы используем наш сервер под именем application и запускаем его в режиме вечного цикла.
Он будет ждать запросов от uWSGI сервере и будет их исполнять.
"""

from sphere import server as application

if __name__ == "__main__":
    application.run()
