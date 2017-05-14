Ресурсы приложения
===================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.logs.blueprint

* API
    * Путь `/api/message/` вызывает `ServiceMessageView`

      Системное имя _api_get_message_

* GUI

    * Путь `/` вызывает `EventListView`

      Системное имя _index_

    * Путь `/filter_form/` вызывает `FilterFormView`

      Системное имя _filter_form_

    * Путь `/event_list_status_change/<status>/` вызывает `EventListSetStatusView`

      Системное имя _event_list_status_change_

    * Путь `/<int:event_id>/` вызывает `EventView`

      Системное имя _event_

    * Путь `/<int:event_id>/status/<status>/` вызывает `EventSetStatusView`

      Системное имя _event_status_change_
