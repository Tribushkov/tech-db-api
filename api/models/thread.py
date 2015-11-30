from data_provider import sql
import user, forum


def save_thread(forum, title, isClosed, user, date, message, slug, optional):
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    sql.update_query('INSERT INTO thread (forum, title, isClosed, user, date, message, slug, isDeleted) '
                               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (forum, title, isClosed, user, date, message, slug, isDeleted, ))
    thread = sql.select_query(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM thread WHERE slug = %s', (slug, )
        )
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
    }
    return response


def details(id, related):
    thread = sql.select_query(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM thread WHERE id = %s LIMIT 1;', (id, )
    )
    if len(thread) == 0:
        raise Exception('No thread exists with id=' + str(id))
    thread = thread[0]
    thread = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    if "user" in related:
        thread["user"] = user.details(thread["user"])
    if "forum" in related:
        thread["forum"] = forum.details(short_name=thread["forum"], related=[])

    return thread


def vote(id, vote):
    try:
        if vote == -1:
            sql.update_query("UPDATE thread SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
        else:
            sql.update_query("UPDATE thread SET likes=likes+1, points=points+1  where id = %s", (id, ))
    except Exception as e:
        print(e.message)
    return details(id=id, related=[])


def open_close_thread(id, isClosed):
    sql.update_query("UPDATE thread SET isClosed = %s WHERE id = %s", (isClosed, id, ))

    response = {
        "thread": id
    }
    return response


def update_thread(id, slug, message):
    sql.update_query('UPDATE thread SET slug = %s, message = %s WHERE id = %s', (slug, message, id, ))

    return details(id=id, related=[])


def thread_list(entity, identifier, related, params):
    query = "SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts " \
            "FROM thread WHERE " + entity + " = %s "
    parameters = [identifier]

    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])
    thread_ids_tuple = sql.select_query(query=query, params=parameters)
    thread_list = []
    for thread in thread_ids_tuple:
        thread = {
            'date': str(thread[0]),
            'forum': thread[1],
            'id': thread[2],
            'isClosed': bool(thread[3]),
            'isDeleted': bool(thread[4]),
            'message': thread[5],
            'slug': thread[6],
            'title': thread[7],
            'user': thread[8],
            'dislikes': thread[9],
            'likes': thread[10],
            'points': thread[11],
            'posts': thread[12],
        }
        if "user" in related:
            thread["user"] = user.details(thread["user"])
        if "forum" in related:
            thread["forum"] = forum.details(short_name=thread["forum"], related=[])
        thread_list.append(thread)
    return thread_list


def remove_restore(thread_id, status):
    if status == 1:
        posts = 0
    else:
        posts = sql.select_query("SELECT COUNT(id) FROM post WHERE thread = %s", (thread_id))[0][0]
    sql.update_query("UPDATE thread SET isDeleted = %s, posts = %s WHERE id = %s", (status,posts,thread_id))
    sql.update_query("UPDATE post SET isDeleted = %s WHERE thread = %s", (status,thread_id))
    response = {
        "thread": thread_id
    }
    return response


def inc_posts_count(post):
    thread = sql.select_query("SELECT thread FROM post WHERE id = %s", (post, ))
    sql.update_query("UPDATE thread SET posts = posts + 1 WHERE id = %s", (thread[0][0], ))
    return


def dec_posts_count(post):
    thread = sql.select_query("SELECT thread FROM post WHERE id = %s", (post, ))
    try:
        sql.update_query("UPDATE thread SET posts = posts - 1 WHERE id = %s", (thread[0][0], ))
    except Exception as e:
        print(e.message)
    return
