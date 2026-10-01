
#import getconnection
from database import get_connection
conn=get_connection()

#check connection
if conn.is_connected():
    print("Mysql connected success fully !!")


#set cursor to use sql from here
cursor = conn.cursor()

cursor.execute("SELECT * FROM users;")

# to display result
for row in cursor.fetchall():
    print(row)

# 4. Close connection
cursor.close()
conn.close()