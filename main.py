from tkinter import *
from tkinter import ttk
import mysql.connector as s
from dbcm import UseDatabase
from datetime import datetime

root = Tk()

class App():

    def __init__(self,root):

        self.itemno_var =[]
        self.item_var =[]
        self.price_var =[]
        self.qty_var =[]
        self.cost_var =[]

        self.dbconfig = {'host':'localhost',
                         'user':'pythonact1',
                         'passwd':'python123',
                         'database': 'shop_info',
                         'port':3308}
        self.root = root
        self.i = 0
        self.data = []
        self.item_dict = dict()
        self.prices_dict = dict()
        self.root.minsize(800,400)

        self.inputs = Frame(self.root)
        self.root.title('Cashier')
        self.root.columnconfigure(0,weight=20)
        self.root.columnconfigure(1,weight=1)

        Label(self.root, text='Welcome to the cashier app', font='Helvetica 18 bold').grid(row=0,column=0,pady=10)

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

        with UseDatabase(self.dbconfig) as cur:
            sql = 'select * from {}'.format('shop_prices')
            cur.execute(sql)
            self.data = cur.fetchall()

        for i in self.data:
            self.item_dict[i[0]] = i[1]
            self.prices_dict[i[0]] = i[2]

        self.button_create()
        self.row_create()
          
    def row_create(self,event=None):

        self.itemno_var.append(IntVar())
        self.item_var.append(StringVar())
        self.qty_var.append(IntVar())
        self.price_var.append(DoubleVar())
        self.cost_var.append(DoubleVar())
        print(self.itemno_var[0])

        self.itemno = Entry(self.inputs,textvariable=self.itemno_var[self.i])
        self.itemno.grid(row=self.i+1, column=0,sticky='WE' )
        self.item = Entry(self.inputs,state='readonly',textvariable=self.item_var[self.i])
        self.item.grid(row=self.i+1, column=1,sticky='WE' )
        self.qty = Entry(self.inputs,textvariable=self.qty_var[self.i])
        self.qty.grid(row=self.i+1, column=2,sticky='WE')
        self.price = Entry(self.inputs,state='readonly',textvariable=self.price_var[self.i])
        self.price.grid(row=self.i+1, column=3,sticky='WE')
        self.cost = Entry(self.inputs,state='readonly',textvariable=self.cost_var[self.i])
        self.cost.grid(row=self.i+1,column=4,sticky='WE')

        self.enter.destroy()
        self.next.destroy()
        self.end.destroy()
        self.totalVal.destroy()
        self.total.destroy()
        self.disp_price.destroy()

        self.button_create()

        self.i += 1

    def fetch_val(self,event=None):

        item_name = self.item_dict[self.itemno_var[self.i-1].get()]
        self.item_var[self.i-1].set(item_name)

        item_price = self.prices_dict[self.itemno_var[self.i-1].get()]
        self.price_var[self.i-1].set(item_price)

        item_cost = item_price * int(self.qty.get())
        self.cost_var[self.i-1].set(item_cost)

        
    def button_create(self,event=None):
        
        self.enter = Button(self.inputs, text='Save')
        self.enter.bind('<Button-1>',self.save)
        self.enter.grid(row=self.i+3, column=0, sticky='w',pady=10)

        self.next = Button(self.inputs, text='Add')
        self.next.bind('<Button-1>',self.fetch_val)
        self.next.grid(row=self.i+3, column=2,pady=10)

        self.disp_price = Button(self.inputs, text='Prices')
        self.disp_price.bind('<Button-1>',self.display)
        self.disp_price.grid(row=self.i+3, column=4, sticky='e',pady=10)

        self.totalVal = Label(self.inputs,text='Total')
        self.totalVal.grid(row=self.i+4,column=0,sticky='W')
        self.total = Entry(self.inputs,state='disabled')
        self.total.grid(row=self.i+4,column=1,sticky='WE',columnspan=4)

        self.end = Button(self.inputs,text='Quit' )
        self.end.grid(row=self.i+5,column=2,pady=10)
        self.end.bind('<Button-1>',self.quit)

    def save(self,event=None):
        pass

    def quit(self,event=None):
        self.root.destroy()

    def display(self,event=None):
        
        r_count = 1
        c_count = 0
        self.info = Toplevel(self.root)
        self.info.title('Prices')
        self.info.geometry('300x300')
        
        Label(self.info,text='Item no.',font='Helvetica 18 bold').grid(row=0,column=0,sticky='ew')
        Label(self.info,text='Item',font='Helvetica 18 bold').grid(row=0,column=1,sticky='ew')
        Label(self.info,text='Price',font='Helvetica 18 bold').grid(row=0,column=2,sticky='ew')

        for row in self.data:
            for val in row:
                Label(self.info,text=val,font='Helvetica 15').grid(row=r_count,column=c_count,sticky='ew')
                c_count += 1
            r_count+=1
            c_count=0
               
    

App(root)
root.mainloop()

