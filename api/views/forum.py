from flask import Blueprint, request
from api.models import forum, post, thread
from utils.helpers import *
from config import *
import simplejson as json

module = Blueprint('forum', __name__, url_prefix='/db/api/forum')


@module.route("/create/", methods=["POST"])
def create():
    content = request.json
    required_data = ["name", "short_name", "user"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = forum.save_forum(name=content["name"], short_name=content["short_name"],
                                  user=content["user"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/details/", methods=["GET"])
def details():
    get_params = get_json(request)
    required_data = ["forum"]
    related = related_exists(get_params)
    try:
        choose_required(data=get_params, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = forum.details(short_name=get_params["forum"], related=related)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listThreads/", methods=["GET"])
def list_threads():
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.thread_list(entity="forum", identifier=content["forum"],
                                         related=related, params=optional)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listPosts/", methods=["GET"])
def list_posts():
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    
    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.posts_list(entity="forum", params=optional, identifier=content["forum"],
                                    related=related)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listUsers/", methods=["GET"])
def list_users():
    content = get_json(request)
    required_data = ["forum"]
    optional = intersection(request=content, values=["limit", "order", "since_id"])
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = forum.list_users(content["forum"], optional)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)
