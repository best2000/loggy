import re, datetime, tkinter, time, sql_log, pandas, threading, socket
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from mpl_toolkits.basemap import Basemap


def server_soc():
    HOST = '127.0.0.1' 
    PORT = 60000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        con, _ = s.accept()
        top = Toplevel()
        top.wm_title("Please Wait...")
        l1=Label(top, text="Feel free to use program while adding")
        l1.grid(row=0, column=0)
        l2 = Label(top, text="")
        l2.grid(row=2, column=0)
        l3 = Label(top, text="DONT CLOSE THIS WINDOW IF IT NOT FINISHED!")
        l3.grid(row=1, column=0)
        while True:
            data = con.recv(1024)
            l2.configure(text=data.decode('utf-8'))
            if data == b'add log finished':
                top.wm_title("Finished...")
                l1.configure(text="Logs added")
                l3.configure(text="PRESS 'Refresh' BUTTOM TO REFRESH DATABASE INORDER TO USE IN PROGRAM")
                l2.configure(text="You can close this.")
                break
        con.close()

def add_log():
    filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
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
        ip = tup[1]
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
    la1.configure(text="Logs(DB): "+str(len(all_log_tup)))
    la2.configure(text="IP(DB): "+str(len(all_ip_tup)))
    la3.configure(text="Logs(vis): "+str(len(log_tup)))
    la4.configure(text="IP(vis): "+str(ip_df.shape[0]))
    #ip database
    listbox_ip.delete(0,'end')
    for i, v in enumerate(all_ip_tup): 
        listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3])+" "+str(v[4]))
    ##ip plot
    fig = plt.Figure(figsize=(6,5), dpi=60)
    pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
    rown = len(ip_df['REC'].head(10).index)
    pl.bar([n for n in range(1, rown+1)], ip_df['REC'].head(10))
    pltk = FigureCanvasTkAgg(fig, frame_plot)
    pltk.get_tk_widget().grid(row=0, column=0)
        #######lis box
    listbox_top.delete(0,'end')
    for i, v in enumerate(ip_df[['IP','REC']].values.tolist()):
        listbox_top.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
    ##country plot
    fig2 = plt.Figure(figsize=(6,5), dpi=60)
    pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
    rown = len(country_df['REC'].head(10).index)
    pl2.bar([n for n in range(1, rown+1)], country_df['REC'].head(10))
    pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
    pltk2.get_tk_widget().grid(row=0, column=2)
        ####list box
    listbox_top2.delete(0, 'end')
    for i, v in enumerate(country_df[['COUNTRY','REC']].values.tolist()):
        listbox_top2.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
    ##map plot
    lat = ip_df['LAT'].head(10).values
    lon = ip_df['LON'].head(10).values

    fig3 = plt.Figure(figsize=(7,5), dpi=60)
    pl3 = fig3.add_subplot(111, title="Top 10 IP")
    m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c',ax=pl3)
    pltk3 = FigureCanvasTkAgg(fig3, frame_plot)
    pltk3.get_tk_widget().grid(row=0, column=4)

    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color = 'white',lake_color='#46bcec')
    # convert lat and lon to map projection coordinates
    lons, lats = m(lon, lat)
    # plot points as red dots
    m.scatter(lons, lats, marker = 'o', color='r', zorder=5)

def log_search_date():
    def loggy_search_date(date): #datetime.date
        global all_log_tup 
        global log_tup
        log_tup = []
        for tup in all_log_tup:
            dtf = re.split('/', tup[4])
            dtf = [ int(x) for x in dtf ]
            dt = datetime.datetime(dtf[0], dtf[1], dtf[2], dtf[3], dtf[4], dtf[5])
            if dt.day == date.day and dt.month == date.month and dt.year == date.year:
                log_tup.append(tup)  
    def loggy_search_datedur(dt1, dt2): #datetime - datetime 
        global all_log_tup 
        global log_tup
        log_tup = []
        for tup in all_log_tup:
            dtf = re.split('/', tup[4])
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
            listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3])+" "+str(v[4]))
    else:
        tup = sql_ip.get_ip_by_ip(entry_ip.get())
        listbox_ip.insert(0, tup[0], tup[1], tup[2], tup[3], tup[4])


def all_log():
    global log_tup
    log_tup = all_log_tup 
    replot()

def refresh_db():
    global all_log_tup
    global log_tup
    global all_ip_tup
    all_log_tup = sql_log.get_all_log()
    log_tup = all_log_tup 
    all_ip_tup = sql_ip.get_all_ip()
    ip_analy_refresh()
    replot()
    datelis = [] 
    for tup in all_log_tup:
        dtf = re.split('/', tup[4])
        dtf = [ int(x) for x in dtf ]
        log_date = datetime.date(dtf[0], dtf[1], dtf[2])
        if log_date not in datelis:
            datelis.append(log_date)
            cal1.calevent_create(log_date, 'log', tags=['log'])
            cal2.calevent_create(log_date, 'log', tags=['log'])

########socket set up
st = threading.Thread(target=server_soc, daemon=True)
st.start()

#######
all_log_tup = sql_log.get_all_log()
log_tup = all_log_tup 
all_ip_tup = sql_ip.get_all_ip()
ip_analy_refresh()


root = Tk()
root.title('Loggy')

#loggy############################################
frame_log = LabelFrame(root, text="Logs")
frame_log.grid(row=0, column=0)

fil_mode = ttk.Combobox(frame_log, values=["Date-Date", "Date"])
fil_mode.grid(row=0, column=0)
fil_mode.current(1)
fil_mode.bind("<<ComboboxSelected>>", check)
        
e1 = Entry(frame_log, width=7) 
e1.grid(row=2, column=0)
e1.insert(END, '00:00:00')
e1.configure(state='disabled')
e2 = Entry(frame_log, width=7) 
e2.grid(row=2, column=3)
e2.insert(END, '00:00:00')
e2.configure(state='disabled')

Button(frame_log, text="Submit", command=log_search_date).grid(row=3, column=1)
Button(frame_log, text='All log', command=all_log).grid(row=0, column=3)
Button(frame_log, text='Refresh', command=refresh_db).grid(row=0, column=4)


cal1 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y', font='Arial 8')
cal1.grid(row=1, column=0)
cal2 = Calendar(frame_log, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y', font='Arial 8')
cal2.configure(state='disabled')
cal2.grid(row=1, column=3, columnspan=2)
datelis = [] 
for tup in all_log_tup:
    dtf = re.split('/', tup[4])
    dtf = [ int(x) for x in dtf ]
    log_date = datetime.date(dtf[0], dtf[1], dtf[2])
    if log_date not in datelis:
        datelis.append(log_date)
        cal1.calevent_create(log_date, 'log', tags=['log'])
        cal2.calevent_create(log_date, 'log', tags=['log'])
cal1.tag_config('log', background='Green')
cal2.tag_config('log', background='Green')
##########overall stat
frame_stat = LabelFrame(root, text="Stats")
frame_stat.grid(row=0, column=1)
la1 = Label(frame_stat, text="Logs(DB): "+str(len(all_log_tup)))
la1.grid(row=0, column=0)
la2 = Label(frame_stat, text="IP(DB): "+str(len(all_ip_tup)))
la2.grid(row=1, column=0)
Label(frame_stat, text="").grid(row=2, column=0)
la3 = Label(frame_stat, text="Logs(vis): "+str(len(all_log_tup)))
la3.grid(row=3, column=0)
la4 = Label(frame_stat, text="IP(vis): "+str(len(all_ip_tup)))
la4.grid(row=4, column=0)
Label(frame_stat, text="").grid(row=5, column=0)
Button(frame_stat, text="Add New Logs", command=add_log).grid(row=6, column=0)
#ip database#############################################
frame_ip = LabelFrame(root, text="IP Database")
frame_ip.grid(row=0, column=2)

listbox_ip = Listbox(frame_ip, width=70, height=14)
listbox_ip.grid(row=1, column=0, columnspan=1)
Scrollbar(frame_ip, command=listbox_ip.yview, orient=VERTICAL).grid(row=1, column=2, sticky='ns')

entry_ip = Entry(frame_ip)
entry_ip.grid(row=0, column=0, sticky='we')
entry_ip.bind('<Return>', ip_search) #widget.bind("<Key>", key)

for i, v in enumerate(all_ip_tup): 
    listbox_ip.insert('end', str(i+1)+'.) '+v[0]+" "+v[1]+" "+str(v[2])+" "+str(v[3])+" "+str(v[4]))
#plot################################################
frame_plot = LabelFrame(root, text="Ranking")
frame_plot.grid(row=1, column=0, columnspan=3)

top = [i+1 for i in range(10)]
######IP##################
##########ip
fig = plt.Figure(figsize=(6,5), dpi=60)
pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Records")
try: pl.bar(top, ip_df['REC'].head(10))
except: pass
pltk = FigureCanvasTkAgg(fig, frame_plot)
pltk.get_tk_widget().grid(row=0, column=0)
    ##################################lisbox
frame_plot_lisbox = LabelFrame(frame_plot, text="IP Ranking")
frame_plot_lisbox.grid(row=0, column=1, sticky='ns')
listbox_top = Listbox(frame_plot_lisbox, width=20, height=18)
listbox_top.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox, command=listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, v in enumerate(ip_df[['IP','REC']].values.tolist()):
    listbox_top.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
##########country 
fig2 = plt.Figure(figsize=(6,5), dpi=60)
pl2 = fig2.add_subplot(111, title="Top 10 Country", xlabel="Countries", ylabel="Records")
try: pl2.bar(top, country_df['REC'].head(10))
except: pass
pltk2 = FigureCanvasTkAgg(fig2, frame_plot)
pltk2.get_tk_widget().grid(row=0, column=2)
    #########lisbox
frame_plot_lisbox2 = LabelFrame(frame_plot, text="Country Ranking")
frame_plot_lisbox2.grid(row=0, column=3, sticky='ns')
listbox_top2 = Listbox(frame_plot_lisbox2, width=20, height=18)
listbox_top2.grid(row=0, column=0)
Scrollbar(frame_plot_lisbox2, command=listbox_top2.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

for i, v in enumerate(country_df[['COUNTRY','REC']].values.tolist()):
    listbox_top2.insert('end', str(i+1)+".) "+v[0]+" ["+str(v[1])+"]")
##########ip map plot
lat = ip_df['LAT'].head(10).values
lon = ip_df['LON'].head(10).values

fig3 = plt.Figure(figsize=(7,5), dpi=70)
pl3 = fig3.add_subplot(111, title="Top 10 IP")
m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c',ax=pl3)
pltk3 = FigureCanvasTkAgg(fig3, frame_plot)
pltk3.get_tk_widget().grid(row=0, column=4)

m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color = 'white',lake_color='#46bcec')
# convert lat and lon to map projection coordinates
lon1, lat1 = m(lon, lat)
# plot points as red dots
try: 
    m.scatter(lon1, lat1, marker = 'o', color='r', zorder=5, s=100, alpha=0.5)
except: pass
##############################################################################
root.mainloop()

#undo lastest added log
#choose to add or remove added log
#show hide console