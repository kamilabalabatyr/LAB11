import psycopg2
import json
from psycopg2 import Error

class PhoneBook:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="kamilabalabatyr",
            password="Kamila97",
            host="localhost",
            port="5432",
            database="postgres"
        )
    
    def search_by_pattern(self, pattern):
        try:
            cursor = self.connection.cursor()
            cursor.callproc('search_by_pattern', (pattern,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print("Error searching by pattern:", e)
            return []
    
    def upsert_user(self, first_name, last_name, phone):
        try:
            cursor = self.connection.cursor()
            cursor.callproc('upsert_user', (first_name, last_name, phone))
            self.connection.commit()
            return True
        except Error as e:
            print("Error upserting user:", e)
            self.connection.rollback()
            return False
    
    def insert_many_users(self, users_list):
        try:
            cursor = self.connection.cursor()
            
            users_json = json.dumps(users_list)
           
            cursor.callproc('insert_many_users', (users_json,))
            self.connection.commit()
            
            invalid_data = cursor.fetchone()[0]
            return json.loads(invalid_data)
        except Error as e:
            print("Error inserting many users:", e)
            self.connection.rollback()
            return users_list 
    
    def get_contacts_paginated(self, limit, offset):
        try:
            cursor = self.connection.cursor()
            cursor.callproc('get_contacts_paginated', (limit, offset))
            results = cursor.fetchall()
            
            return {
                'contacts': [{
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'phone': row[3]
                } for row in results],
                'total': results[0][4] if results else 0
            }
        except Error as e:
            print("Error getting paginated contacts:", e)
            return {'contacts': [], 'total': 0}
    
    def delete_contact(self, username=None, phone=None):
        try:
            cursor = self.connection.cursor()
            cursor.callproc('delete_contact', (username, phone))
            self.connection.commit()
            return cursor.rowcount 
        except Error as e:
            print("Error deleting contact:", e)
            self.connection.rollback()
            return 0
    
    def close(self):
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    pb = PhoneBook()
    
    print("Search results for 'Kamila':")
    print(pb.search_by_pattern("Kamila"))
    
    pb.upsert_user("Kamila", "Balabatyr", "87021151445")
    
    users = [
        {"first_name": "Nursultan", "Nazarbaev": "Abishuly", "+77777777777": "777-7777"},
        {"first_name": "Kasym-Zhomart", "Toqaev": "Kemeluly", "+77077777777": "666-6666"},
        {"first_name": "Sponge", "Bob": "555-5678"} 
    ]
    invalid = pb.insert_many_users(users)
    print("Invalid records:", invalid)
    
    page1 = pb.get_contacts_paginated(5, 0)
    print("First page:", page1['contacts'])
    print("Total contacts:", page1['total'])
    
    deleted_count = pb.delete_contact(username="Kamila")
    print(f"Deleted {deleted_count} contacts")
    
    pb.close()