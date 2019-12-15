import re
from ip_collector import *
from loggy_collector import *
from tkinter import *


def callback1(selection):
    global a
    a = selection

def callback2(selection):
    global b
    b = selection

tk = Tk() 
Label(tk, text='Search').grid(row=0, column=0) 
Label(tk, text='by').grid(row=0, column=2) 
select1 = StringVar(tk)
select1.set(" ") # default value
selected1 = OptionMenu(tk, select1, "Log", "IP", command=callback1)
selected1.grid(row=0, column=1)
select2 = StringVar(tk)
select2.set(" ") # default value
selected2 = OptionMenu(tk, select2, "date", "date-date", "IP", command=callback2)
selected2.grid(row=0, column=3)
e1 = Entry(tk) 
e1.grid(row=0, column=4)
listbox = Listbox(tk, width=150, height=20)
listbox.grid(row=1, column=0)
yscroll = Scrollbar(command=listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=1, sticky='ns')
listbox.configure(yscrollcommand=yscroll.set)
with open('class_loggy_obj.pickle', 'rb') as file:
        try:
            while True:
                object = pickle.load(file) 
                listbox.insert('end', object.default_str)
        except:
            pass

listbox.delete(0,'end')
listbox.insert('end','ew')

def search():
    listbox.delete(0,'end')
    if a == 'Log':
        if b == 'date':
            pass
button1=Button(tk, text="OK", command=search)
button1.grid(row=0, column=5)

def showLOG():
    listbox.delete(0,'end')
    with open('class_loggy_obj.pickle', 'rb') as file:
        try:
            while True:
                object = pickle.load(file) 
                listbox.insert('end', object.default_str)
        except:
            pass
button2=Button(tk, text="All Log", command=showLOG)
button2.grid(row=0, column=6)

def showIP():
    listbox.delete(0,'end')
    with open('class_ip_obj.pickle', 'rb') as file:     
        try:
            while True:
                object = pickle.load(file) #class ip object
                listbox.insert('end', object.address, object.country, object.city, object.lat, object.lon, object.isp,' ')
        except:
            pass


button1=Button(tk, text="All IP", command=showIP)
button1.grid(row=0, column=7)

tk.mainloop()