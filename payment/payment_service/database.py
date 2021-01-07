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

        self.filename = filename

        connection, c = self.getContext()
        # Initialize and create tables, populate them if they aren't populated already

        c.execute(
            "CREATE TABLE IF NOT EXISTS CLIENT_BALANCE (client_id TEXT PRIMARY KEY, funds TEXT, currency TEXT)")
        c.execute(''' CREATE TABLE IF NOT EXISTS PAYMENTS 
                            (payment_id TEXT PRIMARY KEY, total TEXT, currency TEXT, items TEXT, create_time TEXT, update_time TEXT,
                            state TEXT, client_id TEXT, FOREIGN KEY(client_id) REFERENCES CLIENT_BALANCE(client_id)) ''')

        connection.commit()
        content = c.execute('SELECT * FROM CLIENT_BALANCE')
        empty = True
        for cd in content:
            empty = False
            break
        
        ## If we have an empty db, fill with stuff
        if empty:
            print("Empty, filling DB")
            c.execute("INSERT INTO CLIENT_BALANCE VALUES ('1234567', '32.90', 'EUR')")
            c.execute("INSERT INTO CLIENT_BALANCE VALUES ('1234568', '100.00', 'EUR')")
            c.execute("INSERT INTO CLIENT_BALANCE VALUES ('1234569', '2.32', 'EUR')")
            # TODO: Fix the item list here.
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk84729DHDSA7JDG6', '12.98', 'EUR', 'Rental:12.98', ?, ?, 'created', '1234567')''', p)
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk88929DHDSA7JDG6', '28.90', 'EUR', 'Rental:28.90', ?, ?, 'approved', '1234567')''', p)
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk88929DDDSA7JDG6', '7.13', 'EUR', 'Rental:7.13', ?, ?, 'approved', '1234567')''', p)
            connection.commit()
        # content = self.c.execute('SELECT * FROM CLIENT_BALANCE')
        # for c in content:
        #     print(c)
        # content = self.c.execute('SELECT * FROM PAYMENTS')
        # for c in content:
        #     print(c)
        print("yes", flush=True)

        c.close()
        connection.close()

    def getContext(self):
        connection = sqlite3.connect(self.filename, check_same_thread=False)
        c = connection.cursor()
        return connection, c

    def insertPayment(self, payment):
        connection, c = self.getContext()
        ts = time.time()
        date_time = timestampToDateTime(ts)
        p = (payment["id"], payment["total"], payment["currency"], itemlistToString(payment["item_list"]), date_time, date_time, payment["client_id"])
        try:
            c.execute('''INSERT INTO PAYMENTS VALUES (?, ?, ?, ?, ?, ?, 'created', ?)''', p)
        except sqlite3.IntegrityError:
            print("A payment with this ID '%s' already exists" % payment["id"])
            c.close()
            connection.close()
            return False

        c.close()
        connection.commit()
        connection.close()
        return True

    def getPayments(self, payment_id=None):
        connection, c = self.getContext()
        pays = []    
        if not payment_id:
            content = c.execute('SELECT * FROM PAYMENTS')
            for cd in content:
                payment = {"id": cd[0], "item_list" : stringToItemlist(cd[3]), "total": cd[1], "currency": cd[2], "total_tax": 0, "client_id": cd[7], 'state': cd[6], 'time': cd[5]}
                pays.append(payment)
            c.close()
            connection.close()
            return pays
        p = (payment_id, )
        content = c.execute('SELECT * FROM PAYMENTS WHERE payment_id=?', p)
        for cd in content:
            payment = {"id": cd[0], "item_list" : stringToItemlist(cd[3]), "total": cd[1], "currency": cd[2], "total_tax": 0, "client_id": cd[7], 'state': cd[6], 'time': cd[5]}
            c.close()
            connection.close()
            return payment
        c.close()
        connection.close()
        return None

    def getClientPayments(self, client_id):
        connection, c = self.getContext()
        pays = []
        p = (client_id, )
        content = c.execute('SELECT * FROM PAYMENTS WHERE client_id=?', p)
        for cd in content:
            payment = {"id": cd[0], "item_list" : stringToItemlist(cd[3]), "total": cd[1], "currency": cd[2], "total_tax": 0, "client_id": cd[7], 'state': cd[6], 'time': cd[5]}    
            pays.append(payment)

        c.close()
        connection.close()
        return pays
    
    def deletePayment(self, payment_id):
        connection, c = self.getContext()
        p = (payment_id, )
        try:
            c.execute('DELETE FROM PAYMENTS WHERE payment_id=?', p)
            connection.commit()
            c.close()
            connection.close()
        except Exception as e:
            print(e, flush=True)
            c.close()
            connection.close()
            return False
        return True

    def insertClient(self, client):
        connection, c = self.getContext()
        p = (client["id"], '0.00', client["currency"])
        try:
            c.execute("INSERT INTO CLIENT_BALANCE VALUES (?, ?, ?)", p)
        except sqlite3.IntegrityError:
            print("A client with id '%s' already exists" % client["id"])
            c.close()
            connection.close()
            return False


        connection.commit()
        c.close()
        connection.close()

        return True


    def getClients(self, client_id=None):
        connection, c = self.getContext()
        clients = []
        if not client_id:
            content = c.execute('SELECT * FROM CLIENT_BALANCE')
            for cd in content:
                client = {"id": cd[0], "balance" : cd[1], "currency": cd[2]}
                clients.append(client)
            c.close()
            connection.close()
            return clients
        p = (client_id, )
        content = c.execute('SELECT * FROM CLIENT_BALANCE WHERE client_id=?', p)
        for cd in content:
            client = {"id": cd[0], "balance" : cd[1], "currency": cd[2]}
            c.close()
            connection.close()
            return client
        c.close()
        connection.close()
        return None

    def updateClientFunds(self, client_id, new_balance):
        connection, c = self.getContext()
        p = (new_balance, client_id,)
        try:
            c.execute('UPDATE CLIENT_BALANCE SET funds = ? WHERE client_id=?',p)
            connection.commit()
            c.close()
            connection.close()
            return True
        except:
            c.close()
            connection.close()
            return False

    def updatePaymentStatus(self, payment_id, status):
        connection, c = self.getContext()

        ts = time.time()
        date_time = timestampToDateTime(ts)
        p = (status, date_time, payment_id,)
        try:
            c.execute('UPDATE PAYMENTS SET state = ?, update_time=? WHERE payment_id=?',p)
            connection.commit()
            c.close()
            connection.close()
            return True
        except:
            c.close()
            connection.close()
            return False

        


