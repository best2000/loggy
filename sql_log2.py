import sqlite3

def get_all_log():
    with sqlite3.connect('log2.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM log")
    return c.fetchall()

def rollback(atime):
    with sqlite3.connect('log2.db') as con:
            c = con.cursor()
            c.execute("DELETE FROM log where atime = '{}'".format(atime))
            con.commit()

with sqlite3.connect('log2.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE log (
                    ip text,
                    datetime text,
                    atime text
                    )""")
        con.commit()
    except: pass