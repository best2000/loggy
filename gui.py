import re, datetime, tkinter, socket, threading
from ip_collector import *
from loggy_collector import *
from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ip_collector import *
from tkinter import ttk
    
class frame_logfil:
    def __init__(self, master):
        self.master = master
        self.main = LabelFrame(self.master, text='Log Pool Filter')

        self.combo = ttk.Combobox(self.main, values=["Date-Date", "Date"])
        Label(self.main, text='Filter by').grid(row=0, column=0)
        self.combo.grid(row=0, column=1)
        self.combo.current(1)
        self.combo.bind("<<ComboboxSelected>>", self.check)
        
        Label(self.main, text=" TO ").grid(row=1, column=3)
        self.e1 = Entry(self.main, width=7) 
        self.e1.grid(row=2, column=1)
        self.e1.insert(END, '00:00:00')
        self.e1.configure(state='disabled')
        self.e2 = Entry(self.main, width=7) 
        self.e2.grid(row=2, column=5)
        self.e2.insert(END, '00:00:00')
        self.e2.configure(state='disabled')
        Button(self.main, text="Submit", command=self.log_search_datedur).grid(row=3, column=3)
        self.cal1 = Calendar(self.main, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
        self.cal1.grid(row=1, column=0)
        datelis = [] 
        for object in loggy_all():
            obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
            if obj_date not in datelis:
                datelis.append(obj_date)
                self.cal1.calevent_create(obj_date, 'log', tags=['log'])
        self.cal2 = Calendar(self.main, selectmode='day', showothermonthdays=False, year=2015, month=5, date_pattern='dd/mm/y')
        self.cal2.configure(state='disabled')
        self.cal2.grid(row=1, column=4)
        datelis = [] 
        for object in loggy_all():
            obj_date = datetime.date(object.datetime.year, object.datetime.month, object.datetime.day)
            if obj_date not in datelis:
                datelis.append(obj_date)
                self.cal2.calevent_create(obj_date, 'log', tags=['log'])
        
        #PLOTT#############
        self.frame_plot = LabelFrame(self.main, text='visualize')
        self.frame_plot.grid(row=4, column=0)
        
        ##ip######
        iprec_dic_sorted = sort_by_visit_rec(ip_only(loggy_lis))
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
        pltk = FigureCanvasTkAgg(fig, self.frame_plot)
        self.plot_ip = pltk.get_tk_widget()
        self.plot_ip.grid(row=0, column=0)

        self.frame_plot_lisbox = LabelFrame(self.frame_plot, text="IP Ranking")
        self.frame_plot_lisbox.grid(row=0, column=1, sticky='ns')
        self.listbox_top = Listbox(self.frame_plot_lisbox, width=20, height=22)
        self.listbox_top.grid(row=0, column=0)
        Scrollbar(self.frame_plot_lisbox, command=self.listbox_top.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

        for i, k in enumerate(iprec_dic_sorted):
            self.listbox_top.insert('end', str(i+1)+". "+k)
        ##########country 
        country_dic_sorted = top_country(ip_only(loggy_lis))
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
        pltk2 = FigureCanvasTkAgg(fig2, self.frame_plot)
        pltk2.get_tk_widget().grid(row=0, column=2)

        frame_plot_lisbox2 = LabelFrame(self.frame_plot, text="Country Ranking")
        frame_plot_lisbox2.grid(row=0, column=3, sticky='ns')
        listbox_top2 = Listbox(frame_plot_lisbox2, width=20, height=22)
        listbox_top2.grid(row=0, column=0)
        Scrollbar(frame_plot_lisbox2, command=listbox_top2.yview, orient=VERTICAL).grid(row=0, column=1, sticky='ns')

        for i, k in enumerate(country_dic_sorted):
            listbox_top2.insert('end', str(i+1)+'. '+k)

    def check(self, event):
        if self.combo.get() == "Date-Date":
            self.e1.configure(state='normal')
            self.e2.configure(state='normal')
            self.cal2.configure(state='normal')
        else:
            self.e1.configure(state='disabled')
            self.e2.configure(state='disabled')
            self.cal2.configure(state='disabled')

    def log_search_datedur(self):
        if self.combo.get() == "Date-Date":
            d1 = self.cal1.selection_get()
            t1 = re.split(':', self.e1.get())
            dt1 = datetime.datetime(d1.year, d1.month, d1.day, int(t1[0]), int(t1[1]), int(t1[2])) 
            d2 = self.cal2.selection_get()
            t2 = re.split(':', self.e2.get())
            dt2 = datetime.datetime(d2.year, d2.month, d2.day, int(t2[0]), int(t2[1]), int(t2[2])) 
            loggy_list = loggy_search_datedur(dt1, dt2)
        else:
            loggy_list = loggy_search_date(self.cal1.selection_get())
        
        #RE PLOT###
        self.plot_ip.destroy()
        iprec_dic_sorted = sort_by_visit_rec(ip_only(loggy_lis))
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
        pltk = FigureCanvasTkAgg(fig, self.frame_plot)
        pltk.get_tk_widget().grid(row=0, column=0)

        self.listbox_top.delete(0,'end')
        for i, k in enumerate(iprec_dic_sorted):
            self.listbox_top.insert('end', str(i+1)+". "+k)

            

class frame_ip:
    def __init__(self, master):
        self.main = LabelFrame(master, text='IP Pool Filter')

        self.listbox_ip = Listbox(self.main, width=70, height=15)
        self.listbox_ip.grid(row=1, column=0)
        Scrollbar(self.main, command=self.listbox_ip.yview, orient=VERTICAL).grid(row=1, column=2, sticky='ns')

        self.entry_ip = Entry(self.main)
        self.entry_ip.grid(row=0, column=0, sticky='we')
        self.entry_ip.bind('<Return>', self.ip_search) 
        self.entry_ip.insert(0, '<ip search>')

        ip_lis = ip_all() #setup
        for object in ip_lis:
            ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
            self.listbox_ip.insert('end', ip)

    def ip_search(self, event):
        self.listbox_ip.delete(0,'end')
        if self.entry_ip.get() == "":
            ip_lis = ip_all()
            for object in ip_lis:
                ip = object.address+' '+object.country+' '+object.city+' '+str(object.lat)+' '+str(object.lon)+' '+object.isp+' '+str(object.visit_rec)
                self.listbox_ip.insert('end', ip)
        else:
            object = ip_get_object(self.entry_ip.get())
            self.listbox_ip.insert(0, 'Address: '+object.address, 'Country: '+object.country, 'City: '+object.city, 'Lat: '+str(object.lat), 'Lon: '+str(object.lon), 'Isp: '+object.isp, 'Rec: '+str(object.visit_rec))
        

    
global loggy_lis
loggy_lis = loggy_all()


root = tkinter.Tk()
flf = frame_logfil(root) 
flf.main.grid(row=0, column=0)
fip = frame_ip(root)
fip.main.grid(row=0, column=1)
root.mainloop()
