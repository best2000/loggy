import re, datetime, tkinter, time, sql_log, pandas, threading, socket
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from mpl_toolkits.basemap import Basemap
from tkscrolledframe import ScrolledFrame

def server_soc():
    HOST = '127.0.0.1' 
    PORT = 60000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        con, _ = s.accept()
        top = Toplevel()
        top.wm_title("Just Wait...")
        l2 = Label(top, text="")
        l2.grid(row=0, column=0)
        
        Label(top, text="").grid(row=3, column=0)
        while True:
            data = con.recv(1024)
            l2.configure(text=data.decode('utf-8'))
            if data == b'add log finished':
                top.wm_title("Finished...")
                l3 = Label(top, text="PRESS REFRESH WHEN FINISHED!")
                l3.grid(row=1, column=0)
                refresh_db()
                break
        con.close()

def add_log():
    filepath =  filedialog.askopenfilename(initialdir = "C:/Users/User/Desktop/Work/Software II/Access Log",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    t = threading.Thread(target=loggy_read_log_file, args=(filepath,), daemon=True)
    t.start() #report to socket when finish 

def check(event):
    if fil_mode.get() == "Date-Date":
        e1.configure(state='normal')
        e2.configure(state='normal')
        cal2.configure(state='normal')
    else:
        e1.configure(state='disabled')
        e2.configure(state='disabled')
        cal2.configure(state='disabled')

def ip_analy_refresh():
    global ip_df
    global country_df
    global all_log_tup
    global log_tup
    global all_ip_tup

    ####ip ana
    ip_sum = {}
    for tup in log_tup:
        ip = tup[0]
        if ip in ip_sum:
            ip_sum[ip] += 1
            continue
        ip_sum[ip] = 1  
    dadic = {
        'IP':[k for k in ip_sum],
        'REC':[],
        'LAT':[],
        'LON':[]
    }
    for k in ip_sum:
        dadic['REC'].append(ip_sum[k])
        for tup in all_ip_tup:
            if tup[0] == k:
                dadic['LAT'].append(tup[2])
                dadic['LON'].append(tup[3])
                break
    ip_df = pandas.DataFrame(dadic).sort_values('REC', ascending=False)

    ######country ana
    
    country_sum = {}
    for k in ip_sum:
        for tup in all_ip_tup:
            if tup[0] == k:
                country = tup[1]
                break
        if country in country_sum:
            country_sum[country] += ip_sum[k]
            continue
        country_sum[country] = ip_sum[k]

    dadic = {
        'COUNTRY':[k for k in country_sum],
        'REC': []
    }
    for k in country_sum:
        dadic['REC'].append(country_sum[k])
    country_df = pandas.DataFrame(dadic).sort_values('REC', ascending=False)

def replot():
    #replot######
    ip_analy_refresh()
    ##stats
        #overall
    la1.configure(text="Log(DB): "+str(len(all_log_tup)))
    la2.configure(text="IP(DB): "+str(len(all_ip_tup)))
    la3.configure(text="Log(vis): "+str(len(log_tup)))
    la4.configure(text="IP(vis): "+str(ip_df.shape[0]))
        #log history
    
    listbox_lhis.delete(0,'end')
    for i, v in enumerate(his_tup): 
        listbox_lhis.insert('end', v[0]+" "+v[1]+" "+str(v[2]))
        #ip database
    listbox_ip.delete(0,'end')
    for i, v in enumerate(all_ip_tup): 
        listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3]))
    ##ip plot
    fig = plt.Figure(figsize=(6,5), dpi=75)
    pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
    rown = len(ip_df['REC'].head(10).index)
    top = [n for n in range(1, rown+1)]
    pl.bar(top, ip_df['REC'].head(10))
    pl.set_xticks(top)
    pltk = FigureCanvasTkAgg(fig, frame_plot)
    pltk.get_tk_widget().grid(row=0, column=1)
        #######lis box
    listbox_top.delete(0,'end')
    for i, v in enumerate(ip_df[['IP','REC']].values.tolist()):
        listbox_top.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
    ##country plot
    fig2 = plt.Figure(figsize=(6,5), dpi=75)
    pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
    rown = len(country_df['REC'].head(10).index)
    top = [n for n in range(1, rown+1)]
    pl2.bar(top, country_df['REC'].head(10))
    pl2.set_xticks(top)
    pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
    pltk2.get_tk_widget().grid(row=1, column=1)
        ####list box
    listbox_top2.delete(0, 'end')
    for i, v in enumerate(country_df[['COUNTRY','REC']].values.tolist()):
        listbox_top2.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
    ##map plot
    print(ip_df.head())
    lat = ip_df['LAT'].head(10).values
    lon = ip_df['LON'].head(10).values

    fig3 = plt.Figure(figsize=(6,5), dpi=150)
    pl3 = fig3.add_subplot(111, title="Top 10 IP")

    m=Basemap(llcrnrlon=-180, llcrnrlat=-60,urcrnrlon=180,urcrnrlat=80, projection='merc', ax=pl3)
    m.drawmapboundary(fill_color='#A6CAE0')
    m.fillcontinents(color='green', alpha=0.4, lake_color='#A6CAE0')
    #m.drawcoastlines()
    #m.drawcountries()

    pltk3 = FigureCanvasTkAgg(fig3, frame_plot)
    pltk3.get_tk_widget().grid(row=0, column=0, rowspan=2)


    # convert lat and lon to map projection coordinates
    lon1, lat1 = m(lon, lat)
    # plot points as red dots
    m.scatter(lon1, lat1, marker = 'o', color=['r'], zorder=5, s=[(10-i)*15 for i in range(10)], alpha=0.75)

def log_search_date():
    def loggy_search_date(date): #datetime.date
        global all_log_tup 
        global log_tup
        log_tup = []
        for tup in all_log_tup:
            dtf = re.split('/', tup[3])
            dtf = [ int(x) for x in dtf ]
            dt = datetime.datetime(dtf[0], dtf[1], dtf[2], dtf[3], dtf[4], dtf[5])
            if dt.day == date.day and dt.month == date.month and dt.year == date.year:
                log_tup.append(tup)  
    def loggy_search_datedur(dt1, dt2): #datetime - datetime 
        global all_log_tup 
        global log_tup
        log_tup = []
        for tup in all_log_tup:
            dtf = re.split('/', tup[3])
            dtf = [ int(x) for x in dtf ]
            dt = datetime.datetime(dtf[0], dtf[1], dtf[2], dtf[3], dtf[4], dtf[5])
            if (dt >= dt1) == True and (dt <= dt2) == True:
                log_tup.append(tup)  

    if fil_mode.get() == "Date-Date":
        d1 = cal1.selection_get()
        t1 = re.split(':', e1.get())
        dt1 = datetime.datetime(d1.year, d1.month, d1.day, int(t1[0]), int(t1[1]), int(t1[2])) 
        d2 = cal2.selection_get()
        t2 = re.split(':', e2.get())
        dt2 = datetime.datetime(d2.year, d2.month, d2.day, int(t2[0]), int(t2[1]), int(t2[2])) 
        loggy_search_datedur(dt1, dt2)
    else:
        loggy_search_date(cal1.selection_get())

    replot()
    
def ip_search(event):
    listbox_ip.delete(0,'end')
    if entry_ip.get() == "":
        for i, v in enumerate(all_ip_tup): 
            listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3]))
    else:
        tup = sql_ip.get_ip_by_ip(entry_ip.get())
        listbox_ip.insert(0, "IP: "+tup[0], "Country: "+tup[1], "Lat: "+str(tup[2]), "Lon: "+str(tup[3]))
        

def all_log():
    global log_tup
    log_tup = all_log_tup 
    replot()

def refresh_db():
    global all_log_tup
    global log_tup
    global all_ip_tup
    global his_tup
    all_log_tup = sql_log.get_all_log()
    log_tup = all_log_tup 
    all_ip_tup = sql_ip.get_all_ip()
    ip_analy_refresh()
    his_tup = sql_lhis.get_all_his()
    replot()
    cal1.calevent_remove('all')
    cal2.calevent_remove('all')
    datelis = [] 
    for tup in all_log_tup:
        dtf = re.split('/', tup[3])
        dtf = [ int(x) for x in dtf ]
        log_date = datetime.date(dtf[0], dtf[1], dtf[2])
        if log_date not in datelis:
            datelis.append(log_date)
            cal1.calevent_create(log_date, 'log', tags=['log'])
            cal2.calevent_create(log_date, 'log', tags=['log'])

def rollback():
    i = listbox_lhis.curselection()[0]
    his = listbox_lhis.get(i, None)
    atime = his[0:19]
    sql_lhis.rollback(atime)
    sql_log.rollback(atime)
    refresh_db() 
    

def ip_auto_fill(event):
    i = listbox_ip.curselection()[0]
    lip = listbox_ip.get(i, None)
    entry_ip.delete(0, 'end')
    entry_ip.insert(0, re.split(' ',lip)[1])

def ip_auto_fill2(event):
    print("lol")
    i = listbox_top.curselection()[0]
    lip = listbox_top.get(i, None)
    entry_ip.delete(0, 'end')
    entry_ip.insert(0, re.split(' ',lip)[1])

def entry_clr(event):
    if entry_ip.get() == "<ip search>":
        entry_ip.delete(0, 'end')

def tog():
    if s_tog.get() == True:
        frame_log.grid(row=0, column=0)
        frame_stat.grid(row=0, column=1)
        sf.configure(height=474)
    else:
        sf.configure(height=750)
        frame_log.grid_remove()
        frame_stat.grid_remove()

def tog2(event):
    s_tog.set(not (s_tog.get()))
    tog()

########socket set up
st = threading.Thread(target=server_soc, daemon=True)
st.start()

#######SET UP
his_tup = sql_lhis.get_all_his()
all_log_tup = sql_log.get_all_log()
log_tup = all_log_tup 
all_ip_tup = sql_ip.get_all_ip()
ip_analy_refresh()


root = Tk()
root.title('Loggy')
menubar = Menu(root)
s_tog = BooleanVar()
#s_tog.set(True)

root.bind("s", tog2)

view_menu = Menu(menubar)
view_menu.add_checkbutton(label="Search menu", onvalue=1, offvalue=0, variable=s_tog, command=tog)
menubar.add_cascade(label='Search', menu=view_menu)
root.config(menu=menubar)
#loggy############################################
frame_log = LabelFrame(root, text="Logs")

Label(frame_log, text="Filter By").grid(row=0, column=0)
fil_mode = ttk.Combobox(frame_log, values=["Date-Date", "Date"])
fil_mode.grid(row=0, column=2, columnspan=3)
fil_mode.current(1)
fil_mode.bind("<<ComboboxSelected>>", check)
        
e1 = Entry(frame_log, width=7) 
e1.grid(row=2, column=1, columnspan=2)
e1.insert(END, '00:00:00')
e1.configure(state='disabled')
e2 = Entry(frame_log, width=7) 
e2.grid(row=2, column=6, columnspan=2)
e2.insert(END, '23:59:59')
e2.configure(state='disabled')

Button(frame_log, text="Filter", command=log_search_date).grid(row=3, column=4, columnspan=4, sticky="ew")
Button(frame_log, text='All Logs', command=all_log).grid(row=3, column=0, sticky="ew", columnspan=4)



cal1 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y', font='Arial 8')
cal1.grid(row=1, column=0, columnspan=4)
cal2 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y', font='Arial 8')
cal2.configure(state='disabled')
cal2.grid(row=1, column=6, columnspan=2)
datelis = [] 
for tup in all_log_tup:
    dtf = re.split('/', tup[3])
    dtf = [ int(x) for x in dtf ]
    log_date = datetime.date(dtf[0], dtf[1], dtf[2])
    if log_date not in datelis:
        datelis.append(log_date)
        cal1.calevent_create(log_date, 'log', tags=['log'])
        cal2.calevent_create(log_date, 'log', tags=['log'])
cal1.tag_config('log', background='Green')
cal2.tag_config('log', background='Green')
##########overall stat##################################
frame_stat = LabelFrame(root, text="Stats")
###
frame_os = LabelFrame(frame_stat, text="Overall")
frame_os.grid(row=0, column=0, sticky='n')
la1 = Label(frame_os, text="Log(DB): "+str(len(all_log_tup)))
la1.grid(row=0, column=0, sticky='w')
la2 = Label(frame_os, text="IP(DB): "+str(len(all_ip_tup)))
la2.grid(row=1, column=0, sticky='w')
Label(frame_os, text="").grid(row=2, column=0)
la3 = Label(frame_os, text="Log(vis): "+str(len(all_log_tup)))
la3.grid(row=3, column=0, sticky='w')
la4 = Label(frame_os, text="IP(vis): "+str(len(all_ip_tup)))
la4.grid(row=4, column=0, sticky='w')
#logs history###################
frame_lhis = LabelFrame(frame_stat, text="Logs History <datetime/name/line>")
frame_lhis.grid(row=0, column=1, rowspan=7, sticky='n')
listbox_lhis = Listbox(frame_lhis, width=70, height=13, activestyle="none")
listbox_lhis.grid(row=0, column=0, columnspan=3)
Scrollbar(frame_lhis, command=listbox_lhis.yview, orient=VERTICAL).grid(row=0, column=3, sticky='ns')
Button(frame_lhis, text="Add Logs File", command=add_log).grid(row=1, column=0, sticky="ew")
Button(frame_lhis, text='Refresh', command=refresh_db).grid(row=1, column=2, sticky="ew", columnspan=2)
Button(frame_lhis, text="Rollback", command=rollback).grid(row=1, column=1, sticky="ew")


for i, v in enumerate(his_tup): 
    listbox_lhis.insert('end', v[0]+" "+v[1]+" "+str(v[2]))
#ip database#############################################
frame_ip = LabelFrame(frame_stat, text="IP Database <ip/country/lat/lon/rec>")
frame_ip.grid(row=0, column=2)

entry_ip = Entry(frame_ip)
entry_ip.grid(row=0, column=0, sticky='we')
entry_ip.insert(0, "<ip search>")
entry_ip.bind('<Return>', ip_search) #widget.bind("<Key>", key)
entry_ip.bind("<Button-1>", entry_clr)

listbox_ip = Listbox(frame_ip, width=70, height=13, activestyle="none")
listbox_ip.grid(row=1, column=0, columnspan=1, sticky='n')
listbox_ip.bind("<Button-1>", ip_auto_fill)
listbox_ip.bind("<Return>", ip_search)
Scrollbar(frame_ip, command=listbox_ip.yview, orient=VERTICAL).grid(row=1, column=2, sticky='ns')

for i, v in enumerate(all_ip_tup): 
    listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3]))
#plot################################################


# Create a ScrolledFrame widget
sf = ScrolledFrame(root, width=1500, height=750)
sf.grid(row=1, column=0, columnspan=3)
# Bind the arrow keys and scroll wheel
sf.bind_scroll_wheel(root)

# Create a frame within the ScrolledFrame
inner_frame = sf.display_widget(Frame)

frame_plot = Frame(inner_frame)
frame_plot.grid(row=0, column=0)

tog() #toggsearch
######IP##################
##########ip
fig = plt.Figure(figsize=(6,5), dpi=75)
pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
try: 
    rown = len(ip_df['REC'].head(10).index)
    top = [i for i in range(1, rown+1)]
    pl.bar(top, ip_df['REC'].head(10))
    pl.set_xticks(top)
except: pass
pltk = FigureCanvasTkAgg(fig, frame_plot)
pltk.get_tk_widget().grid(row=0, column=1)
    ##################################lisbox
frame_plot_lisbox = LabelFrame(frame_plot, text="IP Ranking")
frame_plot_lisbox.grid(row=0, column=2, sticky='ns')
listbox_top = Listbox(frame_plot_lisbox, width=20, height=22, activestyle="none")
listbox_top.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox, command=listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')
listbox_top.bind("<Button-1>", ip_auto_fill2)
listbox_top.bind("<Return>", ip_search)

for i, v in enumerate(ip_df[['IP','REC']].values.tolist()):
    listbox_top.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
##########country 
fig2 = plt.Figure(figsize=(6,5), dpi=75)
pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
try: 
    rown = len(country_df['REC'].head(10).index)
    top = [i for i in range(1, rown+1)]
    pl2.bar(top, country_df['REC'].head(10))
    pl2.set_xticks(top)
except: pass
pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
pltk2.get_tk_widget().grid(row=1, column=1)
    #########lisbox
frame_plot_lisbox2 = LabelFrame(frame_plot, text="Country Ranking")
frame_plot_lisbox2.grid(row=1, column=2, sticky='ns')
listbox_top2 = Listbox(frame_plot_lisbox2, width=20, height=22, activestyle="none")
listbox_top2.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox2, command=listbox_top2.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, v in enumerate(country_df[['COUNTRY','REC']].values.tolist()):
    listbox_top2.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
##########ip map plot
lat = ip_df['LAT'].head(10).values
lon = ip_df['LON'].head(10).values

fig3 = plt.Figure(figsize=(6,5), dpi=150)
pl3 = fig3.add_subplot(111, title="Top 10 IP")

m=Basemap(llcrnrlon=-180, llcrnrlat=-60,urcrnrlon=180,urcrnrlat=80, projection='merc', ax=pl3)
m.drawmapboundary(fill_color='#A6CAE0')
m.fillcontinents(color='green', alpha=0.4, lake_color='#A6CAE0')
#m.drawcoastlines()
#m.drawcountries()

pltk3 = FigureCanvasTkAgg(fig3, frame_plot)
pltk3.get_tk_widget().grid(row=0, column=0, rowspan=2)


# convert lat and lon to map projection coordinates
lon1, lat1 = m(lon, lat)
# plot points as red dots
try: 
    m.scatter(lon1, lat1, marker = 'o', color=['r'], zorder=5, s=[(10-i)*15 for i in range(10)], alpha=0.75)
    print("lol")
except: pass
##############################################################################
root.mainloop()

#correction test
#map error not plot