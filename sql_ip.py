import sqlite3


def insert_ip(object):
    with sqlite3.connect('ip.db') as con:
        c = con.cursor()
        c.execute("INSERT INTO ip VALUES ('{}', '{}', {}, {}, {})".format(object.address, object.country, object.lat, object.lon, object.visit_rec))
        con.commit()


def get_ip_by_ip(address):
    with sqlite3.connect('ip.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM ip WHERE address='{}'".format(address))
    return c.fetchone()

def get_all_ip():
    with sqlite3.connect('ip.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM ip")
    return c.fetchall()

def get_ip_rec_sort():
    with sqlite3.connect('ip.db') as con:
        c = con.cursor()
        c.execute("SELECT * FROM ip ORDER BY visit_rec DESC LIMIT 10")
    return c.fetchall()

def update_rec(address):
    with sqlite3.connect('ip.db') as con:
        c = con.cursor()
        c.execute("SELECT visit_rec FROM ip WHERE address='{}'".format(address))
        v = c.fetchone()[0]
        v = v+1 
        c.execute("UPDATE ip SET visit_rec={} WHERE address='{}'".format(v, address))
    

with sqlite3.connect('ip.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE ip (
                    address text,
                    country text,
                    lat integer,
                    lon integer,
                    visit_rec integer
                    )""")
        con.commit()
    except: pass



