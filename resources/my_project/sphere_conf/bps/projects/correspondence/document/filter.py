""" Логика фильтров докуметов проекта. """

from sphere.auth.utils import get_current_user


class DocumentFilterMixin(object):
    @classmethod
    def filter_query(cls, query, for_display, filter_data=None, preset=None):
        query = query.filter_by(active=True)
        user = get_current_user()
        roles = user.role_set

        # Фильтры ограничения доступа размещаем тут
        if 'admin' not in roles:
            # Если не администратор, то доступа к архиву нет
            query = query.filter_by(cls.status != 'archive')

        if for_display == 'item':
            return query  # Для открытия карточки ничего фильтровать не нужно

        expr = []
        if preset == 'work':
            expr.append(cls.status != 'archive')

        elif preset == 'archive':
            expr.append(cls.status == 'archive')

        if filter_data:
            for k, v in filter_data.items():
                # тут добавляем в expr кастомные фильтры
                pass

        if expr:
            query = query.filter(*expr)

        return query.order_by('id desc')
