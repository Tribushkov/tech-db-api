import json
from flask import Blueprint, request
from api.models import post, thread
from utils.helpers import *
from config import *

module = Blueprint('post', __name__, url_prefix='/db/api/post')


@module.route("/create/", methods=["POST"])
def create():
    content = request.json
    required_data = ["user", "forum", "thread", "message", "date"]
    optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    optional = intersection(request=content, values=optional_data)
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.create(date=content["date"], thread=content["thread"],
                        message=content["message"], user=content["user"],
                        forum=content["forum"], optional=optional)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/details/", methods=["GET"])
def details():
    content = get_json(request)
    required_data = ["post"]
    related = related_exists(content)
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.details(content["post"], related=related)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/list/", methods=["GET"])
def post_list():
    content = get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:  # TODO some refactoring
        try:
            identifier = content["thread"]
            entity = "thread"
        except:
            response = STATUS_CODE['NOT_FOUND']
            return json.dumps(response)

    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        response = STATUS_CODE['OK']
        response['response'] = post.posts_list(entity=entity, params=optional, identifier=identifier, related=[])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/remove/", methods=["POST"])
def remove():
    content = get_json(request)
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.remove_restore(post_id=content["post"], status=1)
        thread.dec_posts_count(content["post"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/restore/", methods=["POST"])
def restore():
    content = request.json
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        thread.inc_posts_count(content["post"])
        response['response'] = post.remove_restore(post_id=content["post"], status=0)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/update/", methods=["POST"])
def update():
    content = request.json
    required_data = ["post", "message"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.update(update_id=content["post"], message=content["message"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/vote/", methods=["POST"])
def vote():
    content = request.json
    required_data = ["post", "vote"]
    try:
        choose_required(data=content, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.vote(vote_id=content["post"], vote_type=content["vote"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)
