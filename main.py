from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
        self.total_val = DoubleVar()

        self.dbconfig = {'host':'localhost',
                         'user':'pythonact1',
                         'passwd':'python123',
                         'database': 'shop_info',
                         'port':3308}
        self.root = root
        self.i = 0
        self.data = []
        self.purchase_data = []
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
        self.row_create(first=True)

        
    def fetch_item(self,event):
        item_name = self.item_dict[self.itemno_var[self.i-1].get()]
        self.item_var[self.i-1].set(item_name)

        item_price = self.prices_dict[self.itemno_var[self.i-1].get()]
        self.price_var[self.i-1].set(item_price)

    def fetch_cost(self,event):
        item_cost = float(self.price_var[self.i-1].get()) * int(self.qty.get())
        self.cost_var[self.i-1].set(item_cost)

        sum = self.total_val.get() + item_cost
        self.total_val.set(sum)

    def row_create(self,event=None,first=False):   

        self.itemno_var.append(IntVar())
        self.item_var.append(StringVar())
        self.qty_var.append(IntVar())
        self.price_var.append(DoubleVar())
        self.cost_var.append(DoubleVar())

        if not first:
            time = datetime.now()
            push_time = time.strftime('%Y-%m-%d %H:%M:%S')

            push_info = [int(self.itemno.get()), self.item.get(), int(self.qty.get()), float(self.price.get()), float(self.cost.get()),push_time]
            self.purchase_data.append(push_info)

        self.itemno = Entry(self.inputs,textvariable=self.itemno_var[self.i])
        self.itemno.grid(row=self.i+1, column=0,sticky='WE' )
        self.itemno.bind('<FocusOut>',self.fetch_item)
        self.qty = Entry(self.inputs,textvariable=self.qty_var[self.i])
        self.qty.grid(row=self.i+1, column=2,sticky='WE')
        self.qty.bind('<Tab>',self.fetch_cost)
        self.item = Entry(self.inputs,state='readonly',textvariable=self.item_var[self.i])
        self.item.grid(row=self.i+1, column=1,sticky='WE' )
        self.price = Entry(self.inputs,state='readonly',textvariable=self.price_var[self.i])
        self.price.grid(row=self.i+1, column=3,sticky='WE')
        self.cost = Entry(self.inputs,state='readonly',textvariable=self.cost_var[self.i])
        self.cost.grid(row=self.i+1,column=4,sticky='WE')

        self.enter.destroy()
        self.next.destroy()
        self.end.destroy()
        self.total_label.destroy()
        self.total.destroy()
        self.disp_price.destroy()

        self.button_create()

        self.i += 1

        
    def button_create(self,event=None):
        
        self.enter = Button(self.inputs, text='Save')
        self.enter.bind('<Button-1>',self.save)
        self.enter.grid(row=self.i+3, column=0, sticky='w',pady=10)

        self.next = Button(self.inputs, text='Add')
        self.next.bind('<Button-1>',self.row_create)
        self.next.grid(row=self.i+3, column=2,pady=10)

        self.disp_price = Button(self.inputs, text='Prices')
        self.disp_price.bind('<Button-1>',self.display)
        self.disp_price.grid(row=self.i+3, column=4, sticky='e',pady=10)

        self.total_label = Label(self.inputs,text='Total')
        self.total_label.grid(row=self.i+4,column=0,sticky='W')
        self.total = Entry(self.inputs,state='readonly',textvariable=self.total_val)
        self.total.grid(row=self.i+4,column=1,sticky='WE',columnspan=4)

        self.end = Button(self.inputs,text='Quit' )
        self.end.grid(row=self.i+5,column=2,pady=10)
        self.end.bind('<Button-1>',self.quit)

    def save(self,event=None):
        if self.purchase_data:
            with UseDatabase(self.dbconfig) as cur:
                cur.execute('select max(bill_no) from shop_purchases;')
                bill_no = cur.fetchall()[0][0]
                print(bill_no)
                if bill_no:
                    bill_no += 1
                else:
                    bill_no = 1
                for row in self.purchase_data:
                    sql = ''' insert into shop_purchases values
                        ({},{},'{}',{},{},{},'{}')'''.format(bill_no,row[0],row[1],row[2],row[3],row[4],row[5])
                    cur.execute(sql)
            self.purchase_data = list()
            self.__init__(self.root)
        else:
            messagebox.showwarning('Null value','Please enter some values')
        
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

    def quit(self,event=None):
        self.root.destroy()
               
App(root)
root.mainloop()