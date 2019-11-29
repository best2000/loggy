from class_all import *
import pickle

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

def loggy_show_info_all(): #show all ip object in database
    with open('class_loggy_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                print(object.default_str)
        except:
            pass


loggy_show_info_all()