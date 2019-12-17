import pickle, re, datetime
from class_all import *
from ip_collector import *

def loggy_all(): #show all loggy object in database
    loggy_list = []
    with open('class_loggy_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) 
                loggy_list.append(object)
        except:
            return loggy_list

def loggy_show_loggy(loggy_list):
    for object in loggy_list:
        print(object.default_str)

def loggy_search_date(date): #datetime.date
    filtered_loggylist = []
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if object.datetime.day == date.day and object.datetime.month == date.month and object.datetime.year == date.year:
                    filtered_loggylist.append(object)
        except: pass
    return filtered_loggylist

def loggy_search_datedur(dt1, dt2): #datetime - datetime 
    #searching
    filtered_loggylist = []
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if (object.datetime.year >= dt1.year and object.datetime.year <= dt2.year 
                and object.datetime.month >= dt1.month and object.datetime.month <= dt2.month
                and object.datetime.day >= dt1.day and object.datetime.day <= dt2.day
                and object.datetime.hour >= dt1.hour and object.datetime.hour <= dt2.hour
                and object.datetime.minute >= dt1.minute and object.datetime.minute <= dt2.minute
                and object.datetime.second >= dt1.second and object.datetime.second <= dt2.second):
                    filtered_loggylist.append(object)
        except: pass
    return filtered_loggylist

def loggy_search_ip(ip):
    #searching
    filtered_loggylist = []
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if object.ip.address == ip:
                    filtered_loggylist.append(object)
        except: pass
    return filtered_loggylist

def loggy_database_append(loggy_list): #add loggy object to database
    for object in loggy_list:
        with open('class_loggy_obj.pickle', 'ab') as file:
            pickle.dump(object, file)

def loggy_database_rewrite(loggy_list):
    for i in range(len(loggy_list)): #replace object in dummy list to database file
        if i == 0:
            with open('class_loggy_obj.pickle', 'wb') as file:
                pickle.dump(loggy_list[i], file)
        else:
            with open('class_loggy_obj.pickle', 'ab') as file:
                pickle.dump(loggy_list[i], file)
                
def loggy_read_log_file(path): #read log line put it into object loggy and save in database RETURN loggy_list
    loggy_list = []
    with open(path) as log:
        count = len(open(path).readlines())
        for i in range(count):
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
            object.ip = ip_get_object(temp[0][0])
            object.identity = temp[0][1]
            object.userID = temp[0][2]
            mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            for i in range(len(mon)):
                if mon[i] == temp[0][3][1]:
                    month = i+1
                    break
            object.datetime = datetime.datetime(int(temp[0][3][2][0]), month, int(temp[0][3][0]), int(temp[0][3][2][1]), int(temp[0][3][2][2]), int(temp[0][3][2][3]))
            object.timezone = temp[0][4]
            
            #temp[1]----------------------------------
            temp[1] = re.split(' ', temp[1])
            object.http_req.method = temp[1][0]
            object.http_req.path = temp[1][1]
            object.http_req.protocol = temp[1][2]

            #temp[2]----------------------------------
            temp[2] = re.split(' ', temp[2])
            temp[2].remove('')
            object.status_code = temp[2][0]
            object.return_size = temp[2][1]

            #temp[3]----------------------------------
            object.referer = temp[3]

            #temp[4]----------------------------------
            object.user_agent = temp[4]

            loggy_list.append(object)

    return(loggy_list)