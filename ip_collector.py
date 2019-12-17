from class_all import ip
import pickle
import requests

def ip_exist(address): #check exist return True//False
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                if object.address == address:
                    print("exist :", object.address)
                    return True
        except:
            print("not exist :", address)
            return False

def ip_add(address): #add ip object to database
    exist = ip_exist(address)
    if exist == False:
        while True:
            res = requests.get("http://ip-api.com/json/"+address+"?fields=country,city,lat,lon,isp")
            if res.status_code == 429:
                print("code 429 : waiting...")
                continue
            break
        info_dict = res.json()
        object = ip()
        object.address = address
        object.country = info_dict['country']
        object.city = info_dict['city']
        object.lat = info_dict['lat']
        object.lon = info_dict['lon']
        object.isp = info_dict['isp']
        with open('class_ip_obj.pickle', 'ab') as file:
            pickle.dump(object, file)
        print("ip added :", object.address, object.country, object.city, object.lat, object.lat, object.lon, object.isp)
    elif exist == True:
        print(address, "is already exist")
    else:
        print("error!")

def ip_remove(address):
    ip_list = [] #dummy list
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                ip_list.append(object)
        except:
            pass
    for i in ip_list: #delete from dummy list
            if i.address == address:
                ip_list.remove(i)
    for i in range(len(ip_list)): #replace ip object in dummy list to database file
        if i == 0:
            with open('class_ip_obj.pickle', 'wb') as file:
                pickle.dump(ip_list[i], file)
        else:
            with open('class_ip_obj.pickle', 'ab') as file:
                pickle.dump(ip_list[i], file)
    print("ip removed :", address)

def ip_all(): #show all ip object in database
    ip_lis = []
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                ip_lis.append(object)
        except:
            return ip_lis

def ip_get_object(address):
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                if object.address == address:
                    return object
        except:
            print(address, "is not exist")

#gui