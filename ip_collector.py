from class_all import ip
import pickle, requests, time, sql_ip

def ip_exist(address): #check exist return True//False 
    if sql_ip.get_ip_by_ip(address) == None:
        return False
    return True

def ip_add(address): #add ip object to database
    exist = ip_exist(address)
    if exist == False:
        while True:
            res = requests.get("http://ip-api.com/json/"+address+"?fields=country,lat,lon")
            if res.status_code == 429:
                #print("\rcode 429 : waiting...", end="")
                continue
            print("")
            break
        info_dict = res.json()
        object = ip()
        object.address = address
        object.country = info_dict['country']
        object.lat = info_dict['lat']
        object.lon = info_dict['lon']
        sql_ip.insert_ip(object)
        #print(object.address)
    elif exist == True:
        sql_ip.update_rec(address)
        #print(address, "+1")

def ip_creator(i):
    object = ip()
    object.address = i[0]
    object.country = i[1]
    object.lat = i[2]
    object.lon = i[3]
    object.visit_rec = i[4]
    return object

def ip_get_object(address):
    tup = sql_ip.get_ip_by_ip(address)
    object = ip()
    object.address = tup[0]
    object.country = tup[1]
    object.lat = tup[2]
    object.lon = tup[3]
    object.visit_rec = tup[4]
    return object






