import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ip_collector import *

ip = []
rec = []
loggylis = sort_by_visit_rec()
for index, object in enumerate(loggylis):
    if index == 9:
        break
    ip.append(object.address)
    rec.append(object.visit_rec)

"""
plt.barh(ip, rec, color='green')
plt.ylabel("IP")
plt.xlabel("Visited records")
plt.title("Top 10 IP Visited")
plt.show()
"""
ip.reverse()
rec.reverse()

root= tk.Tk() 

fig = plt.Figure(figsize=(6,5), dpi=100)
pl = fig.add_subplot(111)
pltk = FigureCanvasTkAgg(fig, root)
pltk.get_tk_widget().grid(row=0, column=0)
pl.barh(ip, rec, color='green')

root.mainloop()