from flask import Flask
from api.views.thread import module as thread
from api.views.user import module as user
from api.views.forum import module as forum
from api.views.post import module as post
from api.views.common import module as common

app = Flask(__name__)

app.register_blueprint(common)
app.register_blueprint(user)
app.register_blueprint(forum)
app.register_blueprint(thread)
app.register_blueprint(post)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=False)
