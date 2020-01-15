import sqlite3

def insert_his(tup):
    with sqlite3.connect('lhis.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO lhis VALUES ('{}', '{}', {})".format(tup[0], tup[1], tup[2]))
        con.commit()

def get_all_his():
    with sqlite3.connect('lhis.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM lhis")
    return c.fetchall()

def rollback(atime):
    with sqlite3.connect('lhis.db') as con:
        c = con.cursor()
        c.execute("DELETE FROM lhis WHERE atime = '{}'".format(atime))
        con.commit()



with sqlite3.connect('lhis.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE lhis (atime text,
                    name text,
                    line integer
                    )""")
        con.commit()
    except: pass