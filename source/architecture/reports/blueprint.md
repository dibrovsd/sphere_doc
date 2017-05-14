Ресурсы приложения
===================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.reports.blueprint
    
* Пользовательская часть

    * Путь `/` вызывает `IndexView`

      Системное имя _index_

    * Путь `/<int:report_id>/` вызывает `ReportView`

      Системное имя _report_

    * Путь `/<int:report_id>/xls/<sql_name>/` вызывает `ReportXLSView`

      Системное имя _report_xls_

* Админка

    * Путь `/<int:report_id>/edit/` вызывает `ReportEditView`

      Системное имя _edit_index_

    * Путь `/<int:report_id>/edit_sql/<sql_name>/` вызывает `ReportEditSQL`

      Системное имя _edit_sql_

    * Путь `/<int:report_id>/edit_include/<include_name>/` вызывает `ReportEditInclude`

      Системное имя _edit_include_
