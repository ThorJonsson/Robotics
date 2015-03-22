from Tkinter import *

def up(event):
	print "going up"

def down(event):
	print "going down"

def left(event):
	print "rotating left"

def right(event):
	print "rotating right"

def initial(event):
	print "initial position"

root = Tk()

root.bind("<Up>",up)
root.bind("<Down>",down)
root.bind("<Right>",right)
root.bind("<Left>",left)
root.bind("<i>",initial)
root.mainloop()
