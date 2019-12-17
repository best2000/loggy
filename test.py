import tkinter as tk

OptionList = [] 
for i in range(60):
    OptionList.append(i)
    
app = tk.Tk()

app.geometry('100x200')

variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 12))
opt.pack(side="top")



def callback(*args):
    print(variable.get())

variable.trace("w", callback)

app.mainloop()