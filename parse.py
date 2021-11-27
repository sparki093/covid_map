import sqlite3

import requests
from bs4 import BeautifulSoup
url = 'https://russian-trade.com/coronavirus-russia/'
r = requests.get(url)
text = r.text
soup = BeautifulSoup(text, 'lxml')
all = soup.find_all('tr')
spisok = []
for i in all:
    if len(i.findAll('td')) == 0:
        continue
    try:
        id = i.findAll('td')[0].text
        name = i.findAll('td')[1].find('a').text
        zarazheniy = i.findAll('td')[2].text
        smertei = i.findAll('td')[3].text
        vixdorovleniy_total = i.findAll('td')[4].text
        zarazeno_na_now = i.findAll('td')[5].text
    except Exception:
        pass
    spisok.append(
        {"ID": id, "Регион": name, "Заражений": zarazheniy, "Смертей": smertei, "Выздоровлений": vixdorovleniy_total,
         "Заражений на настоящий моент": zarazeno_na_now})

con = sqlite3.connect('/home/alex/VSCode/Flask/flask_map_covid/country.db')
cursor = con.cursor()
cursor.execute("""DELETE from country""")
for i in spisok[:86]:
    index = i['Заражений'].find("(")
    value = (i['Заражений'][:int(index)].strip())
    cursor.execute("""insert into country(number,name,zarazeniy,smertei,vizdorovleniy,total_zaraz,value)
                   VALUES(?,?,?,?,?,?,?)""", (
        i['ID'], i['Регион'], i['Заражений'], i['Смертей'], i['Выздоровлений'], i['Заражений на настоящий моент'],
        value))
cursor.execute("""update country
                set id = (select id from city where country.name=city.name)""")
con.commit()
# con = sqlite3.connect('country.db')
# cursor = con.cursor()
# cursor.execute("""CREATE TABLE country
#                     (number integer,name text,zarazeniy text,smertei text, vizdorovleniy text, total_zaraz text)""")
