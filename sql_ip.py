import sqlite3

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

def ip_exist(address): #check exist return True//False 
    if get_ip_by_ip(address) == None:
        return False
    return True

with sqlite3.connect('ip.db') as con:
    c = con.cursor()
    try:
        c.execute("""CREATE TABLE ip (
                    address text,
                    country text,
                    lat integer,
                    lon integer
                    )""")
        con.commit()
    except: pass



