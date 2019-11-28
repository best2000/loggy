from class_all import * #class: loggy, ip, time, http_req

#test logs list
loglist = [loggy("183.88.39.153", "1", "1", "1"), loggy("83.149.9.216", "2", "2", "2"), loggy("65.55.213.73", "2", "2", "2")]

#search from date input
import re
date = input("date search : ")
date = re.split('/', date)

#searching
filtered_loglist = []
for i in loglist:
    if i.time.day == date[0] and i.time.month == date[1] and i.time.year == date[2]:
        filtered_loglist.append(i)

#search result
print("found :", len(filtered_loglist))
print("==============================")

#วันที่นี้นี้เข้ามากี่ไอพี แต่ละไอพีมาจากที่ไหนบนโลก
#check ip geolocation
#use API from "https://freegeoip.app/"


#add attribute lat long to class obj
#ช่วงเวลานี้เข้ามากี่ไอพี
#searh ip ว่ามีเข้ามาไหม
#keep log file info seperate