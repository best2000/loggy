import re, datetime, tkinter
from ip_collector import *
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ip_collector import *
from tkinter import ttk

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

def add_log_re():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_rewrite(loggy_list)

def add_log_ap():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    loggy_list = loggy_read_log_file(filepath)
    loggy_database_append(loggy_list)

def check(event):
    if fil_mode.get() == "Date-Date":
        e1.configure(state='normal')
        e2.configure(state='normal')
        cal2.configure(state='normal')
    else:
        e1.configure(state='disabled')
        e2.configure(state='disabled')
        cal2.configure(state='disabled')

def replot(loggy_list):
    #replot######
    ##ip plot
    try: pltk.get_tk_widget().destroy()
    except: pass
    iprec_dic_sorted = sort_by_visit_rec(ip_only(loggy_list))
    top = [i+1 for i in range(10)]
    rec = []
    for i, k in enumerate(iprec_dic_sorted):
        try:
            if iprec_dic_sorted[k] == rec[-1]:
                continue
        except: pass
        rec.append(iprec_dic_sorted[k])
    
    fig = plt.Figure(figsize=(6,5), dpi=75)
    pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
    pl.bar(top, rec[:10])
    pltk = FigureCanvasTkAgg(fig, frame_plot)
    pltk.get_tk_widget().grid(row=0, column=0)

    frame_plot_lisbox = LabelFrame(frame_plot, text="IP Ranking")
    frame_plot_lisbox.grid(row=0, column=1, sticky='ns')
    listbox_top = Listbox(frame_plot_lisbox, width=20, height=22)
    listbox_top.grid(row=0, column=0)
    Scrollbar(frame_plot_lisbox, command=listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

    listbox_top.delete(0,'end')
    for i, k in enumerate(iprec_dic_sorted):
        listbox_top.insert('end', str(i+1)+". "+k)
    ##country plot
    try: pltk2.get_tk_widget().destroy()
    except: pass
    country_dic_sorted = top_country(ip_only(loggy_list))
    c_rec = []
    for i, k in enumerate(country_dic_sorted):
        try:
            if country_dic_sorted[k] == c_rec[-1]:
                continue
        except: pass
        c_rec.append(country_dic_sorted[k])

    fig2 = plt.Figure(figsize=(6,5), dpi=75)
    pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
    pl2.bar(top, c_rec[:10])
    pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
    pltk2.get_tk_widget().grid(row=0, column=2)

    frame_plot_lisbox2 = LabelFrame(frame_plot, text="Country Ranking")
    frame_plot_lisbox2.grid(row=0, column=3, sticky='ns')
    listbox_top2 = Listbox(frame_plot_lisbox2, width=20, height=22)
    listbox_top2.grid(row=0, column=0)
    Scrollbar(frame_plot_lisbox2, command=listbox_top2.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

    listbox_top2.delete(0,'end')
    for i, k in enumerate(country_dic_sorted):
        listbox_top2.insert('end', str(i+1)+'. '+k)

def log_search_date():
    if fil_mode.get() == "Date-Date":
        d1 = cal1.selection_get()
        t1 = re.split(':', e1.get())
        dt1 = datetime.datetime(d1.year, d1.month, d1.day, int(t1[0]), int(t1[1]), int(t1[2])) 
        d2 = cal2.selection_get()
        t2 = re.split(':', e2.get())
        dt2 = datetime.datetime(d2.year, d2.month, d2.day, int(t2[0]), int(t2[1]), int(t2[2])) 
        loggy_list = loggy_search_datedur(dt1, dt2)
    else:
        loggy_list = loggy_search_date(cal1.selection_get())
    replot(loggy_list)

def all_log():
    replot(loggy_list) 
    
global loggy_list
loggy_list = loggy_all()

root = Tk()
root.title('Loggy')
#menubar##########################################
menubar = Menu(root)  
root.config(menu=menubar)

filemenu = Menu(menubar) 
menubar.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)

#loggy############################################
frame_log = LabelFrame(root, text="Logs")
frame_log.grid(row=0, column=0)

fil_mode = ttk.Combobox(frame_log, values=["Date-Date", "Date"])
Label(frame_log, text='Filter by').grid(row=0, column=0)
fil_mode.grid(row=0, column=1)
fil_mode.current(1)
fil_mode.bind("<<ComboboxSelected>>", check)

Button(frame_log, text='All log', command=all_log).grid(row=0, column=2)
        
Label(frame_log, text=" TO ").grid(row=1, column=3)
e1 = Entry(frame_log, width=7) 
e1.grid(row=2, column=1)
e1.insert(END, '00:00:00')
e1.configure(state='disabled')
e2 = Entry(frame_log, width=7) 
e2.grid(row=2, column=5)
e2.insert(END, '00:00:00')
e2.configure(state='disabled')
Button(frame_log, text="Submit", command=log_search_date).grid(row=3, column=3)
cal1 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
cal1.grid(row=1, column=0)
datelis = [] 
for object in loggy_all():
    obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
    if obj_date not in datelis:
        datelis.append(obj_date)
        cal1.calevent_create(obj_date, 'log', tags=['log'])
cal2 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
cal2.configure(state='disabled')
cal2.grid(row=1, column=4)
datelis = [] 
for object in loggy_all():
    obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
    if obj_date not in datelis:
        datelis.append(obj_date)
        cal2.calevent_create(obj_date, 'log', tags=['log'])

#ip database#############################################
frame_ip = LabelFrame(root, text="IP Database")
frame_ip.grid(row=0, column=1)

listbox_ip = Listbox(frame_ip, width=70, height=15)
listbox_ip.grid(row=1, column=0, columnspan=1)
Scrollbar(frame_ip, command=listbox_ip.yview, orient=VERTICAL).grid(row=1, column=2, sticky='ns')

entry_ip = Entry(frame_ip)
entry_ip.grid(row=0, column=0, sticky='we')
entry_ip.bind('<Return>', ip_search) #widget.bind("<Key>", key)
entry_ip.insert(0, '<ip search>')


ip_lis = ip_all() #setup
for object in ip_lis:
    ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
    listbox_ip.insert('end', ip)
#plot################################################
frame_plot = LabelFrame(root, text="Ranking")
frame_plot.grid(row=1, column=0, columnspan=2)

##########ip
iprec_dic_sorted = sort_by_visit_rec(ip_only(loggy_list))
top = [i+1 for i in range(10)]
rec = []
for i, k in enumerate(iprec_dic_sorted):
    try:
        if iprec_dic_sorted[k] == rec[-1]:
            continue
    except: pass
    rec.append(iprec_dic_sorted[k])


fig = plt.Figure(figsize=(6,5), dpi=75)
pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
pl.bar(top, rec[:10])
pltk = FigureCanvasTkAgg(fig, frame_plot)
pltk.get_tk_widget().grid(row=0, column=0)

frame_plot_lisbox = LabelFrame(frame_plot, text="IP Ranking")
frame_plot_lisbox.grid(row=0, column=1, sticky='ns')
listbox_top = Listbox(frame_plot_lisbox, width=20, height=22)
listbox_top.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox, command=listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, k in enumerate(iprec_dic_sorted):
    listbox_top.insert('end', str(i+1)+". "+k)
##########country 
country_dic_sorted = top_country(ip_only(loggy_list))
c_rec = []
for i, k in enumerate(country_dic_sorted):
    try:
        if country_dic_sorted[k] == c_rec[-1]:
            continue
    except: pass
    c_rec.append(country_dic_sorted[k])

fig2 = plt.Figure(figsize=(6,5), dpi=75)
pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
pl2.bar(top, c_rec[:10])
pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
pltk2.get_tk_widget().grid(row=0, column=2)

frame_plot_lisbox2 = LabelFrame(frame_plot, text="Country Ranking")
frame_plot_lisbox2.grid(row=0, column=3, sticky='ns')
listbox_top2 = Listbox(frame_plot_lisbox2, width=20, height=22)
listbox_top2.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox2, command=listbox_top2.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, k in enumerate(country_dic_sorted):
    listbox_top2.insert('end', str(i+1)+'. '+k)
############################################################
root.mainloop()

#plot bar chart top 10 loocation
#map plot