import functools
import Tkinter as tk

def forward(event,param):
	print "forward"
	print "whith parameter : ",param


root = tk.Tk()
root.bind("<Up>",functools.partial(forward,param="aze"))
root.mainloop()

