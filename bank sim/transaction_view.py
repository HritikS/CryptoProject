import sqlite3

conn = sqlite3.connect('BankDB.db')
c = conn.cursor()

def trans():
    for i in c.execute("SELECT * FROM sampe;"):
        print(i)

def users():
    for i in c.execute("SELECT * FROM USERS;"):
        print(i)


while True:
    ptr = int(input("1. Users\n2. Transactions\n3. Exit\n"))
    if ptr == 1:
        users()
    elif ptr == 2:
        trans()
    elif ptr == 3:
        exit()
    else:
        print("Wrong input\n")
