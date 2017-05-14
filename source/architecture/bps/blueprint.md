Ресурсы приложения
===================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.bps.blueprint

* Представления
    * Путь `/` вызывает `IndexView`

    Системное имя _index_

    * Путь `/<project_name>/` вызывает `DocumentListView`

      Системное имя _document_list_

    * Путь `/<project_name>/filter/` вызывает `FilterView`

      Системное имя _filter_

    * Путь `/<project_name>/preset/save/<preset_name>/` вызывает `SavePreset`

      Системное имя _save_preset_

    * Путь `/<project_name>/preset/reset/` вызывает `SavePreset`

      Системное имя _reset_preset_

    * Путь `/<project_name>/create/` вызывает `DocumentForm`

      Системное имя _document_create_

    * Путь `/<project_name>/<document_id>/` вызывает `DocumentForm`

      Системное имя _document_form_

    * Путь `/<project_name>/<document_id>/delete/` вызывает `DeleteDocumentView`

      Системное имя _document_delete_

    * Путь `/<project_name>/<document_id>/event_form/<status>/<event>/` вызывает `DocumentEvent`

      Системное имя _event_form_

    * Путь `/<project_name>/<document_id>/event_accept/` вызывает `DocumentAcceptView`

      Системное имя _event_accept_

* Ajax
    * Путь `/<project_name>/autocomplete/<data_source>/` вызывает `AutocompleteChoicesView`

      Системное имя _autocomplete_data_

    * Путь `/<project_name>/autocomplete_label/<data_source>/` вызывает `AutocompleteLabelView`

      Системное имя _autocomplete_label_

* Плагины

    * Путь `/<project_name>/<document_id>/add_comment/` вызывает `DocumentCommentCreate`

      Системное имя _document_add_comment_

* Расширения

    * Метод `render_form_fields` доступен глобально под именем `bps_form_fields`

    * Метод `field_to_str` доступен глобально под именем `field_to_str`

    * Метод `get_data_source_label` доступен глобально под именем `bps_data_source_label`

* Авто-документация
    * Путь `/docs/` вызывает `IndexView`

      Системное имя _docs_index_

    * Путь `/docs/<project_name>/` вызывает `ProjectView`

      Системное имя _docs_project_

    * Путь `/docs/<project_name>/<status>/` вызывает `WorkflowView`

      Системное имя _docs_workflow_
