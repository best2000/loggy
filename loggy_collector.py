import pickle, re
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

def loggy_search_date(date):
    #search from date input
    date = re.split('/', date)
    #searching
    filtered_loggylist = []
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if object.time.day == date[0] and object.time.month == date[1] and object.time.year == date[2]:
                    filtered_loggylist.append(object)
        except: pass
    return filtered_loggylist

def loggy_search_datedur(datedur): #16-17/May/2015 
    #search from date input
    datedur = re.split('/', datedur)
    datedur[0] = re.split('-', datedur[0])
    print(datedur)
    #check this date make sense
    if datedur[0][0] > datedur[0][1]: 
        return None
    elif datedur[0][0] == datedur[0][1]:
        loggy_search_date(datedur[0][0]+'/'+datedur[1]+'/'+datedur[2])
        return None
    #searching
    filtered_loggylist = []
    day_target = []
    for i in range(int(datedur[0][0]), int(datedur[0][1])+1):
        day_target.append(str(i))
    print(day_target)
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if object.time.day in day_target and object.time.month == datedur[1] and object.time.year == datedur[2]:
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
            object.time.day = temp[0][3][0]
            object.time.month = temp[0][3][1]
            object.time.year = temp[0][3][2][0]
            object.time.hour = temp[0][3][2][1]
            object.time.minute = temp[0][3][2][2]
            object.time.second = temp[0][3][2][3]
            object.time.zone = temp[0][4]
            
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