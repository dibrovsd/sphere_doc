""" Источник данных для отправки Email-сообщений. """

from flask import request
from werkzeug.utils import cached_property

from sphere.bps.models import Claim, CallcenterMessage
from sphere.email.models import Log as Email
from sphere.auth.utils import get_current_user
from sphere.lib.utils import get_model


class EmailDataSource(object):
    """ Класс с методами, которые поставляют данные для GUI генератора писем. """

    @cached_property
    def document(self):
        """ Текущий объект, к которому создается письмо. """
        model = get_model(request.args.get('model_name'))
        return model.query.get(request.args.get('object_id'))

    @cached_property
    def project(self):
        """ Текущий проект. """
        return self.document.project

    @property
    def project_name(self):
        """ Текущий проект. """
        return self.project.name

    @cached_property
    def reply_to(self):
        """ Базовое письмо, на котороые оператор пишет ответ. """
        reply_to_id = request.args.get('reply_to')
        if reply_to_id:
            return Email.query.get(reply_to_id)

    def get_log_data(self):
        return None

    def get_object_linked(self):
        res = [self.document]
        return res

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
