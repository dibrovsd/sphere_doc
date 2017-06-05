#!/usr/bin/env python
# coding=utf-8

"""
Файл для запуска управляющих команд из консоли.
"""

from flask_script import Manager
from sphere import server, db, cache
from sphere.lib.managment_commands import create_superuser as create_superuser_
from sphere.lib.syncdb import SyncManager
from sphere.reports.commands import update_label_map
from flask_migrate import MigrateCommand

manager = Manager(server)

manager.add_command('db', MigrateCommand)
"""
Команды для работы с базами данных
"""


@manager.command
def runserver(host='127.0.0.1', port='5000', debug='True'):
    """ Запуск отладочного сервера. """
    is_debug = debug == 'True'
    server.run(host=host, port=int(port), debug=is_debug)


@manager.command
def create_superuser(email, password):
    """ Создать пользователя с правами админа. """
    create_superuser_(email, password)


@manager.command
def syncdb():
    """ Выполнить модификацию базы данных, взяв модели за основу """
    manager = SyncManager(engine=db.engine)
    manager.process()


@manager.command
def cache_clear():
    """ Полный сброс кэша """
    cache.clear()


@manager.command
def report_update_label_map():
    """ Обновить справочники для отчетов.  """
    update_label_map()


if __name__ == "__main__":
    manager.run()
