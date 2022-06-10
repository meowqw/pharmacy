
import settings
from mysql.connector import connect, Error
import sys

class DB:
    def __init__(self):
        self.connection = connect(host=settings.HOST,
                                  #   port=settings.PORT,
                                  user=settings.USER,
                                  password=settings.PASSWORD,
                                  database=settings.DB_NAME,
                                  charset='utf8')
        self.cursor = self.connection.cursor()

    def create_users_table(self):
        """USER TABLE"""
        create_users_table_query = """
            CREATE TABLE users(
            id INTEGER(255) PRIMARY KEY,
            login VARCHAR(300),
            username VARCHAR(300))"""

        self.cursor.execute(create_users_table_query)
        self.connection.commit()

    def create_goods_table(self):
        """GOODS TABLE"""
        create_goods_table_query = """
            CREATE TABLE goods(
            id VARCHAR(255) PRIMARY KEY,
            title VARCHAR(300),
            manufacturer VARCHAR(300),
            img VARCHAR(400),
            information TEXT,
            price FLOAT,
            leave_condition BOOLEAN)"""

        self.cursor.execute(create_goods_table_query)
        self.connection.commit()

    def create_pharmacy_table(self):
        """PHARMACY TABLE"""
        create_pharmacy_table_query = """
            CREATE TABLE pharmacy(
            id INT PRIMARY KEY,
            title VARCHAR(300),
            address VARCHAR(300),
            phone VARCHAR(300),
            schedule VARCHAR(300))"""

        self.cursor.execute(create_pharmacy_table_query)
        self.connection.commit()
    
    def create_user_table(self):
        """USER"""
        create_pharmacy_table_query = """
            CREATE TABLE user(
            id INT PRIMARY KEY,
            login VARCHAR(300),
            password VARCHAR(300))"""

        self.cursor.execute(create_pharmacy_table_query)
        self.connection.commit()

    def create_available_table(self):
        """AVAILABLE TABLE"""
        create_available_table_query = """
            CREATE TABLE available(
            id_pharmacy INT,
            id_good VARCHAR(255),
            available BOOLEAN,
            FOREIGN KEY(id_pharmacy) REFERENCES pharmacy(id),
            FOREIGN KEY(id_good) REFERENCES goods(id),
            PRIMARY KEY(id_pharmacy, id_good))"""

        self.cursor.execute(create_available_table_query)
        self.connection.commit()

    def create_reviews_table(self):
        """REVIEWS TABLE"""
        create_reviews_table_query = """
            CREATE TABLE reviews(
            id_user INT,
            id_good VARCHAR(255),
            text TEXT,
            rating INTEGER(20),
            FOREIGN KEY(id_user) REFERENCES users(id),
            FOREIGN KEY(id_good) REFERENCES goods(id),
            PRIMARY KEY(id_user, id_good))"""

        self.cursor.execute(create_reviews_table_query)
        self.connection.commit()

    def create_tables(self):
        """CREATE TABLES"""
        # self.create_users_table()
        # print("[DB]: users table created")
        # self.create_pharmacy_table()
        # print("[DB]: pharmacy table created")
        # self.create_goods_table()
        # print("[DB]: goods table created")
        # self.create_reviews_table()
        # print("[DB]: reviews table created")
        # self.create_available_table()
        print("[DB]: available table created")
        self.create_user_table()
        print("[DB]: user table created")


    def add_user(self, data):
        """ADD USER IN DB"""
        id_ = data['id']
        login = data['login']
        username = data['username']
        print(data)
        query = "INSERT INTO users (id, login, username) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (id_, login, username))
        self.connection.commit()

    def add_pharmacy(self, data):
        """ADD PHARMACY IN DB"""
        id_ = data['id']
        title = data['title']
        address = data['address']
        phone = data['phone']
        schedule = data['schedule']
        query = "INSERT INTO pharmacy (id, title, address, phone, schedule) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (id_, title, address, phone, schedule))
        self.connection.commit()
    
    def update_pharmacy(self, data):
        """UPDATE PHARMACY IN DB"""
        id_ = data['id']
        title = data['title']
        address = data['address']
        phone = data['phone']
        schedule = data['schedule']
        query = "UPDATE pharmacy SET title=%s, address=%s, phone=%s, schedule=%s WHERE id=%s"
        self.cursor.execute(query, (title, address, phone, schedule, id_))
        self.connection.commit()
    
    def get_all_pharmacy(self):
        """GET ALL PHARMACY"""
        query = "SELECT * FROM pharmacy"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def get_good_by_title(self, title):
        """GET GOOD BY TITLE"""
        query = f"SELECT * FROM goods WHERE title LIKE '%{title}%'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def get_good_by_id(self, id_):
        """GET GOOD BY TITLE"""
        query = f"SELECT * FROM goods WHERE id LIKE '%{id_}%'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def get_all_goods(self):
        """GET ALL GOODS FROM DB"""
        query = "SELECT * FROM goods"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_pharmacy_available_by_id(self, id_):
        """GET PHARMACY AVAILABLE BY ID"""
        query = 'SELECT * FROM pharmacy INNER JOIN available ON available.id_pharmacy = pharmacy.id WHERE available.available = 1 AND available.id_good = "%s"' % (id_)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def add_review(self, data):
        """ADD REVIEWS"""
        id_ = data['id_good']
        review_text = data['text']
        rating = data['rating']
        id_user = data['id_user']
        print(data)
        query = "INSERT INTO reviews (id_user, id_good, text, rating) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (id_user, id_, review_text, rating))
        self.connection.commit()
        self.connection.close()

    def get_reviews_by_id(self, id_good):
        """GET REVIEWS BY ID"""
        query = 'SELECT * FROM reviews WHERE id_good = "%s"' % (id_good)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def add_goods(self, data):
        """ADD PRODUCT IN DB"""
        id_ = data['id']
        title = data['title']
        manufacturer = data['manufacturer']
        img = data['img']
        information = data['information']
        price = data['price']
        leave_condition = data['leave_condition']
        query = "INSERT INTO goods (id, title, manufacturer, img, information, price, leave_condition) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (id_, title, manufacturer, img, information, price, leave_condition))
        self.connection.commit()
        self.connection.close()
    
    def update_goods(self, data):
        """UPDATE PRODUCT IN DB"""
        id_ = data['id']
        title = data['title']
        manufacturer = data['manufacturer']
        img = data['img']
        information = data['information']
        price = data['price']
        leave_condition = data['leave_condition']
        query = "UPDATE goods SET title=%s, manufacturer=%s, img=%s, information=%s, price=%s, leave_condition=%s WHERE id=%s"
        self.cursor.execute(query, (title, manufacturer, img, information, price, leave_condition, id_))
        self.connection.commit()
        self.connection.close()

    def add_available(self, data):
        """ADD AVAILABLE IN DB"""
        id_pharmacy = data['id_pharmacy']
        id_good = data['id_good']
        available = data['available']
        query = "INSERT INTO available (id_pharmacy, id_good, available) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (id_pharmacy, id_good, available))
        self.connection.commit()
        self.connection.close()
    
    def update_available(self, data):
        """UPDATE AVAILABLE IN DB"""
        id_pharmacy = data['id_pharmacy']
        id_good = data['id_good']
        available = data['available']
        query = "UPDATE available SET id_pharmacy=%s, id_good=%s, available=%s WHERE id_pharmacy=%s and id_good=%s"
        self.cursor.execute(query, (id_pharmacy, id_good, available, id_pharmacy, id_good))
        self.connection.commit()
        self.connection.close()

    def get_all_available(self):
        """GET ALL AVAILABLE"""
        query = "SELECT * FROM available"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_user(self, login):
        query = 'SELECT * FROM user WHERE login = "%s"' % (login)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def add_users(self, data):
        id_ = data['id']
        login = data['login']
        password = data['password']
        print(data)
        query = "INSERT INTO user (id, login, password) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (id_, login, password))
        self.connection.commit()
        self.connection.close()

    def delete_good(self, id_):
        query = "DELETE FROM goods WHERE id = '%s'" % (id_)
        self.cursor.execute(query)

        self.connection.commit()

        self.connection.close()
    
    def delete_available(self, id_):
        query = "DELETE FROM available WHERE id_good = '%s'" % (id_)
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()
    
    def delete_available_pharmacy(self, id_):
        query = "DELETE FROM available WHERE id_pharmacy = '%s'" % (id_)
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def delete_available_id(self, id_ph, id_good):
        query = "DELETE FROM available WHERE id_pharmacy = '%s' and id_good = '%s'" % (id_ph, id_good)
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()


    def delete_reviews(self, id_):
        query = "DELETE FROM reviews WHERE id_good = '%s'" % (id_)
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def delete_pharmacy(self, id_):
        query = "DELETE FROM pharmacy WHERE id = '%s'" % (id_)
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()



# DB().delete_good('sdfsf')
# print(DB().get_available_by_id('T000'))
# DB().create_tables()
# print(DB().get_reviews_by_id('T000'))
# DB().add_user({'id': 213123213, 'login': 'sadf', 'username': 'erewr'})
# DB().add_review({'id_good': 'sdfsf', 'id_user': 213123213, 'rating': 4, 'text': 'sdfsdf'})

# DB().add_users({'id': 1, 'login': 'admin', 'password': 'admin'})
