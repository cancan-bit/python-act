import mysql.connector as s

class UseDatabase():
    
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.conn = s.connect(**self.config)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self,exc_type,exc_value, exc_trace):
        self.conn.commit()
        self.cur.close()
        self.conn.close()