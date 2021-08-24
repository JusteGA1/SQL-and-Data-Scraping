import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

connection = psycopg2.connect(
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


def create_db_structure() -> None:
    """
    Creates database structure: tables and their relations.
    NOTE: deletes tables if exist and creates new empty tables.
    """
    with connection.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS items;')
        cur.execute('DROP TABLE IF EXISTS categories;')

        cur.execute('''
            CREATE TABLE categories (
                id serial PRIMARY KEY,
                categoryName varchar(255)
            );
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id serial PRIMARY KEY,
                categoryId int,
                title varchar(1000),
                price decimal(7, 2), 
                itemURL varchar(1000),
                imgURL varchar(1000)
            );
        ''')

        cur.execute('''
            ALTER TABLE items ADD FOREIGN KEY (categoryId)
            REFERENCES categories(id);
        ''')
        connection.commit()


def insert_values_to_db() -> None:
    """Inserts default categories into the database."""
    with connection.cursor() as cur:
        cur.execute('''
           INSERT INTO categories(categoryName) VALUES
               ('earrings'),
               ('necklaces'),
               ('bracelets')
           ''')
        connection.commit()


def get_categories() -> list:
    """Return categories from the database."""
    with connection.cursor() as cur:
        cur.execute('SELECT * FROM categories')
        return cur.fetchall()


def insert_item(item: tuple) -> None:
    """Inserts given item into the database."""
    with connection.cursor() as cur:
        query = '''
        INSERT INTO items (categoryId, title, price, itemURL, imgURL) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        cur.execute(query, item)
        connection.commit()


def count_items() -> tuple:
    """
    Heroku database row count is inaccurate.
    Function will return the actual row count.
    """
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM items')
        return cur.fetchone()
# print(count_items())


def get_items_from_database() -> list:
    """
    Join categories and items tables from the database on category id.
    :return: items with category name
    """
    with connection.cursor() as cur:
        cur.execute('''
        SELECT 
            categories.categoryName,
            items.title,
            items.price,
            items.itemURL,
            items.imgURL
        FROM items
        LEFT JOIN categories
        ON items.categoryId=categories.id
        ''')
        return cur.fetchall()


if __name__ == "__main__":
    create_db_structure()
    insert_values_to_db()
