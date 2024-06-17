import sqlite3

conn = sqlite3.connect('hotdeal.db')

c = conn.cursor()
c.execute("Create table hotdeal ")