from data_provider import sql


def save_subscription(email, thread_id):
    sql.update_query('INSERT INTO subscription (thread, user) VALUES (%s, %s)', (thread_id, email, ))
    subscription = sql.select_query(
        'select thread, user FROM subscription WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def remove_subscription(email, thread_id):
    try:
        sql.update_query('DELETE FROM subscription WHERE user = %s AND thread = %s', (email, thread_id, ))
    except Exception:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    return
