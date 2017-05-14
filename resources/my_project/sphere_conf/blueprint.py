
from flask import Blueprint
from base import views

blueprint = Blueprint('sphere_conf', __name__, template_folder='templates')

blueprint.add_url_rule('/', view_func=views.index)
