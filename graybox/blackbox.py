import requests
import bs4
import sqlite3
import math

conn = sqlite3.connect('values.db')
conn.execute('create table if not exists value (inp text not null, outp text);')

BASE = 'https://blackbox.school-slon.ru/'

def query(v):
    resp = requests.get(BASE, params={'n': int(v)}).text
    soup = bs4.BeautifulSoup(resp, 'html.parser')
    try:
        return int(soup.find('div', attrs={'class': 'part'}).text)
    except:
        return None

def get(v):
    v = int(v)
    cursor = conn.cursor()
    cursor.execute('select outp from value where inp=?', (str(v), ))
    res = cursor.fetchall()
    if res:
        return int(res[0][0]) if res[0][0] is not None else None
    res = query(v)
    conn.execute('insert into value values (?, ?)', (str(v), str(res) if res else None))
    conn.commit()
    return res

if False:  # populate database file 
    for v in range(-20, 20):
        print(v, get(v))

# explore plot, find that it is a parabola. Need only three variables to define it.
# R = Ax^2 + Bx + C
c = get(0)
b = ((get(1)-get(0)) + (get(0)-get(-1))) // 2

a = 0
def calc(v):
    return a*v*v + b*v + c
while get(-10000) != calc(-10000):
    a += 1

print(c, b, a)

if True:  # find limits
    # upper limit
    step = 1e15
    cursor = 0
    while step != 1:
        print(cursor)
        cursor += step
        cursor = int(cursor)
        if get(cursor) is None:
            cursor -= step
            step = math.ceil(step/2)
            print(cursor, step)
    cursor -= 10
    while get(cursor) is not None:
        cursor += 1
    limit_upper = cursor 
    
    # lower limit
    step = 1e15
    cursor = 0
    while step != 1:
        print(cursor)
        cursor -= step
        cursor = int(cursor)
        if get(cursor) is None:
            cursor += step
            step = math.ceil(step/2)
            print(cursor, step)
    cursor += 10
    while get(cursor) is not None:
        cursor -= 1
    limit_lower = cursor

print()
print()

print('def blackbox(value):')
print(' if not isinstance(value, int): return "нет ответа"')
print(' if value >=', limit_upper, 'or value <=', str(limit_lower)+': return "слишком большое число"')
print(' return', a, '* value * value +', b, '* value +', c)

