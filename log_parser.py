import re
import pickle
from class_all import *
from ip_collector import *

loggy_list = []
with open('apache_log.txt') as log:
    count = len(open('apache_log.txt').readlines())
    for i in range(count):
        logline = log.readline()
        temp = re.split('"', logline)
        #for i in temp:
            #print('[1]', i)
        #print("-------------------")
        #remove zone
        temp.remove(' ')
        temp.pop()

        #for i in temp:
            #print('[2]', i)
        
        #temp[0]-------------------------------------------
        #print(temp[0])
        temp[0] = temp[0].replace('[','')
        temp[0] = temp[0].replace(']','')
        temp[0] = re.split(' ', temp[0])
        temp[0][3] = re.split('/', temp[0][3])
        temp[0][3][2] = re.split(':', temp[0][3][2])
        temp[0].remove('')
        #print(temp[0])
        
        object = loggy()
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
        #print(temp[1])
        temp[1] = re.split(' ', temp[1])
        object.http_req.method = temp[1][0]
        object.http_req.path = temp[1][1]
        object.http_req.protocol = temp[1][2]
        #print(temp[1])

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






    #วันที่นี้นี้เข้ามากี่ไอพี แต่ละไอพีมาจากที่ไหนบนโลก