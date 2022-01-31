import sqlite3

def test():
    return 'function imported successfully'

def get_pending(cursor):
    cursor.execute('''select * from pending''')
    return cursor.fetchall()

def approve_url(cursor,conn,id):
    cursor.execute('''select * from pending where id={}'''.format(id))
    row = cursor.fetchall()
    for i in row:
        cursor.execute('''insert into valid values(?,?)''',(i[0],i[1]))
    cursor.execute('''delete from pending where id={}'''.format(id))
    conn.commit()
    return row

def insert_pending(cursor,conn,id,url):
    statement = '''insert into pending values(?,?)'''.strip()
    cursor.execute(statement,(id,url))
    conn.commit()
    return id

def delete_pending(cursor,conn,id):
    cursor.execute('''delete from pending where id={}'''.format(id))
    conn.commit()
    return id

def get_valid(cursor):
    cursor.execute('''select url from valid''')
    return cursor.fetchall()