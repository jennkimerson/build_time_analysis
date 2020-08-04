import os
import psycopg2 as pp
import psycopg2.extras as ppx


def get_host():
    host = os.getenv('PGHOST')
    if host is None:
        raise SystemExit('Please set the PGHOST environment')
    return host


def get_ceph_builds():
    host = get_host()
    conn = pp.connect(dbname='public', host=host, port=5433)
    cur = conn.cursor(cursor_factory=ppx.DictCursor)
    # Some builds do not have a start_time, so we will also query the
    # creation_time from the events table.
    postgreSQL_select_Query = """SELECT brew.build.*,brew.events.time
                                    AS creation_time FROM brew.build
                                    INNER JOIN brew.events ON brew.build.create_event=brew.events.id
                                    WHERE brew.build.pkg_id=34590 and brew.build.state = 1
                                    ORDER BY brew.events.id;"""
    # Execute Query
    cur.execute(postgreSQL_select_Query)

    # Selecting rows from brew.task.id table using cursor.fetchall
    return cur.fetchall()
