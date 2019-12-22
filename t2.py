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

def log_search_advance_pop():
    print("Advance af!")

def ip_search_advance_pop():
    print("Advance af!")

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
menubar = Menu(root)  
root.config(menu=menubar)

filemenu = Menu(menubar) 
menubar.add_cascade(label='File', menu=filemenu) 
filemenu.add_cascade(label='Add log(append).txt', command=add_log_ap)
filemenu.add_cascade(label='Add log(rewrite).txt', command=add_log_re)

log_view = Menu(menubar)
show_all = BooleanVar()
show_all.set(True)
show_done = BooleanVar()
show_not_done = BooleanVar()
log_view = Menu(menubar)
menubar.add_cascade(label='Log View', menu=log_view)
log_view.add_checkbutton(label="Show All", onvalue=1, offvalue=0, variable=show_all)
log_view.add_checkbutton(label="Show Done", onvalue=1, offvalue=0, variable=show_done)
log_view.add_checkbutton(label="Show Not Done", onvalue=1, offvalue=0, variable=show_not_done)
#loggy############################################
frame_log = LabelFrame(root, text="Logs")
frame_log.grid(row=0, column=0)

listbox_log = Listbox(frame_log, width=70, height=17)
listbox_log.grid(row=0, column=0)
Scrollbar(frame_log, command=listbox_log.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

###search###
frame_log_search = LabelFrame(frame_log, text="Log Search")
frame_log_search.grid(row=0, column=2, sticky='ns')

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
Button(frame_log_search, text='<== Search by Date', command=log_search_date).grid(row=2, column=1)

Button(frame_log_search, text='Search by Date-Date', command=log_search_datedur_pop).grid(row=3, column=0)
Button(frame_log_search, text='Log Advance Search', command=log_search_advance_pop).grid(row=3, column=1)

loggy_list = loggy_all() #setup
for object in loggy_list:
    listbox_log.insert('end', object.default_str)
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
entry_ip.bind('<FocusIn>', entry_ip_fin)
entry_ip.bind('<FocusOut>', entry_ip_fout)

Button(frame_ip, text="IP Advance Search", command=ip_search_advance_pop).grid(row=2, column=0, sticky='w')

ip_lis = ip_all() #setup
for object in ip_lis:
    ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
    listbox_ip.insert('end', ip)
#plot################################################
frame_plot = LabelFrame(root, text="Ranking")
frame_plot.grid(row=1, column=0, columnspan=2)

##########ip
iprec_dic_sorted = sort_by_visit_rec()
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
country_dic_sorted = top_country()
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