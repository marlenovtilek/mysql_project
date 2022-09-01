from sqlite3 import Cursor
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "tileksql",
    db = "my_shop",
    autocommit = True
)

cursor = db.cursor()

def create_category_table(cursor):
    query =  f"""Create table category(
        id integer primary key auto_increment,
        name varchar(50) not null);
        """
    cursor.execute(query)

# while True:
#     name = input("Введите название новой категории: ")
#     if name == "exit":
#         break
#     query = f"insert into category(name) values('{name}')"
#     cursor.execute(query)

def delete_category_by_id(id, cursor):
    query = f"delete from category where id = {id};"
    cursor.execute(query)

delete_category_by_id(7, cursor)

query = "Select * from category;"
cursor.execute(query)
categories = cursor.fetchall()
for category in categories:
    id = category[0]
    name = category[1]
    print(f"ID:{id} - NAME:{name}")

