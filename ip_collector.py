from class_all import ip
import pickle
import requests

def ip_exist(address): #check exist return True//False
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                if object.address == address:
                    return True
        except:
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
        ip_lis = ip_all()
        for i in range(len(ip_lis)):
            if ip_lis[i].address == address:
                ip_lis[i].visit_rec += 1
                print(ip_lis[i].address, str(ip_lis[i].visit_rec)+'+1')
                break
        with open('class_ip_obj.pickle', 'wb') as file:
            for object in ip_lis:
                pickle.dump(object, file)

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

def sort_by_visit_rec(ip_lis):
    iprec_dic = {}
    for object in ip_lis:
        iprec_dic[object.address] = object.visit_rec
    iprec_dic_sorted = {k: v for k, v in sorted(iprec_dic.items(), key=lambda iprec_dic: iprec_dic[1], reverse=True)}
    return iprec_dic_sorted

def top_country(ip_lis):
    country_dic = {}
    for object in ip_lis:
        try:
            country_dic[object.country] += 1
            continue
        except: pass
        country_dic[object.country] = 1

    country_dic_sorted = {k: v for k, v in sorted(country_dic.items(), key=lambda country_dic: country_dic[1], reverse=True)}
    return country_dic_sorted

def ip_only(loggy_lis):
    ip_lis = []
    for object in loggy_lis:
        ip_lis.append(object.ip)
    return ip_lis