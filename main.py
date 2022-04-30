from tkinter import *
from tkinter import ttk
import mysql.connector as s
from dbcm import UseDatabase

root = Tk()

class App():

    def __init__(self,root):
        self.root = root
        self.i = 0
        self.root.minsize(800,400)

        self.inputs = Frame(self.root)
        self.root.title('Cashier')
        self.root.columnconfigure(0,weight=20)
        self.root.columnconfigure(1,weight=1)

        Label(self.root, text='Welcome to the cashier app').grid(row=0,column=0)

        self.inputs.columnconfigure(0,weight=1)
        self.inputs.columnconfigure(1,weight=10)
        self.inputs.columnconfigure(2,weight=1)
        self.inputs.columnconfigure(3,weight=1)
        self.inputs.columnconfigure(4,weight=1)
        self.inputs.grid(row=1,column=0,sticky='nsew',padx=10)

        
        Label(self.inputs,text='Item no.').grid(row=0,column=0,sticky='EW' )
        Label(self.inputs,text='Item').grid(row=0,column=1,sticky='EW')
        Label(self.inputs,text='Qty').grid(row=0,column=2,sticky='EW' )
        Label(self.inputs,text='Price').grid(row=0,column=3,sticky='EW')
        Label(self.inputs,text='Cost').grid(row=0,column=4,sticky='EW')

        self.button_create()
        self.row_create()
        

    def row_create(self,event=None):

        self.itemno = Entry(self.inputs).grid(row=self.i+1, column=0,sticky='WE' )
        self.item = Entry(self.inputs,state='disabled').grid(row=self.i+1, column=1,sticky='WE' )
        self.qty = Entry(self.inputs).grid(row=self.i+1, column=2,sticky='WE')
        self.price = Entry(self.inputs,state='disabled').grid(row=self.i+1, column=3,sticky='WE')
        self.cost = Entry(self.inputs,state='disabled').grid(row=self.i+1,column=4,sticky='WE')

        self.enter.destroy()
        self.next.destroy()
        self.end.destroy()

        self.button_create()

        self.i += 1

    def save(self,event=None):
        pass

    def quit(self,event=None):
        self.root.destroy()

    def button_create(self,event=None):
        
        self.enter = Button(self.inputs, text='Save')
        self.enter.bind('<Button-1>',self.save)
        self.enter.grid(row=self.i+3, column=0, sticky='w',pady=10)

        self.next = Button(self.inputs, text='Add')
        self.next.bind('<Button-1>',self.row_create)
        self.next.grid(row=self.i+3, column=2,pady=10)

        self.end = Button(self.inputs, text='Quit')
        self.end.bind('<Button-1>',self.quit)
        self.end.grid(row=self.i+3, column=4, sticky='e',pady=10)


App(root)
root.mainloop()

