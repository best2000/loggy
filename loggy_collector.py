import pickle, re, datetime, sql_log, socket
from class_all import *
from ip_collector import *

def loggy_creator(i):
    object = loggy()
    object.default_str = i[0]
    object.ip = i[1]
    object.identity = i[2]
    object.userID = i[3]
    temp = re.split("/", i[4])
    object.datetime = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]), int(temp[5])) 
    object.timezone = i[5]
    object.req = i[6]
    object.status_code = i[7]
    object.return_size = i[8]
    object.referer = i[9]
    object.user_agent = i[10]
    return object

def loggy_all(): #show all loggy object in database
    loggy_list = []
    loglis = sql_log.get_all_log()
    for i in loglis:
        object = loggy_creator(i)
        loggy_list.append(object)
    return loggy_list
              
def loggy_read_log_file(path): #read log line put it into object loggy and save in database RETURN loggy_list
    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 60000))
    with open(path) as log:
        count = len(open(path).readlines())
        for i in range(count):
            text = str(i+1)+'/'+str(count)
            s.send(str.encode(text))
            logline = log.readline()
            temp = re.split('"', logline)
            temp.remove(' ')
            temp.pop()

            #temp[0]-------------------------------------------
            temp[0] = temp[0].replace('[','')
            temp[0] = temp[0].replace(']','')
            temp[0] = re.split(' ', temp[0])
            temp[0][3] = re.split('/', temp[0][3])
            temp[0][3][2] = re.split(':', temp[0][3][2])
            temp[0].remove('')
            
            object = loggy()
            object.default_str = logline
            ip_add(temp[0][0]) #add to ip datbase auto check exist
            object.ip = temp[0][0]
            object.identity = temp[0][1]
            object.userID = temp[0][2]
            for i in range(len(mon)):
                if mon[i] == temp[0][3][1]:
                    month = i+1
                    break
            object.datetime = "{}/{}/{}/{}/{}/{}".format(temp[0][3][2][0], month, temp[0][3][0], temp[0][3][2][1], temp[0][3][2][2], temp[0][3][2][3])
            object.timezone = temp[0][4]
            
            #temp[1]----------------------------------
            object.req = temp[1]

            #temp[2]----------------------------------
            temp[2] = re.split(' ', temp[2])
            temp[2].remove('')
            object.status_code = temp[2][0]
            object.return_size = temp[2][1]

            #temp[3]----------------------------------
            object.referer = temp[3]

            #temp[4]----------------------------------
            object.user_agent = temp[4]

            sql_log.insert_log(object)
    s.send(b'add log finished')
    s.close()
            

