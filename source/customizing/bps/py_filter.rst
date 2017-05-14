Работа с фильтром
=====================
Для настройки фильтра необходимо создать метод для обработки полей фильтра.
Все Python файлы для работы с документом необходимо хранить в директории ``/<ИМЯ_ПРОЕКТА>/document/``

Для работы с фильтром необходимо создать файл ``filter.py``, содержащий класс **DocumentFilterMixin** с методом *filter_query*. Данный метод формирует запрос к базе с учетом фильтра по параметрам, описанным в конфигурационном файле проекта.

.. code-block:: python

    class DocumentFilterMixin(object):
        @classmethod
        def filter_query(cls, query, for_display, filter_data=None, preset=None):
            query = query.filter_by(active=True) #фильтр по активным документам

            # Для открытия каталога ничего фильтровать не нужно
            if for_display == 'item':
                return query

            query = query.order_by(cls.d_create.desc())

            expr = [] #запрос для sqlalchemy

        if filter_data: #если есть заполненные поля фильтра
            for k, v in filter_data.items():

                # сборка запроса

                if k == 'client_name':
                    expr.append(expr.append(Client.legal_status == v)

        if expr:
            query = query.filter(*expr)

        return query

Для формирования запроса необходимо набрать **выражение (expr)** для добавления к запросу. Делается это добавлением пар **ключ/значение** (k, v).

**Примеры того как можно добавлять пары в запрос**

- Полное равенство

.. code-block:: python

    if k == 'field_1':
        contracts_filter_exp.append(cls.field_1 == v)

- Неполное равенство

.. code-block:: python

    if k == 'field_1':
        contracts_filter_exp.append(ilike(cls.field_1, v))

*Для использования ilike необходимо импортировать модуль из sphere.lib.utils:*
``from sphere.lib.utils import ilike``

- Поиск среди ключей

Для упрощения кода можно объединять поля фильтра в группы c одинаковой логикой и делать поиск среди ключей:

.. code-block:: python

    if k in ('field_1', 'field_2', 'field_3'):
        expr.append(getattr(cls, k) == v)

    if k in ('field_1', 'field_2', 'field_3'):
        expr.append(ilike(getattr(cls, k), v))

- Поиск в промежутке между значениями

.. code-block:: python

    if k in ('field_1', 'field_2', 'field_3'):
        if k == 'field_1':
        expr.append(cls.field_1.between(*v))

Применимо для полей с **data_type** равным *integer_range, date_range, float_range*

.. tip::

    Для того чтобы использовать фильтр его необходимо подключить в файле приложения document
    
    ``...папка_проекта/document/__init__.py:``


.. code-block:: python

    from .filter import DocumentFilterMixin

    class DocumentMixin(DocumentFilterMixin):
    . . .
