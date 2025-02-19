import sqlite3
from sqlite3 import Error

def create_connection():
    # Create a database Connection;
    conn = None
    try:
        conn = sqlite3.connect('cookbooks.db')
        print(f'Successfully connected to SQLite {sqlite3.version}')
        return conn
    except Error as e:
        print(f"Error has been found when creating a connection with the void: {e}")
        return None

def create_table(conn):
    # Creates a table structure of database

    try:
        sql_create_cookbook_table = """
        CREATE TABLE IF NOT EXISTS cookbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_published INTEGER,
            aesthetic_rating INTEGER,
            instagram_worthy BOOLEAN,
            cover_color TEXT
        );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_cookbook_table)
        print("Successfully created a database structure") 
    except Error as e:
        print(f"Error when creating table: {e}")


def insert_cookbooks(conn, cookbook):
    # add new cookbook to shelf
    sql = """Insert INTO cookbooks(title, author, year_published, aesthetic_rating, instagram_worthy, cover_color)
    VALUES(?,?,?,?,?,?)"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, cookbook)
        conn.commit()
        print(f"Successfully curated cookbook with id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding to collection: {e}")
        return []

def get_all_cookbooks(conn):
    # browse entire collection
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cookbooks")
        books = cursor.fetchall()
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]}")
            print(f"Aesthetic Rating: {'⭐' * book[4]}")
            print(f"Instagram Worthy: {'Yes' if book[5] else 'Not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
    except Error as e:
        print(f"Error found when retrieving collection: {e}")
        return []
    
def main():
    # Establish Connection
    conn = create_connection()

    if conn is not None:
        # Create table
        create_table(conn)

        # insert samples

        cookbooks = [
            ('Top Ten to Wow Guests: How to make 5-star food',
             'Gordon', 2020, 4, True, 'Firey Orange'),
            ('Grilling outside: 20 new ways to make a burger!',
             'Mcbrother', 1940, 5, True, 'Neon Yellow'),
            ('Making Pizza: 7 different ways to cook pizza',
             'Hut', 1958, 3, False, 'Roof Red'),
            ('Frying Chicken: how to make crisp and golden skin',
             'Sanders', '1990', 3, False, 'Greasy Gold'),
            ('Brewing Drinks: 99 new ways to brew coffee',
             'Bucks', '1975', 4, True, 'Forest Green')]

        print("\nCurating your cookbook collection...")
        for cookbook in cookbooks:
            insert_cookbooks(conn, cookbook)
        
        print("\nYour carefully curated cookbooks: ")
        get_all_cookbooks(conn)

        conn.close()
        print("\nDatabase Connection Closed")
    else:
        print("Error! The Connection cannot be found")

if __name__ == '__main__':
    main()