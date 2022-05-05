from dbcm import UseDatabase
import mysql.connector as s

config = {'host':'localhost',
        'user':'pythonact1',
        'passwd':'python123',
        'database': 'mysql'}

conn = s.connect(**config)
if conn.is_connected():
    print('Success')