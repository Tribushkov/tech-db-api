from data_provider import sql
import user, follower


def save_forum(name, short_name, user):
    sql.update_query('INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)',
                               (name, short_name, user, ))
    forum = sql.select_query(
            'select id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
        )
    return forum_description(forum)


def forum_description(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def details(short_name, related):
    forum = sql.select_query(
        'select id, name, short_name, user FROM forum WHERE short_name = %s LIMIT 1;', (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with exists short_name=" + short_name)
    forum = forum_description(forum)

    if "user" in related:
        forum["user"] = user.details(forum["user"])
    return forum


def list_users(short_name, optional):
    query = "SELECT user.id, user.email, user.name, user.username, user.isAnonymous, user.about FROM user " \
        "WHERE user.email IN (SELECT DISTINCT user FROM post WHERE forum = %s)"
    if "since_id" in optional:
        query += " AND user.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY user.name " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    con = sql.connect()
    cursor = con.cursor(sql.db.cursors.DictCursor)
    cursor.execute(query, (short_name, ))
    users_tuple = [i for i in cursor.fetchall()]

    for user_sql in users_tuple:
        cursor.execute("""SELECT `thread` FROM `subscription` WHERE `user` = %s;""", (user_sql['email'], ))
        sub = [i['thread'] for i in cursor.fetchall()]

        followers = follower.list_followers(cursor, user_sql['email'])
        following = follower.list_following(cursor, user_sql['email'])

        user_sql.update({'following': following, 'followers': followers, 'subscriptions': sub})
    cursor.close()
    return users_tuple
