import mysql.connector

mydb = mysql.connector.connect(
  # host="DESKTOP-F9CSS1C",
  # host="3306",
  user="root",
  password="Zj5$q26]}~R6",
  database="mydatabase"
)

# print(mydb)
# print('end')

mycursor = mydb.cursor()

# # DB created
# mycursor.execute("CREATE DATABASE mydatabase")
# mycursor.execute("SHOW DATABASES")
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)

# # Table created
# mycursor.execute("CREATE TABLE groceries (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER );")

this = [8,"test value"]

mycursor.execute("""INSERT INTO groceries VALUES (2, "Peanut Butter", 1);""")
mycursor.execute("""INSERT INTO groceries(id) VALUES (7);""")
mycursor.execute("""INSERT INTO groceries(id,name) VALUES (8,"test value");""")

mycursor.execute("SELECT * FROM groceries;")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

# This saves the changes thare are made in the script run
mydb.commit()