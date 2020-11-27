import sqlite3, time, datetime


def timestampToDateTime(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")

def itemlistToString(item_list):

    s = ""
    for item in item_list:
        s += str(item["item_name"]) + ":" + str(item["item_price"]) + ","

    return s[:len(s)-1]

def stringToItemlist(s):
    item_list = []
    items = s.split(",")
    for item in items:
        name_price = item.split(":")
        item_list.append({"item_name": name_price[0], "item_price": name_price[1]})
    return item_list


class Database:

    def __init__(self, filename='database.db'):
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.connection.cursor()

        # Initialize and create tables, populate them if they aren't populated already

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS CLIENT_BALANCE (client_id TEXT PRIMARY KEY, funds TEXT, currency TEXT)")
        self.c.execute(''' CREATE TABLE IF NOT EXISTS PAYMENTS 
                            (payment_id TEXT PRIMARY KEY, total TEXT, currency TEXT, items TEXT, create_time TEXT, update_time TEXT,
                            state TEXT, client_id TEXT, FOREIGN KEY(client_id) REFERENCES CLIENT_BALANCE(client_id)) ''')

        self.connection.commit()
        content = self.c.execute('SELECT * FROM CLIENT_BALANCE')
        empty = True
        for c in content:
            empty = False
            break
        
        ## If we have an empty db, fill with stuff
        if empty:
            print("Empty, filling DB")
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('AA-01-AA', '32.90', 'EUR')")
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('GD-02-XA', '100.00', 'EUR')")
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('LD-34-CV', '2.32', 'EUR')")
            # TODO: Fix the item list here.
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            self.c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk84729DHDSA7JDG6', '12.98', 'EUR', 'Rental:12.98', ?, ?, 'created', 'AA-01-AA')''', p)
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            self.c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk88929DHDSA7JDG6', '28.90', 'EUR', 'Rental:28.90', ?, ?, 'created', 'LD-34-CV')''', p)
            self.connection.commit()
        # content = self.c.execute('SELECT * FROM CLIENT_BALANCE')
        # for c in content:
        #     print(c)
        # content = self.c.execute('SELECT * FROM PAYMENTS')
        # for c in content:
        #     print(c)

    def insertPayment(self, payment):
        ts = time.time()
        date_time = timestampToDateTime(ts)
        p = (payment["id"], payment["total"], payment["currency"], itemlistToString(payment["item_list"]), date_time, date_time, payment["client_id"])
        try:
            self.c.execute('''INSERT INTO PAYMENTS VALUES (?, ?, ?, ?, ?, ?, 'created', ?)''', p)
        except sqlite3.IntegrityError:
            print("A payment with this ID '%s' already exists" % payment["id"])
            return False

        self.connection.commit()

        return True

    def getPayments(self, payment_id=None):
        
        pays = []    
        if not payment_id:
            content = self.c.execute('SELECT * FROM PAYMENTS')
            for c in content:
                payment = {"id": c[0], "item_list" : stringToItemlist(c[3]), "total": c[1], "currency": c[2], "total_tax": 0, "client_id": c[6]}
                pays.append(payment)
            return pays
        p = (payment_id, )
        content = self.c.execute('SELECT * FROM PAYMENTS WHERE payment_id=?', p)
        for c in content:
            payment = {"id": c[0], "item_list" : stringToItemlist(c[3]), "total": c[1], "currency": c[2], "total_tax": 0, "client_id": c[6]}
            return payment
        return None


