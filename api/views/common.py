from api.models.common import clear, status
from flask import Blueprint
from config import *
import json

module = Blueprint('common', __name__, url_prefix='/db/api')


@module.route("/clear/", methods=['POST', 'GET'])
def clear_db():
    try:
        clear()
    except:
        pass
    response = STATUS_CODE['OK']
    return json.dumps(response)


@module.route('/status/', methods=['GET'])
def show_status():
    stat = status()
    response = STATUS_CODE['OK']
    response['response'] = stat
    return json.dumps(response)


