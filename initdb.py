import sqlite3 , time

conn = sqlite3.connect('mydb')
print("Opened database successfully")

valid_domains = ['ethermon.io','opensea.io','metamask.io','decentraland.org','polygonscan','etherscan','ethermon.zendesk']

for i in valid_domains :
    id = time.time_ns()
    print(id,i)
    conn.execute('INSERT INTO valid VALUES(?,?)',(id,i));


conn.commit()
print("mydb init successful")
conn.close()