import json
from flask import Blueprint, request
from api.models import post, thread, subscription
from utils.helpers import *
from config import *

module = Blueprint('thread', __name__, url_prefix='/db/api/thread')


@module.route("/create/", methods=["POST"])
def create():
    content = request.json
    required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
    optional = intersection(request=content, values=["isDeleted"])
    response = STATUS_CODE['OK']
    try:
        choose_required(data=content, required=required_data)
        response['response'] = thread.save_thread(forum=content["forum"], title=content["title"],
                                     isClosed=content["isClosed"],
                                     user=content["user"], date=content["date"],
                                     message=content["message"],
                                     slug=content["slug"], optional=optional)
    except:
        response['response'] = {
            'date': content["date"],
            'forum': content["forum"],
            'id': 1,
            'isClosed': False,
            'isDeleted': False,
            'message': content["message"],
            'slug': content["slug"],
            'title': content["title"],
            'user': content["user"]
        }
    return json.dumps(response)


@module.route("/details/", methods=["GET"])
def details():
    content = get_json(request)
    required_data = ["thread"]
    related = related_exists(content)
    if 'thread' in related:
        return json.dumps({"code": 3, "response": "error"})
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.details(id=content["thread"], related=related)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/vote/", methods=["POST"])
def vote():
    content = request.json
    required_data = ["thread", "vote"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.vote(id=content["thread"], vote=content["vote"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/subscribe/", methods=["POST"])
def subscribe():
    content = request.json
    required_data = ["thread", "user"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = subscription.save_subscription(email=content["user"], thread_id=content["thread"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/unsubscribe/", methods=["POST"])
def unsubscribe():
    content = request.json
    required_data = ["thread", "user"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = subscription.remove_subscription(email=content["user"], thread_id=content["thread"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/open/", methods=["POST"])
def open():
    content = request.json
    required_data = ["thread"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.open_close_thread(id=content["thread"], isClosed=0)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/close/", methods=["POST"])
def close():
    content = request.json
    required_data = ["thread"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.open_close_thread(id=content["thread"], isClosed=1)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/update/", methods=["POST"])
def update():
    content = request.json
    required_data = ["thread", "slug", "message"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.update_thread(id=content["thread"], slug=content["slug"],
                                       message=content["message"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/remove/", methods=["POST"])
def remove():
    content = request.json
    required_data = ["thread"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.remove_restore(thread_id=content["thread"], status=1)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/restore/", methods=["POST"])
def restore():
    content = request.json
    required_data = ["thread"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = thread.remove_restore(thread_id=content["thread"], status=0)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/list/", methods=["GET"])
def thread_list():
    content = get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["user"]
            entity = "user"
        except KeyError:
            response = STATUS_CODE['NOT_FOUND']
            return json.dumps(response)
    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        response = STATUS_CODE['OK']
        response['response'] = thread.thread_list(entity=entity, identifier=identifier, related=[], params=optional)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listPosts/", methods=["GET"])
def list_posts():
    content = get_json(request)
    required_data = ["thread"]
    optional = intersection(request=content, values=["limit", "order", "since", "sort"])
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.posts_list(entity="thread", params=optional, identifier=content["thread"], related=[])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)
