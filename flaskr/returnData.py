
from flask import (
    Blueprint
)

bp = Blueprint('auth', __name__, url_prefix='/get')

# @bp.route('/register', methods=('GET', 'POST'))
# def getData()