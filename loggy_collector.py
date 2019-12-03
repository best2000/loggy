from class_all import *
import pickle
import re
import time

def loggy_add(object): #add ip object to database
    with open('class_loggy_obj.pickle', 'ab') as file:
        pickle.dump(object, file)

def loggy_rewrite(loggy_list):
    for i in range(len(loggy_list)): #replace object in dummy list to database file
        if i == 0:
            with open('class_loggy_obj.pickle', 'wb') as file:
                pickle.dump(loggy_list[i], file)
        else:
            with open('class_loggy_obj.pickle', 'ab') as file:
                pickle.dump(loggy_list[i], file)

def loggy_show_info_all(): #show all loggy object in database
    with open('class_loggy_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) 
                print(object.default_str)
        except:
            pass

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
        except:
            pass
    #search result
    print("found :", len(filtered_loggylist))
    time.sleep(3)
    for object in filtered_loggylist:
        print(object.default_str)

def loggy_search_ip(ip):
    #searching
    filtered_loggylist = []
    with open('class_loggy_obj.pickle', 'rb') as file: #read class loggy objects from file
        try:
            while True:
                object = pickle.load(file) 
                if object.ip.address == ip:
                    filtered_loggylist.append(object)
        except:
            pass
    #search result
    print("found :", len(filtered_loggylist))
    time.sleep(3)
    for object in filtered_loggylist:
        print(object.default_str)

def loggy_search_timedu(start, stop): #16/May/2015_15:00:00 16/May/2015_16:00:00
    start = re.split('_', start)
    start_date = start[0]
    start_time = start[1]
    stop = re.split('_', stop)
    stop_date = stop[0]
    stop_time = stop[1]

    start_date = re.split('/', start_date)
    start_day = start_date[0]
    start_month = start_date[1]
    start_year = start_date[2]
    start_time = re.split(':', start_time)
    start_hour = start_time[0]
    start_minute = start_time[1]
    start_second = start_time[2]

    stop_date = re.split('/', stop_date)
    stop_day = stop_date[0]
    stop_month = stop_date[1]
    stop_year = stop_date[2]
    stop_time = re.split(':', stop_time)
    stop_hour = stop_time[0]
    stop_minute = stop_time[1]
    stop_second = stop_time[2]

