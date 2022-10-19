import mysql.connector as s
from dbcm import UseDatabase

dbconfig = {'host':'localhost',
            'user':'pythonact1',
            'passwd':'python123',
            'database': 'shop_info',
            'port': 3308
        }


def create_acc(phone_no, cust):
    with UseDatabase(dbconfig) as cur:
        sql = "select * from customer_info where phone_no = {}".format(phone_no)
        cur.execute(sql)
        data = cur.fetchall()
        if not data:
            sql = " insert into customer_info values({},'{}',{})".format(phone_no,cust,0)
            cur.execute(sql)

def fetch_info(phone_no):
    with UseDatabase(dbconfig) as cur:
        sql = "select * from customer_info where phone_no = {}".format(phone_no)
        cur.execute(sql)
        data = cur.fetchone()
        return data

def modify_info(phone_no,pts):
       with UseDatabase(dbconfig) as cur:
            sql = "update customer_info set points = points + {} where phone_no= {}".format(pts,phone_no)
            cur.execute(sql)


def purchase_data():
    with UseDatabase(dbconfig) as cur:
        sql = 'select max(bill_no) from shop_purchases;'
        cur.execute(sql)
        val = cur.fetchone()[0]
        data = []
        for i in range(1,val+1):
            sql = 'select * from shop_purchases where bill_no = {}'.format(i)
            cur.execute(sql)
            info = cur.fetchall()
            data.append(info)
    return data
