""" Источник данных для отправки СМС-сообщений. """


class SMSDataSource(object):
    """ Поставщик данных. """

    def get_log_data(self):
        """ Данные для сохранения в лог письма после его отправки. """
        return {}

    @property
    def message_types(self):
        """ Типы сообщений. """
        return [
            ('recall', 'Перезвонить'),
            ('get_documents', 'Предоставить документы'),
        ]

    @property
    def recipients(self):
        """
        Список возможных номеров для отправки SMS.
        Если передать пустой список, то оператору нужно будет номера телефонов прописать вручную.
        """
        return [
            ('+79269344424', 'Степан Дибров'),
        ]

    def get_ajax_data(self, message_type):
        """
        Тексты сообщений по умолчанию.

        Оператор их может поправить как нужно
        """
        if message_type == 'get_documents':
            message = 'Прошу предоставить документы.'

        elif message_type == 'recall':
            message = 'Прошу перезвонить нам.'

        return {
            'message': message
        }
