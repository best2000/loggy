import re, datetime
from ip_collector import *
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar

def showLOG():
    listbox.delete(0,'end')
    loggy_list = loggy_all()
    for object in loggy_list:
        listbox.insert('end', object.default_str)

def showIP():
    listbox.delete(0,'end')
    ip_lis = ip_all()
    for object in ip_lis:
        Ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp
        listbox.insert('end', Ip)


def add_log_re():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_rewrite(loggy_list)

def add_log_ap():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_append(loggy_list)

def ip_search_pop():
    def ip_search():
        listbox.delete(0,'end')
        object = ip_get_object(e1.get())
        Ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp
        listbox.insert('end', Ip)
    
    pop = Toplevel()
    pop.title("IP Search..")
    l = Label(pop, text="IP")
    l.grid(row=0, column=0)
    e1 = Entry(pop) 
    e1.grid(row=0, column=1)
    button=Button(pop, text="OK", command=ip_search)
    button.grid(row=0, column=2)

def log_search_ip_pop():
    def log_search_ip():
        listbox.delete(0,'end')
        loggy_list = loggy_search_ip(e1.get())
        for object in loggy_list:
            listbox.insert('end', object.default_str)
    pop = Toplevel()
    pop.title("Log Search by IP..")
    l = Label(pop, text="IP")
    l.grid(row=0, column=0)
    e1 = Entry(pop) 
    e1.grid(row=0, column=1)
    button=Button(pop, text="OK", command=log_search_ip)
    button.grid(row=0, column=2)

def log_search_date_pop():
    def log_search_date():
        listbox.delete(0,'end')
        loggy_list = loggy_search_date(cal.format_date(cal.selection_get()))
        for object in loggy_list:
            listbox.insert('end', object.default_str)

    pop = Toplevel()
    pop.title("Log Search by Date..")
    cal = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, day=17, date_pattern='dd-mm-y')
    cal.grid(row=0, column=0)
    Button(pop, text="ok", command=log_search_date).grid(row=1, column=0)

    datelis = []
    for object in loggy_all():
        date = object.time.day + 
        cal.calevent_create(datetime.date(2015,5,1), 'get log', tags=['log'])

main = Tk()
main.title('Loggy')
Label(main, text='Display').grid(row=0, column=0)
listbox = Listbox(main, width=150, height=20)
listbox.grid(row=1, column=0)
yscroll = Scrollbar(command=listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=1, sticky='ns')
listbox.configure(yscrollcommand=yscroll.set)
menu = Menu(main) 
main.config(menu=menu) 
filemenu = Menu(main) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)
searchmenu = Menu(main)
menu.add_cascade(label='Search', menu=searchmenu)
subsearchmenu = Menu(main)
searchmenu.add_cascade(label='IP', command=ip_search_pop)
searchmenu.add_cascade(label='Log', menu=subsearchmenu)
subsearchmenu.add_cascade(label="Date", command=log_search_date_pop)
subsearchmenu.add_cascade(label="Date-Date")
subsearchmenu.add_cascade(label="IP", command=log_search_ip_pop)
            
button2=Button(main, text="All Log", command=showLOG)
button2.grid(row=0, column=1)
button1=Button(main, text="All IP", command=showIP)
button1.grid(row=0, column=2)
main.mainloop()


#calendar
#plot bar chart top 10 ip, loocation
#add file log
#search for date time to date time
#map plot
