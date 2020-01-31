from tkinter import *
from tkscrolledframe import ScrolledFrame

# Create a root window
root = Tk()

# Create a ScrolledFrame widget
sf = ScrolledFrame(root, width=640, height=480)
sf.grid(row=0, column=0)

# Bind the arrow keys and scroll wheel
sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)

# Create a frame within the ScrolledFrame
inner_frame = sf.display_widget(Frame)

# Add a bunch of widgets to fill some space
for i in range(100):
   Label(inner_frame, text=str(i)).grid(row=i, column=0)

# Start Tk's event loop
root.mainloop()