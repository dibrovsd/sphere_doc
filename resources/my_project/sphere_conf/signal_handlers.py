from werkzeug.datastructures import FileStorage
from io import BytesIO

from sphere import db
from sphere.email import signals
from sphere.bps.models import CallcenterMessage
from sphere.bps.plugins.files.models import CallcenterMessageFile
from sphere.auth.models import User


@signals.email_loaded.connect_via('sber@sbps.ru')
def email_loaded_handler(sender, obj, msg, conn):
    """ Обрабатываем загруженное письмо. """

    # Если это ответ на наше письмо, проставим в нем те же привязки, что и в исходном письме
    if obj.reply_to_message:
        obj.data = obj.reply_to_message.data

    else:
        # Если новое письмо, создаем документ в сообщениях КЦ
        user = User.query.filter_by(email='robot@sbps.ru').first()
        callcenter_message = CallcenterMessage(author=user)

        db.session.add(callcenter_message)
        db.session.flush()

        # Приложим вложения письма
        for attachment in obj.get_attachments():
            fl = CallcenterMessageFile(document_id=callcenter_message.id)
            fl.save_file(FileStorage(
                stream=BytesIO(attachment['content']),
                filename=attachment['filename']
            ))
            db.session.add(fl)

        # Привязка письма к убытку
        obj.data = {'callcenter_message_id': callcenter_message.id}
