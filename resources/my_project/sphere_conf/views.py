""" Логика отображения данных """

from flask import render_template


def index():
    """ Стартовая страница системы. """
    return render_template('sphere_conf/index.html')
