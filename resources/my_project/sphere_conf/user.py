""" Кастомизация параметров пользователя системы. """


class UserMixin(object):
    """ Дополнительные поля / переопределяем методы пользователя
    в sphere.auth.models.User """


class AdminMixin(object):
    """ Дополнителнения / переопределяем методы админки пользователя
    в sphere.auth.admin.UserView """
