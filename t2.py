import re, datetime, tkinter
from ip_collector import *
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ip_collector import *

def loggy_searchby_ip(event):
    listbox_log.delete(0,'end')
    if entry_log.get() == "":
        loggy_list = loggy_all() #setup
        for object in loggy_list:
            listbox_log.insert('end', object.default_str)
    else:
        loggy_list = loggy_search_ip(entry_log.get())
        for object in loggy_list:
            listbox_log.insert(0, object.default_str)

def entry_log_fin(event):
    entry_log.delete(0, 'end')

def entry_log_fout(event):
    entry_log.delete(0, 'end')
    entry_log.insert(0, '<logs search by ip>')

def ip_search(event):
    listbox_ip.delete(0,'end')
    if entry_ip.get() == "":
        ip_lis = ip_all()
        for object in ip_lis:
            ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
            listbox_ip.insert('end', ip)
    else:
        object = ip_get_object(entry_ip.get())
        listbox_ip.insert(0, 'Address: '+object.address, 'Country: '+object.country, 'City: '+object.city, 'Lat: '+str(object.lat), 'Lon: '+str(object.lon), 'Isp: '+object.isp, 'Rec: '+str(object.visit_rec))

def entry_ip_fin(event):
    entry_ip.delete(0, 'end')

def entry_ip_fout(event):
    entry_ip.delete(0, 'end')
    entry_ip.insert(0, '<ip search>')

def log_search_date():
    listbox_log.delete(0,'end')
    loggy_list = loggy_search_date(cal.selection_get())
    for object in loggy_list:
        listbox_log.insert('end', object.default_str)

def date_fill(event):
    label_date.configure(text='Date: '+cal.format_date(cal.selection_get()))

def log_search_datedur_pop():
    def log_search_datedur():
        listbox_log.delete(0,'end')
        d1 = cal1.selection_get()
        t1 = re.split(':', e1.get())
        dt1 = datetime.datetime(d1.year, d1.month, d1.day, int(t1[0]), int(t1[1]), int(t1[2])) 
        d2 = cal2.selection_get()
        t2 = re.split(':', e2.get())
        dt2 = datetime.datetime(d2.year, d2.month, d2.day, int(t2[0]), int(t2[1]), int(t2[2])) 
        loggy_list = loggy_search_datedur(dt1, dt2)
        for object in loggy_list:
            listbox_log.insert('end', object.default_str)

    pop = Toplevel()
    pop.title("Log Search by Datetime-Datetime")
    Label(pop, text=" TO ").grid(row=0, column=3)
    e1 = Entry(pop, width=7) 
    e1.grid(row=1, column=1)
    e1.insert(END, '00:00:00')
    e2 = Entry(pop, width=7) 
    e2.grid(row=1, column=5)
    e2.insert(END, '00:00:00')
    Button(pop, text="Submit", command=log_search_datedur).grid(row=2, column=3)
    cal1 = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
    cal1.grid(row=0, column=0, columnspan=3)
    datelis = [] 
    for object in loggy_all():
        obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
        if obj_date not in datelis:
            datelis.append(obj_date)
            cal1.calevent_create(obj_date, 'log', tags=['log'])
    cal2 = Calendar(pop, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
    cal2.grid(row=0, column=4, columnspan=3)
    datelis = [] 
    for object in loggy_all():
        obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
        if obj_date not in datelis:
            datelis.append(obj_date)
            cal2.calevent_create(obj_date, 'log', tags=['log'])

def add_log_re():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_rewrite(loggy_list)

def add_log_ap():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_append(loggy_list)

root = Tk()
root.title('Loggy')
#menubar##########################################
menu = Menu(root) 
root.config(menu=menu) 
filemenu = Menu(root) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)
#loggy############################################
frame_log = LabelFrame(root, text="Logs")
frame_log.grid(row=0, column=0)

listbox_log = Listbox(frame_log, width=70, height=17)
listbox_log.grid(row=0, column=0)
Scrollbar(frame_log, command=listbox_log.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

###search###
frame_log_search = LabelFrame(frame_log, text="Log Search")
frame_log_search.grid(row=0, column=2)

entry_log = Entry(frame_log_search)
entry_log.grid(row=0, column=0, columnspan=2, sticky='ew')
entry_log.insert(0, '<logs search by ip>')
entry_log.bind('<FocusIn>', entry_log_fin)
entry_log.bind('<FocusOut>', entry_log_fout)
entry_log.bind('<Return>', loggy_searchby_ip) #widget.bind("<Key>", key)
   
cal = Calendar(frame_log_search, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
cal.grid(row=1, column=0, columnspan=2)
cal.bind('<Leave>', date_fill)
datelis = [] #hilight date
for object in loggy_all():
    obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
    if obj_date not in datelis:
        datelis.append(obj_date)
        cal.calevent_create(obj_date, 'log', tags=['log'])

label_date = Label(frame_log_search, text='Date:<pick one>')
label_date.grid(row=2, column=0)
Button(frame_log_search, text='Submit', command=log_search_date).grid(row=2, column=1)

Button(frame_log_search, text='Search by Date-Date', command=log_search_datedur_pop).grid(row=3, column=0)

loggy_list = loggy_all() #setup
for object in loggy_list:
    listbox_log.insert('end', object.default_str)
#ip#############################################
frame_ip = LabelFrame(root, text="IP Database")
frame_ip.grid(row=0, column=1, sticky='ns')

listbox_ip = Listbox(frame_ip, width=70, height=15)
listbox_ip.grid(row=1, column=0, columnspan=1)
Scrollbar(frame_ip, command=listbox_ip.yview, orient=VERTICAL).grid(row=1, column=2, sticky='ns')

entry_ip = Entry(frame_ip)
entry_ip.grid(row=0, column=0, sticky='we')
entry_ip.bind('<Return>', ip_search) #widget.bind("<Key>", key)
entry_ip.insert(0, '<ip search>')
entry_ip.bind('<FocusIn>', entry_ip_fin)
entry_ip.bind('<FocusOut>', entry_ip_fout)

ip_lis = ip_all() #setup
for object in ip_lis:
    ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
    listbox_ip.insert('end', ip)
#plot################################################
frame_plot = LabelFrame(root, text="Top")
frame_plot.grid(row=1, column=0, sticky='w')

loggylis = sort_by_visit_rec()
ip_rec = [[]]
n = 1
nex = 0
for i in range(len(loggylis)):
    try:
        if loggylis[i-1].visit_rec > loggylis[i].visit_rec:
            n += 1
            nex = 1
    except: pass
    if n == 11:
        break
    if nex == 1:
        ip_rec.append([loggylis[i]])
        nex = 0
    else:
        ip_rec[-1].append(loggylis[i])
top = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rec = []
for lis in ip_rec:
    rec.append(lis[0].visit_rec)

fig = plt.Figure(figsize=(6,5), dpi=75)
pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Visited")
pl.bar(top, rec)
pltk = FigureCanvasTkAgg(fig, frame_plot)
pltk.get_tk_widget().grid(row=0, column=0)

frame_plot_lisbox = LabelFrame(frame_plot, text="Top 10 ip")
frame_plot_lisbox.grid(row=0, column=1, sticky='n')
listbox_top = Listbox(frame_plot_lisbox, width=20, height=22)
listbox_top.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox, command=listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, lis in enumerate(ip_rec):
    listbox_top.insert('end', str(i+1)+". "+lis[0].address)

root.mainloop()

#plot bar chart top 10 loocation
#map plot