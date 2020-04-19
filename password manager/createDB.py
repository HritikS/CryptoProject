import sqlite3


if __name__ == "__main__":
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE USERS(ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT, PASSWORD TEXT);")
    c.execute("CREATE TABLE PASSES(ID INTEGER, APPLICATION TEXT, USERNAME TEXT, PASSWORD TEXT, IV TEXT);")
    print("DataBase Created.")
