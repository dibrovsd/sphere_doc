from werkzeug.datastructures import FileStorage
from io import BytesIO
from flask import flash
from datetime import timedelta

from sphere import db
from sphere.email import signals
from sphere.bps.models import CallcenterMessage
from sphere.bps.plugins.files.models import CallcenterMessageFile
from sphere.auth.models import User
from sphere.lib.utils import get_model
from sphere.auth.utils import get_current_user
from sphere.bps.plugins.tasks.signals import task_saved


@task_saved.connect
def task_saved_handler(sender, document, task, created):
    """
    Если в настройках задачи есть настройка напоминания "За" сколько-то минут и при этом не было 
    выставлено напоминание при создании задачи, создаем напоминание автоматически
    """
    if created:
        try:
            notify_time_before = document.project.tasks[task.task_type].get('notify_time_before')
            if notify_time_before and task.d_expire and not task.reminds:
                for time_remaind in notify_time_before:
                    TaskRemind = get_model(document.project.model_name + 'TaskRemind')
                    remind = TaskRemind(
                        task_id=task.id,
                        author_id=get_current_user().id,
                        d_remind=task.d_expire - timedelta(minutes=int(time_remaind))
                    )
                    db.session.add(remind)
        except ValueError:
            flash('Не удалось создать автоматическое напоминание.<br/>Создайте напоминание в ручную!', 'warning')


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
