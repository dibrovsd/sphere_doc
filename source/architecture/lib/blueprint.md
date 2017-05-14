Ресурсы приложения
===================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.lib.blueprint

* Путь `/media/<path:relative_path>` вызывает `media`

* Путь `/attachment/<path:relative_path>` вызывает `attachment`

* Путь `/set_lang/<code>/` вызывает `set_lang`

* Путь `/show_file/<path:relative_path>` вызывает `ShowFile`

  Системное имя _show_file_

* Путь `/close_modal_window/` вызывает `CloseModalWindow`

  Системное имя _close_modal_window_

* Путь `/user_notification/new/` вызывает `UserNotificationsNewView`

  Системное имя _user_notification_new_

* Путь `/user_notification/content/` вызывает `UserNotificationsContentView`

  Системное имя _user_notification_content_

* Метод `form_render` доступен глобально под именем `form_render`

* Метод `url_for` доступен глобально под именем `url`

* Метод `render_paginator` доступен глобально под именем `render_paginator`

* Метод `now` доступен глобально под именем `now`

* Метод `thumbnail` доступен глобально под именем `thumbnail`

* Метод `format_datetime` доступен глобально под именем `datetime`

* Метод `format_date` доступен глобально под именем `date`

* Метод `momentjs_from_now` доступен глобально под именем `from_now`

* Метод `to_json` доступен глобально под именем `to_json`

* Метод `to_string` доступен глобально под именем `to_string`

* Метод `nl2br` доступен глобально под именем `nl2br`

* Метод `numformat` доступен глобально под именем `numformat`

* Метод `multiline` доступен глобально под именем `multiline`

.. automodule:: sphere.lib.blueprint
    :members:
    :show-inheritance:
    :undoc-members:
