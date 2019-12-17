import re
from ip_collector import *
from loggy_collector import *
from tkinter import *
from tkinter import filedialog


def callback1(selection):
    global a
    a = selection

def callback2(selection):
    global b
    b = selection

def showLOG():
    listbox.delete(0,'end')
    loggy_list = loggy_all()
    for object in loggy_list:
        listbox.insert('end', object.default_str)

def showIP():
    listbox.delete(0,'end')
    ip_lis = ip_all()
    for object in ip_lis:
        Ip = object.address, object.country, object.city, object.lat, object.lon, object.isp
        listbox.insert('end', Ip)

def log_search():
    listbox.delete(0,'end')
    if a == 'Log':
        if b == 'date':
            loggy_list = loggy_search_date(e1.get())
            for object in loggy_list:
                listbox.insert('end', object.default_str)
        elif b == 'date-date':
            loggy_list = loggy_search_datedur(e1.get())
            for object in loggy_list:
                listbox.insert('end', object.default_str)
        elif b == 'IP':
            loggy_list = loggy_search_ip(e1.get())
            for object in loggy_list:
                print(object.default_str)
                listbox.insert('end', object.default_str)
    else:
        listbox.insert('end', 'ERROR')



def add_log_re():
    tk.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(tk.filename)
    loggy_database_rewrite(loggy_list)

def add_log_ap():
    tk.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(tk.filename)
    loggy_database_append(loggy_list)

def ip_search_pop():
    def ip_search():
        listbox.delete(0,'end')
        object = ip_get_object(e1.get())
        Ip = object.address, object.country, object.city, object.lat, object.lon, object.isp
        listbox.insert('end', Ip)
    
    pop = Toplevel()
    pop.wm_title("Search..")
    l = Label(pop, text="IP")
    l.grid(row=0, column=0)
    e1 = Entry(pop) 
    e1.grid(row=0, column=1)
    button=Button(pop, text="OK", command=ip_search)
    button.grid(row=0, column=2)

tk = Tk()
tk.title('Loggy')
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
listbox = Listbox(tk, width=150, height=20)
listbox.grid(row=1, column=0)
yscroll = Scrollbar(command=listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=1, sticky='ns')
listbox.configure(yscrollcommand=yscroll.set)
menu = Menu(tk) 
tk.config(menu=menu) 
filemenu = Menu(tk) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)
searchmenu = Menu(tk)
menu.add_cascade(label='Search', menu=searchmenu)
subsearchmenu = Menu(tk)
searchmenu.add_cascade(label='IP', command=ip_search_pop)
searchmenu.add_cascade(label='Log', menu=subsearchmenu)
for name in ("Date", "Date-Date", "IP"):
            subsearchmenu.add_cascade(label=name)
button2=Button(tk, text="All Log", command=showLOG)
button2.grid(row=0, column=6)
button1=Button(tk, text="All IP", command=showIP)
button1.grid(row=0, column=7)
tk.mainloop()


#calendar
#plot bar chart top 10 ip, loocation
#add file log
#search for date time to date time
#map plot
