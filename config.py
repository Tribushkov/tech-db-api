DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "forumdb"
DB_CHARSET = "utf8"

STATUS_CODE = {
    'OK': {'code': 0},
    'NOT_FOUND': {'code': 1, 'response': 'object not found'},
    'INVALID_REQUEST': {'code': 2, 'response': 'invalid request'},
    'WRONG_REQUEST': {'code': 3, 'response': 'wrong request'},
    'UNKNOWN_ERROR': {'code': 4, 'response': 'unknown error'},
    'ALREADY_EXISTS': {'code': 5, 'response': 'object already exists'}
}
