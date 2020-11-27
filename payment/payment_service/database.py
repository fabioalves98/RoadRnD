import sqlite3, time, datetime


def timestampToDateTime(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")

class Database:

    def __init__(self, filename='database.db'):
        self.connection = sqlite3.connect(filename)
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
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('ABCDEFGH', '32.90', 'EUR')")
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('ABCDEFGA', '100.00', 'EUR')")
            self.c.execute("INSERT INTO CLIENT_BALANCE VALUES ('ABCDEFGB', '2.32', 'EUR')")
            # TODO: Fix the item list here.
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            self.c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk84729DHDSA7JDG6', '12.98', 'EUR', 'Rental/12.98', ?, ?, 'created', 'ABCDEFGB')''', p)
            ts = time.time()
            p = (timestampToDateTime(ts), timestampToDateTime(ts),)
            self.c.execute('''INSERT INTO PAYMENTS VALUES ('PAYMENT-BDSk88929DHDSA7JDG6', '28.90', 'EUR', 'Rental/28.90', ?, ?, 'created', 'ABCDEFGH')''', p)
            self.connection.commit()
        content = self.c.execute('SELECT * FROM CLIENT_BALANCE')
        for c in content:
            print(c)
        content = self.c.execute('SELECT * FROM PAYMENTS')
        for c in content:
            print(c)
