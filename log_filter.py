class time:
    def __init__(self, date, month, year):    
        self.day = date
        self.month = month
        self.year = year
class loggy:
    def __init__(self, ip, date, month, year):
        self.ip = ip
        self.time = time(date, month, year)

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
import requests

for i in filtered_loglist:
    url = "https://freegeoip.app/json/" + i.ip

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers)

    resdict = response.json() #convert JSON string response to dict 
    for i in resdict:
        print(i, ":", resdict[i])
    print("------------------------------")

