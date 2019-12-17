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

def ip_search():
    def ip_search():
        listbox.delete(0,'end')
        object = ip_get_object(e1.get())
        Ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp
        listbox.insert('end', Ip)
    la.configure(text='IP Search')
    la.grid() 
    e1.grid()
    button.configure(text="OK", command=ip_search)
    button.grid()

def log_search_ip():
    def log_search_ip():
        listbox.delete(0,'end')
        loggy_list = loggy_search_ip(e1.get())
        for object in loggy_list:
            listbox.insert('end', object.default_str)
    la.configure(text='Log Search by IP')
    la.grid() 
    e1.grid()
    button.configure(text="OK", command=log_search_ip)
    button.grid()

def log_search_date_pop():
    def log_search_date():
        listbox.delete(0,'end')
        loggy_list = loggy_search_date(cal.selection_get())
        for object in loggy_list:
            listbox.insert('end', object.default_str)

    pop = Toplevel()
    pop.title("Log Search by Date")
    cal = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, font="Arial 14")
    cal.grid(row=0, column=0)
    Button(pop, text="OK", command=log_search_date, font="Arial 14").grid(row=1, column=0)
    #hilight date
    datelis = []
    for object in loggy_all():
        obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
        if obj_date not in datelis:
            datelis.append(obj_date)
            cal.calevent_create(obj_date, 'log', tags=['log'])

def log_search_datedur_pop():
    def log_search_datedur():
        listbox.delete(0,'end')
        d1 = cal1.selection_get()
        t1 = re.split(':', e1.get())
        dt1 = datetime.datetime(d1.year, d1.month, d1.day, int(t1[0]), int(t1[1]), int(t1[2])) 
        d2 = cal2.selection_get()
        t2 = re.split(':', e2.get())
        dt2 = datetime.datetime(d2.year, d2.month, d2.day, int(t2[0]), int(t2[1]), int(t2[2])) 
        loggy_list = loggy_search_datedur(dt1, dt2)
        for object in loggy_list:
            listbox.insert('end', object.default_str)

    pop = Toplevel()
    pop.title("Log Search by Datetime-Datetime")
    Label(pop, text=" TO ", font="Arial 14").grid(row=0, column=3)
    e1 = Entry(pop, width=7, font="Arial 14") 
    e1.grid(row=1, column=1)
    e1.insert(END, '00:00:00')
    e2 = Entry(pop, width=7, font="Arial 14") 
    e2.grid(row=1, column=5)
    e2.insert(END, '00:00:00')
    Button(pop, text="OK", command=log_search_datedur, font="Arial 14").grid(row=2, column=3)
    cal1 = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, font="Arial 14")
    cal1.grid(row=0, column=0, columnspan=3)
    datelis = [] 
    for object in loggy_all():
        obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
        if obj_date not in datelis:
            datelis.append(obj_date)
            cal1.calevent_create(obj_date, 'log', tags=['log'])
    cal2 = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, font="Arial 14")
    cal2.grid(row=0, column=4, columnspan=3)
    datelis = [] 
    for object in loggy_all():
        obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
        if obj_date not in datelis:
            datelis.append(obj_date)
            cal2.calevent_create(obj_date, 'log', tags=['log'])

main = Tk()
main.title('Loggy')

la = Label(main, text="")
la.grid(row=0, column=0)
e1 = Entry(main, width=70) 
e1.grid(row=0, column=1)
e1.grid_remove()
button = Button(main, text="OK")
button.grid(row=0, column=2)
button.grid_remove()

listbox = Listbox(main, width=150, height=20)
listbox.grid(row=1, column=0, columnspan=3)
yscroll = Scrollbar(command=listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=3, sticky='ns')
listbox.configure(yscrollcommand=yscroll.set)



menu = Menu(main) 
main.config(menu=menu) 
filemenu = Menu(main) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)

showallmenu = Menu(main)  
menu.add_cascade(label='Show All', menu=showallmenu)
showallmenu.add_cascade(label='Log', command=showLOG)
showallmenu.add_cascade(label='IP', command=showIP)

searchmenu = Menu(main)
menu.add_cascade(label='Search', menu=searchmenu)
subsearchmenu = Menu(main)
searchmenu.add_cascade(label='Log', menu=subsearchmenu)
subsearchmenu.add_cascade(label="Date", command=log_search_date_pop)
subsearchmenu.add_cascade(label="Datetime-Datetime", command=log_search_datedur_pop)
subsearchmenu.add_cascade(label="IP", command=log_search_ip)
searchmenu.add_cascade(label='IP', command=ip_search)

main.mainloop()

#plot bar chart top 10 ip loocation
#map plot