from data_provider import sql
import user


def add_follow(email1, email2):
    sql.update_query('INSERT INTO follower (follower, followee) VALUES (%s, %s)', (email1, email2, ))
    return user.details(email1)


def remove_follow(email1, email2):
    sql.update_query('DELETE FROM follower WHERE follower = %s AND followee = %s', (email1, email2, ))
    return user.details(email1)


def followers_list(email, type, params):
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"

    query = "SELECT " + type + " FROM follower JOIN user ON user.email = follower." + type + \
            " WHERE " + where + " = %s "

    if "since_id" in params:
        query += " AND user.id >= " + str(params["since_id"])
    if "order" in params:
        query += " ORDER BY user.name " + params["order"]
    else:
        query += " ORDER BY user.name DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    followers_ids_tuple = sql.select_query(query=query, params=(email, ))

    f_list = []
    for id in followers_ids_tuple:
        id = id[0]
        f_list.append(user.details(email=id))

    return f_list


def list_following(cursor, user_id):
    cursor.execute("""SELECT followee FROM follower WHERE follower = %s;""", (user_id, ))
    following = [i['followee'] for i in cursor.fetchall()]
    return following


def list_followers(cursor, user_id):
    cursor.execute("""SELECT follower FROM follower WHERE followee = %s;""", (user_id, ))
    followers = [i['follower'] for i in cursor.fetchall()]
    return followers

