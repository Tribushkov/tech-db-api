from data_provider import sql


def clear():
    tables = ['post', 'thread', 'forum', 'subscription', 'follower', 'user']
    sql.execute("SET global foreign_key_checks = 0;")
    for table in tables:
        sql.execute("TRUNCATE TABLE %s;" % table)
    sql.execute("SET global foreign_key_checks = 1;")


def status():
    resp = []
    tables = ['user', 'thread', 'forum', 'post']

    for table in tables:
        count = len(sql.select_query('SELECT id FROM ' + table, ()))
        resp.append(count)

    response = {
        'user': resp[0],
        'thread': resp[1],
        'forum': resp[2],
        'post': resp[3]
    }
    return response
