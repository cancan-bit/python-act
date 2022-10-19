from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as s
from dbcm import UseDatabase
from datetime import datetime
from customers import *
import re
 
root = Tk()
 
class App():
 
    def __init__(self,root):
 
        self.itemno_var =[]
        self.item_var =[]
        self.price_var =[]
        self.qty_var =[]
        self.cost_var =[]

        self.itemno =[]
        self.item =[]
        self.price =[]
        self.qty=[]
        self.cost =[]

        self.total_val = DoubleVar()
        self.cust_pno = IntVar()
        self.pts_avail = IntVar()
        self.pts_used = IntVar()
        self.cust_name=StringVar()
        self.final_total = DoubleVar()
        self.pts_used.set(0)

        self.purchase_hist = {}

        self.dbconfig = {'host':'localhost',
                         'user':'pythonact1',
                         'passwd':'python123',
                         'database': 'shop_info',
                         'port': 3308
        }

        self.root = root
        self.i = 0     #Row tracker
        self.data = []
        self.c=1  #Purchase history tracker
 
        self.purchase_data = []
        self.item_dict = dict()
        self.prices_dict = dict()
        self.cust_dict = dict()

        self.main_frame = Frame(self.root)
        self.canvas = Canvas(self.main_frame,background = '#b2bdff')
        self.new_frame = Frame(self.canvas,background='#b2bdff')
        self.new_frame.grid(row=0,column=0, columnspan=2)
        self.main_frame.pack(fill='both',expand=1)
        self.canvas.pack(side='left',fill='both',expand=1)

        self.inputs = Frame(self.new_frame,background = '#fdff86',padx=20,pady=20)
        self.info = Frame(self.new_frame,background='#9bf6ff',padx=20,pady=20)

        self.canvas.create_window((0,0),window=self.new_frame,anchor='nw')


        self.root.title('Cashier')
        self.root.configure(background='#b2bdff')
        self.canvas.columnconfigure(0,weight=20)
        self.canvas.columnconfigure(1,weight=5)
 
        Label(self.new_frame, text='Welcome to the cashier app', font='Helvetica 26 bold',background='#b2bdff').grid(row=0,column=0,pady=10)
 
        self.inputs.columnconfigure(0,weight=2)
        self.inputs.columnconfigure(1,weight=10)
        self.inputs.columnconfigure(2,weight=2)
        self.inputs.columnconfigure(3,weight=2)
        self.inputs.columnconfigure(4,weight=2)
        self.inputs.grid(row=1,column=0,sticky='ns',padx=10,pady=20)
 
 
        Label(self.inputs,text='Item no.', font = 'Calibri 20').grid(row=0,column=0,sticky='EW' )
        Label(self.inputs,text='Item', font = 'Calibri 20').grid(row=0,column=1,sticky='EW')
        Label(self.inputs,text='Qty', font = 'Calibri 20').grid(row=0,column=2,sticky='EW' )
        Label(self.inputs,text='Price', font = 'Calibri 20').grid(row=0,column=3,sticky='EW')
        Label(self.inputs,text='Cost', font = 'Calibri 20').grid(row=0,column=4,sticky='EW')
 
        scroll = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y')
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")) )

        
        with UseDatabase(self.dbconfig) as cur:
            sql = '''create table if not exists shop_prices(
                    itemno int primary key,
                    item_name varchar(30),
                    price float(10,2));
                    '''
            cur.execute(sql)
            try:
                sql = '''insert into shop_prices values
                          (1,'Soap',300),
                          (2,'Detergent',250),
                          (3, 'Shampoo',340),
                          (4,'Face cream',460),
                          (5,'Perfume',550),
                          (6,'Toothpaste',100),
                          (7,'Hair Gel',230),
                          (8,'Notebook',50),
                          (9,'Pen',20),
                          (10,'Toothbrush',80);
                       '''
                cur.execute(sql)
            except:
                pass
 
            sql = '''create table if not exists shop_purchases (
                        bill_no int,
                        item_no int,
                        item varchar(30),
                        qty int,
                        price float(10,2),
                        cost float(10,2),
                        time datetime,
                        phone_no int,
                        c_name varchar(30),
                        pts_use int,
                        foreign key (item_no) references shop_prices(item_no),
                        foreign key (phone_no) references customer_info(phone_no)
                        ) ;'''
            cur.execute(sql)

            sql = '''create table if not exists customer_info(
                phone_no int primary key,
                customer_name varchar(30),
                points int
            );
            '''         
            cur.execute(sql)
 
        with UseDatabase(self.dbconfig) as cur:
            sql = 'select * from {}'.format('shop_prices')
            cur.execute(sql)
            self.data = cur.fetchall()

            sql = '''select phone_no,points from customer_info'''
            cur.execute(sql)
            inf = cur.fetchall()
            for i in inf:
                self.cust_dict[i[0]] = i[1]
 
        for i in self.data:
            self.item_dict[i[0]] = i[1]
            self.prices_dict[i[0]] = i[2]

        self.info.grid(row=2,column=0,padx=10,pady=20)
        self.display()

        self.button_create()
        self.row_create()
 
    def fetch_item(self,event):
        s = str(event.widget)  
        x = re.findall('\d',s[:15])
        err = len(x)   #-1 for excluding the last number
        s = str(event.widget)[36+err:]
        print(event.widget)
        pos = int(s)//11 
        print(pos)
        try: 
            item_name = self.item_dict[self.itemno_var[pos].get()]
            self.item_var[pos].set(item_name)
 
            item_price = self.prices_dict[self.itemno_var[pos].get()]
            self.price_var[pos].set(item_price)
        except Exception as e:
            print(e)
            messagebox.showerror('Error!','Invalid item number.')
            self.itemno_var[pos].set(0)
 
    def fetch_cost(self,event):
        try:
            s = str(event.widget)  
            x = re.findall('\d',s[:15])
            err = len(x)   #-1 for excluding the last number
            s = str(event.widget)[36+err:]
            pos = int(s)//11 
            print(pos)
            if int(self.qty[pos].get()) >= 0:
                item_cost = float(self.price_var[pos].get()) * int(self.qty[pos].get())
                self.cost_var[pos].set(item_cost)
                self.total_val.set(0)
                for i in self.cost_var:
                    val = self.total_val.get()
                    dat = i.get()

                    self.total_val.set(val+dat)
                f_total = int(self.total_val.get()) - int(self.pts_used.get())
                self.final_total.set(f_total)
                print(self.final_total.get())
            else:
                messagebox.showerror('Error!','Invalid value for qty.')
                self.qty_var[pos].set(0)
        except Exception as e:
            print(e)
            messagebox.showerror('Error!','Invalid value for qty.')
 
    def row_create(self,event=None,first=False):   
 
        self.itemno_var.append(IntVar())
        self.item_var.append(StringVar())
        self.qty_var.append(IntVar())
        self.price_var.append(DoubleVar())
        self.cost_var.append(DoubleVar())
        
        self.itemno.append(None)
        self.item.append(None)
        self.qty.append(None)
        self.price.append(None)
        self.cost.append(None)
 
        self.itemno[self.i] = Entry(self.inputs,textvariable=self.itemno_var[self.i],font =('Calibri 20'))
        self.itemno[self.i].grid(row=self.i+1, column=0,sticky='WE' )
        self.itemno[self.i].bind('<Tab>',self.fetch_item)
        self.qty[self.i] = Entry(self.inputs,textvariable=self.qty_var[self.i],font =('Calibri 20'))
        self.qty[self.i].grid(row=self.i+1, column=2,sticky='WE')
        self.qty[self.i].bind('<Tab>',self.fetch_cost)
        self.item[self.i] = Entry(self.inputs,state='readonly',textvariable=self.item_var[self.i],font =('Calibri 20'))
        self.item[self.i].grid(row=self.i+1, column=1,sticky='WE' )
        self.price[self.i] = Entry(self.inputs,state='readonly',textvariable=self.price_var[self.i],font =('Calibri 20'))
        self.price[self.i].grid(row=self.i+1, column=3,sticky='WE')
        self.cost[self.i] = Entry(self.inputs,state='readonly',textvariable=self.cost_var[self.i],font =('Calibri 20'))
        self.cost[self.i].grid(row=self.i+1,column=4,sticky='WE')
 
        self.enter.destroy()
        self.next.destroy()
        self.end.destroy()
        self.total_label.destroy()
        self.total.destroy()
        self.disp_price.destroy()
        self.cust_pno_label.destroy()
        self.cust_pno_entry.destroy()
        self.pts_avail_entry.destroy()
        self.pts_avail_label.destroy()
        self.pts_used_entry.destroy()
        self.pts_used_label.destroy()
        self.user_create.destroy()
        self.final_total_label.destroy()
        self.final_total_entry.destroy()
        self.cust_name_entry.destroy()
        self.cust_name_label.destroy()
 
        self.button_create()
 
        self.i += 1
 
 
    def button_create(self,event=None):
 
        self.enter = Button(self.inputs, text='Save', font =('Calibri 20'))
        self.enter.bind('<Button-1>',self.save)
        self.enter.grid(row=self.i+3, column=0, sticky='w',pady=10)
 
        self.next = Button(self.inputs, text='Add', font =('Calibri 20'))
        self.next.bind('<Button-1>',self.row_create)
        self.next.grid(row=self.i+3, column=2,pady=10)
 
        self.disp_price = Button(self.inputs, text='Past Purchases', font =('Calibri 20'))
        self.disp_price.bind('<Button-1>',self.purchases)
        self.disp_price.grid(row=self.i+3, column=4, sticky='e',pady=10)
 
        self.total_label = Label(self.inputs,text='Sub Total', font = 'Calibri 20',background = '#fdff86')
        self.total_label.grid(row=self.i+4,column=0,sticky='W')
        self.total = Entry(self.inputs,state='readonly',textvariable=self.total_val,font =('Calibri 20'))
        self.total.grid(row=self.i+4,column=1,sticky='WE',columnspan=4)

        self.cust_pno_label = Label(self.inputs, text ='Phone No.',font = 'Calibri 20', background='#fdff86')
        self.cust_pno_label.grid(row=self.i+5,column=0,sticky='W')
        self.cust_pno_entry = Entry(self.inputs,textvariable=self.cust_pno,font=('Calibri 20'))
        self.cust_pno_entry.grid(row=self.i+5,column=1,sticky='EW',columnspan=4)
        self.cust_pno_entry.bind('<Tab>',self.fetch_rec)

        self.cust_name_label = Label(self.inputs, text ='Name',font = 'Calibri 20', background='#fdff86')
        self.cust_name_label.grid(row=self.i+6,column=0,sticky='W')
        self.cust_name_entry = Entry(self.inputs,state='readonly',textvariable=self.cust_name,font=('Calibri 20'))
        self.cust_name_entry.grid(row=self.i+6,column=1,sticky='EW',columnspan=4)

        self.pts_avail_label = Label(self.inputs, text ='Points Available',font = 'Calibri 20', background='#fdff86')
        self.pts_avail_label.grid(row=self.i+7,column=0,sticky='W')
        self.pts_avail_entry = Entry(self.inputs,state='readonly',textvariable=self.pts_avail,font=('Calibri 20'))
        self.pts_avail_entry.grid(row=self.i+7,column=1,sticky='EW',columnspan=4)

        self.pts_used_label = Label(self.inputs, text ='Points Used',font = 'Calibri 20', background='#fdff86')
        self.pts_used_label.grid(row=self.i+8,column=0,sticky='W')
        self.pts_used_entry = Entry(self.inputs,textvariable=self.pts_used,font=('Calibri 20'))
        self.pts_used_entry.grid(row=self.i+8,column=1,sticky='EW',columnspan=4)
        self.pts_used_entry.bind('<Tab>',self.manage_rec)

        self.final_total_label = Label(self.inputs, text='Total',font='Calibri 20',background='#fdff86')
        self.final_total_label.grid(row=self.i+9,column=0,sticky='W')
        self.final_total_entry = Entry(self.inputs,state='readonly',textvariable=self.final_total,font=("Calibri 20"))
        self.final_total_entry.grid(row=self.i+9,column=1,sticky='ew',columnspan=4)
        f_total = float(self.total_val.get()) - (float(self.pts_used.get())*0.01)
        self.final_total.set(f_total)
        print(self.final_total.get())

        self.user_create = Button(self.inputs, text='Create New User', font = ('Calibri 20'))
        self.user_create.grid(row=self.i+10,column=2,pady=10)
        self.user_create.bind('<Button-1>',self.new_user)

        self.end = Button(self.inputs,text='Quit', font =('Calibri 20'))
        self.end.grid(row=self.i+11,column=2,pady=10)
        self.end.bind('<Button-1>',self.quit)

    def new_user(self,event=None):
        self.user_win= Toplevel(background='#b2bdff')
        self.phone_info = IntVar()
        self.name_info = StringVar()

        Label(self.user_win,text='New User', background='#b2bdff',font='Calibri 20').grid(row=0,column=1,sticky='nsew',padx=10,pady=10)

        Label(self.user_win,text='Phone No.',background='#b2bdff',font='Calibri 20').grid(row=1,column=0,sticky='w')
        self.phone_info_entry = Entry(self.user_win,textvariable=self.phone_info,font = ('Calibri 20'))
        self.phone_info_entry.grid(row=1,column=1,sticky='ew',padx=10,pady=10)

        Label(self.user_win,text='Name',background='#b2bdff',font='Calibri 20').grid(row=2,column=0,sticky='w')
        self.cust_name_entry = Entry(self.user_win,textvariable=self.name_info,font = ('Calibri 20'))
        self.cust_name_entry.grid(row=2,column=1,sticky='ew',pady=10,padx=10)

        self.push_db = Button(self.user_win,text = 'Create', font = ('Calibri 20'))
        self.push_db.grid(row=3,column=2,sticky='EW',padx=20,pady=20)
        self.push_db.bind('<Button-1>',self.push_data)

    def push_data(self,event=None):
        phone_no = self.phone_info.get()
        name = self.name_info.get()
        print(phone_no,name)
        try:
            if phone_no and name:
                print('In here')
                create_acc(phone_no,name)
                self.cust_dict[phone_no] = name
        except AlreadyExistsException:
            messagebox.showerror('Error!','Phone No. already exists')
        self.user_win.destroy()

    def manage_rec(self,event=None):
        print(self.pts_used.get(),'Inside manage_rec')
        if int(self.pts_used.get()) > 0:
            if int(self.pts_used.get()) > int(self.pts_avail.get()):
                messagebox.showerror('Error!','Not enough points')
            else:
                f_total = int(self.total_val.get()) - int(self.pts_used.get())*0.01
                self.final_total.set(f_total)
                with UseDatabase(dbconfig) as cur:
                    sql = "update customer_info set points = points - {} where phone_no= {}".format(int(self.pts_used.get()),int(self.cust_pno))
                    cur.execute(sql)
        else:
            messagebox.showerror('Error!','Points must be positive')

    def fetch_rec(self,event=None):
        try:
            name,pts = fetch_info(self.cust_pno.get())
            self.cust_name.set(name)
            print(self.cust_name.get())
            self.pts_avail.set(pts)      
        except:
            messagebox.showinfo('Error!','Phone No. not registered. Create a new account')    

    def save(self,event=None):
        time = datetime.now()
        push_time = time.strftime('%Y-%m-%d %H:%M:%S')

        pts_to_add = float(self.final_total.get())*0.1

        for j in range(self.i):
            push_info = [int(self.itemno[j].get()), self.item[j].get(), int(self.qty[j].get()), 
            float(self.price[j].get()), float(self.cost[j].get()),push_time,int(self.cust_pno.get()),self.cust_name.get()]
            if 0 not in push_info:
                self.purchase_data.append(push_info)

        if self.purchase_data:
            with UseDatabase(self.dbconfig) as cur:
                cur.execute('select max(bill_no) from shop_purchases;')
                bill_no = cur.fetchall()[0][0]
                if bill_no:
                    bill_no += 1
                else:
                    bill_no = 1
                for row in self.purchase_data:
                    if row[0] != 0 and row[6] != 0:
                        sql = ''' insert into shop_purchases values
                            ({},{},'{}',{},{},{},'{}',{},'{}')'''.format(bill_no,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        cur.execute(sql)
                        sql = 'update customer_info set points = points + {} where phone_no = {}'.format(pts_to_add,row[6])
                        cur.execute(sql)

            self.purchase_data = list()
            self.main_frame.destroy()
            self.__init__(self.root)
        elif not self.cust_pno.get():
            print(self.purchase_data)
            messagebox.showwarning('Error!','Create new user')
        else:
            messagebox.showwarning('Error!','Please fill the empty values')
 
    def display(self):

        head = ('Item_no.','Item_name','Price') 
        
        tree = ttk.Treeview(self.info,columns=head, show='headings')

        style = ttk.Style(self.info)
        style.configure('Treeview',font=('Calibri 20'),rowheight='30',padx=10)
        style.configure('Treeview.Heading',font=('Arial 23 bold'),rowheight='27')

        tree.heading('Item_no.',text='Item No.')
        tree.heading('Item_name', text='Item Name')
        tree.heading('Price', text='Price')

        for row in self.data:
            tree.insert('', END,values=row)

        tree.grid(row=0,column=0,sticky='ew')

    def purchases(self,event=None):
        values= purchase_data()
        self.max_bno = len(values)
        for i in values:
            self.purchase_hist[int(i[0][0])] = i


        self.win = Toplevel()
        self.win.configure(background='#b2bdff')
        self.create_plist(self.win)
   
        self.win.mainloop()

    def create_plist(self,w):

        try:
            self.tree.destroy()
            self.prev.destroy()
            self.next.destroy()
        except:
            pass

        head = ('bill_no','i_no','i_name','qty','price','cost')
        
        self.tree = ttk.Treeview(w, columns=head, show='headings')

        style = ttk.Style(w)
        style.configure('Treeview',font=('Calibri 20'),rowheight='30',padx=10)
        style.configure('Treeview.Heading',font=('Arial 23 bold'),rowheight='27')

        self.tree.heading('bill_no',text='Bill No.')
        self.tree.heading('i_no', text='Item No.')
        self.tree.heading('i_name', text='Item')
        self.tree.heading('qty',text='Qty')
        self.tree.heading('price',text='Price')
        self.tree.heading('cost',text='Cost')

        run_tot = 0
        pno = 0
        c_name = ''
        date = ''
        point_used = 0
        for row in self.purchase_hist[self.c]:
            print(row)
            run_tot += int(row[-4])
            date = row[-3]
            pno = row[-2]
            c_name = row[-1]
            self.tree.insert('',END,values=row)

        self.tree.grid(row=0,column=0,columnspan=2)

        
        Label(w, text='Phone No', font='Helvetica 26 bold',background='#b2bdff').grid(row=1,column=0)
        Label(w, text=str(pno),font='Helvetica 26 bold',background='#b2bdff').grid(row=1,column=1,sticky='EW')

        Label(w, text='Name', font='Helvetica 26 bold',background='#b2bdff').grid(row=2,column=0)
        Label(w, text=str(c_name),font='Helvetica 26 bold',background='#b2bdff').grid(row=2,column=1,sticky='EW')

        Label(w, text='Date', font='Helvetica 26 bold',background='#b2bdff').grid(row=3,column=0)
        Label(w, text=date,font='Helvetica 26 bold',background='#b2bdff').grid(row=3,column=1,sticky='EW')

        Label(w, text='Sub-total', font='Helvetica 26 bold',background='#b2bdff').grid(row=4,column=0)
        Label(w, text=str(run_tot),font='Helvetica 26 bold',background='#b2bdff').grid(row=4,column=1,sticky='EW')

        Label(w, text='Points Used', font='Helvetica 26 bold',background='#b2bdff').grid(row=5,column=0)
        Label(w, text=str(point_used),font='Helvetica 26 bold',background='#b2bdff').grid(row=5,column=1,sticky='EW')

        Label(w, text='Total', font='Helvetica 26 bold',background='#b2bdff').grid(row=6,column=0)
        Label(w, text=str(run_tot + point_used*0.01),font='Helvetica 26 bold',background='#b2bdff').grid(row=6,column=1,sticky='EW')


        self.prev = Button(w, text='Previous',font=('Calibri 20'))
        self.prev.bind('<Button-1>', self.increment)
        self.prev.grid(row=7,column=0)
     
        self.next = Button(w, text='Next',font=('Calibri 20'))
        self.next.bind('<Button-1>', self.decrement)
        self.next.grid(row=7,column=1)


    def increment(self, event=None):
        if self.c > 1:
            self.c -= 1
            self.create_plist(self.win)


    def decrement(self,event=None):
        if self.c < self.max_bno:
            self.c += 1 
            self.create_plist(self.win)


    def quit(self,event=None):
        self.root.destroy()
 
App(root)
root.mainloop()