""" Логика отображения данных """

from flask import render_template

from sphere.auth.utils import get_current_user
from sphere_conf.utils import get_index_content


def index():
    """ Стартовая страница системы. """
    user = get_current_user()
    content = None

    if user:
        content = get_index_content(user=get_current_user())

    return render_template('sphere_conf/index.html', content=content)
