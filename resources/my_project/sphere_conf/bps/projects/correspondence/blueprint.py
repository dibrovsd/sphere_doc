from flask import Blueprint


blueprint = Blueprint('correspondence', __name__,
                      static_folder='static',
                      template_folder='templates')
