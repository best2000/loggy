## import all names from Tkinter
## bit naughty but I don't mind
from tkinter import *
# root window
root=Tk()
# text area
text=Text()
text.pack(side="left", expand="yes", fill="both")

# scrolbar for above textarea
sb = Scrollbar(root)
sb.pack(side="right", fill="y")

## bind them both together...

# this line binds the yscrollcommand
# of the text area to the scrollbar set method
text['yscrollcommand'] = sb.set

# this line binds the scrollbars command to
# the yview method of the text area
sb['command'] = text.yview

# mainloop entry
root.mainloop()