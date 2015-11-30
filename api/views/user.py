import json
from flask import Blueprint, request
from api.models import user, post, follower
from utils.helpers import *
from config import *

module = Blueprint('user', __name__, url_prefix='/db/api/user')


@module.route("/create/", methods=["POST"])
def create():
    request_data = request.json
    required_data = ["email", "username", "name", "about"]
    optional = intersection(request=request_data, values=["isAnonymous"])
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = user.save_user(email=request_data["email"], username=request_data["username"],
                               about=request_data["about"], name=request_data["name"], optional=optional)
    except Exception as e:
        if e.message == STATUS_CODE['ALREADY_EXISTS']:
            response = STATUS_CODE['ALREADY_EXISTS']
        else:
            response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/details/", methods=["GET"])
def details():
    request_data = get_json(request)
    required_data = ["user"]
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = user.details(email=request_data["user"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/follow/", methods=["POST"])
def follow():
    request_data = request.json
    required_data = ["follower", "followee"]
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = follower.add_follow(email1=request_data["follower"], email2=request_data["followee"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/unfollow/", methods=["POST"])
def unfollow():
    request_data = request.json
    required_data = ["follower", "followee"]
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = follower.remove_follow(email1=request_data["follower"], email2=request_data["followee"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listFollowers/", methods=["GET"])
def list_followers():
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = follower.followers_list(email=request_data["user"], type="follower", params=followers_param)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listFollowing/", methods=["GET"])
def list_following():
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = follower.followers_list(email=request_data["user"], type="followee", params=followers_param)
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/listPosts/", methods=["GET"])
def list_posts():
    request_data = get_json(request)
    required_data = ["user"]
    optional = intersection(request=request_data, values=["limit", "order", "since"])
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = post.posts_list(entity="user", params=optional, identifier=request_data["user"], related=[])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)


@module.route("/updateProfile/", methods=["POST"])
def update():
    request_data = request.json
    required_data = ["user", "name", "about"]
    try:
        choose_required(data=request_data, required=required_data)
        response = STATUS_CODE['OK']
        response['response'] = user.update_user(email=request_data["user"], name=request_data["name"], about=request_data["about"])
    except:
        response = STATUS_CODE['NOT_FOUND']
    return json.dumps(response)
