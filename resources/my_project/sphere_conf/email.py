""" Источник данных для отправки Email-сообщений. """

from flask import request
from werkzeug.utils import cached_property

from sphere.bps.models import Claim, CallcenterMessage
from sphere.email.models import Log as EmailLog
from sphere.auth.utils import get_current_user


class EmailDataSource(object):
    """ Класс с методами, которые поставляют данные для GUI генератора писем. """

    @property
    def current_project(self):
        """ Название текущего проекта. """
        for project_name in ['claim', 'callcenter_message']:
            if project_name + '_id' in request.args:
                return project_name

    @cached_property
    def current_document(self):
        """ Текущий объект, из которого создается письмо. """
        model = {
            'claim': Claim,
            'callcenter_message': CallcenterMessage
        }.get(self.current_project)

        return model.query.get(request.args['%s_id' % self.current_project])

    def get_log_data(self):
        """ Данные для сохранения в лог письма после его отправки. """
        return {k: int(request.args.get(k)) for k in request.args}

    @cached_property
    def reply_to(self):
        """ Базовое письмо, на котороые оператор пишет ответ. """
        if 'reply_to' in request.values:
            return EmailLog.query.get(request.values['reply_to']).first()

    @property
    def message_types(self):
        """ Возможные типы сообщений. """
        if self.reply_to:
            return [('reply', 'Ответ')]

        return [
            ('new', 'Новое сообщение'),
            ('get_documents', 'Предоставить недостающие документы'),
        ]

    @property
    def recipients(self):
        """ Возможные получатели сообщения. """
        # Для ответа подставляем отправителя из исходного письма
        if self.reply_to:
            return {
                'choices': [self.reply_to.sender],
                'default': [self.reply_to.sender],
            }

        if self.current_document:
            return {
                'choices': self.current_document.email_recepients,
                'default': [],
            }

        return {
            'choices': [],
            'default': [],
        }

    def get_ajax_data(self, message_type):
        """ Данные сформированного по умолчанию письма. """
        signature = 'С уважением, \n%s. \nООО СК «Сбербанк страхование» \nwww.sberbankins.ru' % get_current_user()

        if self.reply_to:
            return {
                'message': '\n ------ Исходное сообщение ------ \n %s' % self.reply_to.message,
                'subject': 'Re: %s' % self.reply_to.subject,
                'signature': signature,
            }

        data = {
            'new': {
                'subject': 'Сбербанк: Добрый день.',
                'message': '%s' % self.current_document,
                'signature': signature,
            },
            'get_documents': {
                'subject': 'Сбербанк: Запрос документов',
                'message': 'Добрый день.\nПрошу предоставить документы',
                'signature': signature,
            }
        }

        return data[message_type]
