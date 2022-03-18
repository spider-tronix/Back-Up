from email import message
import tkinter as tk
from tkinter import ttk
from tkinter import *
from typing import Literal
from unicodedata import name
def Popup():
    root = tk.Tk()
    root.title('Back Up')
    root.geometry('800x400')

    
    """ mb = Menubutton(root, text = Menu)
    mb.grid()
    mb.menu  =  Menu ( mb, tearoff = 0 )
    #mb[]  =  mb.menu
    cVar  = IntVar()
    aVar = IntVar()
    mb.menu.add_checkbutton ( label ='Contact', variable = cVar )
    mb.menu.add_checkbutton ( label = 'About', variable = aVar )
    mb.pack()"""
    """v = tk.IntVar()
    v.set(1)  # initializing the choice, i.e. Python
    menus = [("Menu", 101),("Caliberate", 102),("Mute", 103),("Off", 104)]
    def ShowChoice():
        print(v.get())
        root.quit()
    
    for a, val  in menus:
        tk.Radiobutton(root, 
                            text=a,
                            padx = 20, 
                            variable=v, 
                            command=ShowChoice,
                            value=val).pack(anchor=tk.CENTER)
    root.mainloop()
    """
    menu =  Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='Menu', menu=filemenu)
    filemenu.add_separator()
    filemenu.add_checkbutton ( label ='Contact' )
    filemenu.add_checkbutton ( label = 'About' ) 
    caliberate ="Caliberate"
    filemenu.add_command(label='Caliberate')
    filemenu.add_separator()
    filemenu.add_command(label='Mute')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

    w = Label(root, text='Hey Raghuram, You are slouching',font= {"Arial", 55}, width=100, height=30, bg='Red', fg='white')

    """frame = Frame(root)
    frame.pack()
    bottomframe = Frame(root)
    bottomframe.pack( side = BOTTOM )
    mute = Button(frame, text = 'Mute', fg ='blue', command=root.quit)
    mute.place(bordermode= 'inside',relx = 0.5, rely = 0.5, anchor = CENTER)
    mute.pack()
    ok = Button(frame, text = 'OK', fg='blue', command=root.quit)
    ok.place(anchor= S)
    #ok.place(relx = 0.5, rely = 0.5, anchor = )
    ok.pack( side = LEFT )
    ignore = Button(frame, text ='Ignore', fg ='blue', command=root.quit)
    ignore.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    ignore.pack( side = LEFT )"""
    
    
    ttk.Button(root, text='OK', command=root.quit).place(relx = 0.5, rely = 0.5, anchor = CENTER)
    ttk.Button(root, text='Mute', command= root.quit).place(relx = 0.4, rely = 0.5, anchor = CENTER)
    ttk.Button(root, text='Ignore', command=root.quit).place(relx = 0.6, rely = 0.5, anchor = CENTER)
    w.pack()
    w.place(bordermode= 'inside',relx = 0.5, rely = 0.4, anchor = CENTER)
    root.mainloop()

"""from tkinter import *
      
root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')
mainloop()"""