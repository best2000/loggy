import sqlite3

def get_all_log():
    with sqlite3.connect('log.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM log")
    return c.fetchall()

def rollback(atime):
    with sqlite3.connect('log.db') as con:
            c = con.cursor()
            c.execute("DELETE FROM log where atime = '{}'".format(atime))
            con.commit()

with sqlite3.connect('log.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE log (
                    ip text,
                    identity text,
                    userID text,
                    datetime text,
                    timezone text,
                    req text,
                    status_code text,
                    return_size text,
                    referer text,
                    user_agent text,
                    atime text
                    )""")
        con.commit()
    except: pass



