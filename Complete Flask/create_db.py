import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "admin",
)

my_curser = mydb.curser()

my_curser.execute("CREATE DATABASE users")

my_curser.execute("SHOW DATABASES")
for db in my_curser:
    print(db)