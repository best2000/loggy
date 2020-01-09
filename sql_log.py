import sqlite3


def insert_log(object):
    with sqlite3.connect('log.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO log VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(object.default_str, object.ip, 
                    object.identity,
                    object.userID,
                    object.datetime,
                    object.timezone,
                    object.req,
                    object.status_code,
                    object.return_size,
                    object.referer,
                    object.user_agent))
        con.commit()

def get_all_log():
    with sqlite3.connect('log.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM log")
    return c.fetchall()




    

with sqlite3.connect('log.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE log (
                    default_str text,
                    ip text,
                    identity text,
                    userID text,
                    datetime text,
                    timezone text,
                    req text,
                    status_code text,
                    return_size text,
                    referer text,
                    user_agent text
                    )""")
        con.commit()
    except: pass



