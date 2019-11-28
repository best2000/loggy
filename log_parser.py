from class_all import * #class: loggy, ip, time, http_req
import re


with open('apache_log.txt') as log:
    logline = log.readline()
    logobj = loggy()
    temp = re.split('"', logline)
    for i in temp:
        print('[1]', i)
    print("-------------------")
    #remove zone
    temp.remove(' ')
    temp.remove('\n')

    for i in temp:
        print('[2]', i)
    
    #temp[0]-------------------------------------------
    #print(temp[0])
    temp[0] = temp[0].replace('[','')
    temp[0] = temp[0].replace(']','')
    temp[0] = re.split(' ', temp[0])
    temp[0][3] = re.split('/', temp[0][3])
    temp[0][3][2] = re.split(':', temp[0][3][2])
    temp[0].remove('')
    #print(temp[0])
    #check ip info from ip_database if not add new ip info 
    temp[0][0] # this is ip adress
    ###################

    logobj.identity = temp[0][1]
    logobj.userID = temp[0][2]
    logobj.time.day = temp[0][3][0]
    logobj.time.month = temp[0][3][1]
    logobj.time.year = temp[0][3][2][0]
    logobj.time.hour = temp[0][3][2][1]
    logobj.time.minute = temp[0][3][2][2]
    logobj.time.second = temp[0][3][2][3]
    logobj.time.zone = temp[0][4]
    print(logobj.time.zone)

    #temp[1]----------------------------------
    #print(temp[1])
    temp[1] = re.split(' ', temp[1])
    logobj.http_req.method = temp[1][0]
    logobj.http_req.path = temp[1][1]
    logobj.http_req.protocol = temp[1][2]
    #print(temp[1])

    #add loggy obj write it to history file











   