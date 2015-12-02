from Tkinter import *

window = Tk()

cadre = Frame(window, width=700, height=500, borderwidth=1)
cadre.pack(fill=BOTH)

#move forward
forward = Frame(cadre, width=700, height=100, borderwidth=1)
forward.pack(fill=Y)
message = Label(forward, text="Move Forward")
message.pack(side="left") 

var_texte = StringVar()
ligne_texte = Entry(forward, textvariable=var_texte, width=5)
ligne_texte.pack(side="left")

message = Label(forward, text="mm")
message.pack(side="left") 

bouton_forward = Button(forward, text="Move Forward", fg="red",command=window.quit)
bouton_forward.pack(side="left") 

#move aside
aside = Frame(cadre, width=700, height=100, borderwidth=1)
aside.pack(fill=Y)
message = Label(aside, text="Move Aside")
message.pack(side="left")

var_texte = StringVar()
ligne_texte = Entry(aside, textvariable=var_texte, width=5)
ligne_texte.pack(side="left")

message = Label(aside, text="mm")
message.pack(side="left")

bouton_aside = Button(aside, text="Move Aside", fg="red",command=window.quit)
bouton_aside.pack(side="left") 

#rotation
rotation = Frame(cadre, width=700, height=100, borderwidth=1)
rotation.pack(fill=Y)
message = Label(rotation, text="Rotation")
message.pack(side="left")

var_texte = StringVar()
ligne_texte = Entry(rotation, textvariable=var_texte, width=5)
ligne_texte.pack(side="left")

message = Label(rotation, text="degres")
message.pack(side="left")

bouton_aside = Button(rotation, text="Rotation", fg="red",command=window.quit)
bouton_aside.pack(side="left") 

window.mainloop()

