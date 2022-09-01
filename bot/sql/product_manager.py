

class Product():

    def __init__(self, cursor):
        self.cursor = cursor

    
    def _execute_query(self, query):
        result = self.cursor.execute(query)
        # Выполняется команда в базу
        return 

    def create_product_table(self):
        query = """Create table if not exists product (id integer primary key auto_increment, 
        name varchar(255) not null, 
        description text, 
        price decimal(10,2) not null,
        is_available Boolean not null default True,
        category_id integer not null,
        foreign key(category_id) references category(id)
        );
        """
        res = self._execute_query(query)
        return res


    
    def add_product(self, data):
        
        query = f"""
        insert into product(name, description, price,category_id) values('{data.get("name")}','{data.get("description")}', 
        {data.get('price')},{data.get('category_id')}); """

        self._execute_query(query)
    

    def get_all_products(self):
        query = """
        Select * from product;
        """
        self.cursor.executes(query)
        return self.cursor.fetchall()

    def get_products_by_category(self, category_id):
        query = f"""
        Select * from product where category_id = {category_id};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_product_by_id(self, id):
        query = f"""
        Select * from product where id = {id};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
