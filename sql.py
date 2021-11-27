import sqlite3

def select():
    con = sqlite3.connect('country1.db')
    cursor = con.cursor()
    cursor.execute('select * from country')
    res= cursor.fetchall()
    return res