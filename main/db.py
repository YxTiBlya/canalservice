import psycopg2

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postresql", 
            user="admin", 
            password="admin",
        )
        self.cursor = self.connection.cursor()


    # excel
    def table_exists(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM main_table')
            result = self.cursor.fetchall()
            return result

    def table_clear(self):
        with self.connection:
            self.cursor.execute('DELETE FROM main_table')

    def table_insert(self, id, order, costDoll, costRub, date):
        with self.connection:
            self.cursor.execute('INSERT INTO main_table VALUES (%s,%s, %s, %s, %s)',(id, order, costDoll, costRub, date))


    # tg
    def order_exists(self, order):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM main_orders WHERE ordernumber = %s',(order,))
            result = self.cursor.fetchone()
            return result

    def add_order(self, order):
        with self.connection:
            self.cursor.execute('INSERT INTO main_orders (ordernumber) VALUES (%s)',[order])
    
    def get_orders(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM main_orders')
            result = self.cursor.fetchall()
            return result

    def del_order(self, order):
        with self.connection:
            self.cursor.execute('DELETE FROM main_orders WHERE ordernumber = %s',(order,))

    
