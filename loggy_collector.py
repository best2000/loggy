import pickle, re, datetime, sql_log, socket, sql_ip, requests
import sqlite3

def loggy_read_log_file(path): #read log line put it into object loggy and save in database RETURN loggy_list
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 60000))
    mon = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    with sqlite3.connect('log.db') as con:
        c = con.cursor()
        with sqlite3.connect('ip.db') as con2:
            c2 = con2.cursor()
            with open(path, 'r') as log:
                count = len(open(path).readlines())
                for i in range(count):
                    text = str(i+1)+'/'+str(count)
                    s.send(str.encode(text))
                    logline = log.readline()
                    temp = re.split('"', logline)
                    temp.remove(' ')
                    temp.pop()
                    temp[0] = temp[0].replace('[','')
                    temp[0] = temp[0].replace(']','')
                    temp[0] = re.split(' ', temp[0])
                    temp[0][3] = re.split('/', temp[0][3])
                    temp[0][3][2] = re.split(':', temp[0][3][2])
                    temp[0].remove('')
                    exist = sql_ip.ip_exist(temp[0][0])
                    if exist == False:
                        while True:
                            res = requests.get("http://ip-api.com/json/"+temp[0][0]+"?fields=country,lat,lon")
                            if res.status_code == 429:
                                #print("\rcode 429 : waiting...", end="")
                                continue
                            print("")
                            break
                        info_dict = res.json()
                        c2.execute("INSERT INTO ip VALUES ('{}', '{}', {}, {}, {})".format(temp[0][0], info_dict['country'], info_dict['lat'], info_dict['lon'], 1))
                    else:
                        c2.execute("SELECT visit_rec FROM ip WHERE address='{}'".format(temp[0][0]))
                        v = c2.fetchone()[0]
                        v = v+1 
                        c2.execute("UPDATE ip SET visit_rec={} WHERE address='{}'".format(v, temp[0][0]))
                    month = mon[temp[0][3][1]]       
                    temp[2] = re.split(' ', temp[2])
                    temp[2].remove('')
                    c.execute("INSERT INTO log VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(logline, temp[0][0], 
                                        temp[0][1],
                                        temp[0][2],
                                        "{}/{}/{}/{}/{}/{}".format(temp[0][3][2][0], month, temp[0][3][0], temp[0][3][2][1], temp[0][3][2][2], temp[0][3][2][3]),
                                        temp[0][4],
                                        temp[1],
                                        temp[2][0],
                                        temp[2][1],
                                        temp[3],
                                        temp[4]))
            con2.commit()
        con.commit()
    s.send(b'add log finished')
    s.close()


#def 15796