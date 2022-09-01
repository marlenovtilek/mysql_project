from secrets import choice
from sql.config import *
import mysql.connector
class Category():
    def __init__(self, cursor):
        self.cursor = cursor

    def create_table(self):
        query = """Create table IF NOT EXISTS category(
            id integer primary key auto_increment,
            name varchar(100) not null unique
            );    
        """
        result = self.cursor.execute(query)
        return result

    def add_new_category(self, name):
        # Добавляет новую категорию 
        query = f"""insert into category(name) values('{name}'); """
        result =  self.cursor.execute(query)
        return  result 

    def delete_category(self, id):
        query = f"""delete from category where id = {id};""" 
        result = self.cursor.execute(query)
        return result

    def update_category(self, id, new_value):
        query = f"""update category set name = '{new_value}' where id = {id};"""
        result = self.cursor.execute(query)
        return result

    def get_all_categories(self):
        query = f"""select * from category;"""
        result = self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_category_by_name(self, name):
        cursor = self.run_connect()
        query = f"""select * from category where name = '{name}';"""
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def search_movie(self, search_text):
        query = f"""
            Select * from movie where name like %{search_text}%;

        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def _get_all_id(self, id):
        query = """
            Select id from movies;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()




