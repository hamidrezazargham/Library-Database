import psycopg2 as psg
from datetime import datetime, timedelta
import random
import data


conn = psg.connect(host=data.DB_HOST, dbname=data.DB_NAME, user=data.DB_USER, password=data.DB_PASSWORD, port=data.DB_PORT)
cursor = conn.cursor()


books = {
    'id': [],
    'title': []
}
cursor.execute("SELECT Book_Id, Title FROM Books;")
fetched = cursor.fetchall()
for i in range(len(fetched)):
    books['id'].append(fetched[i][0])
    books['title'].append(fetched[i][1])


members = {
    'id': [],
    'name': []
}
cursor.execute("SELECT Member_id, First_name || ' ' || Last_name AS Full_Name FROM Members;")
fetched = cursor.fetchall()
for i in range(len(fetched)):
    members['id'].append(fetched[i][0])
    members['name'].append(fetched[i][1])
    
date_range = {
    'year': [2023],
    'month': list(range(1, 13)),
    'day': list(range(1, 31))
}
n = 100
for i in range(n):
    print(i)
    book = random.choice(books['id'])
    member = random.choice(members['id'])
    borrow_date = datetime(year=random.choice(date_range['year']), month=random.choice(date_range['month']), day=random.choice(date_range['day']))
    return_date = borrow_date + timedelta(days=random.randint(1, 20))
    try:
        cursor.execute("CALL Borrow({}, {}, '{}');".format(book, member, borrow_date.strftime("%Y-%m-%d")))
        cursor.execute("CALL Return_book({}, {}, '{}');".format(book, member, return_date.strftime("%Y-%m-%d")))
        conn.commit()
    except Exception as e:
        print("An exception occurred:", e)
        cursor.close()
        conn.close()
        
        conn = psg.connect(host=data.DB_HOST, dbname=data.DB_NAME, user=data.DB_USER, password=data.DB_PASSWORD, port=data.DB_PORT)
        cursor = conn.cursor()
conn.commit()
cursor.close()
conn.close()