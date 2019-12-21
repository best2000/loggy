import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ip_collector import *

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

root= tk.Tk() 

fig = plt.Figure(figsize=(6,5), dpi=100)
pl = fig.add_subplot(111, title="Top 10 IP", xlabel="IP", ylabel="Visited")
pl.bar(top, rec)

pltk = FigureCanvasTkAgg(fig, root)
pltk.get_tk_widget().grid(row=0, column=0)

for i, lis in enumerate(ip_rec):
    for object in lis:
        print(i+1, ':', object.address)

root.mainloop()