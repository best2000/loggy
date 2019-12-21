from tkinter import *

root = Tk()

fr_log = LabelFrame(root, text="Loggy Area")
fr_log.grid(row=0, column=0)
 
lb_log = Listbox(fr_log)
lb_log.grid(row=0, column=0)

root.mainloop()