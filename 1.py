import psycopg2

# 1
def search_phonebook(pattern):
    conn = psycopg2.connect("dbname=postgres user=kamilabalabatyr password=your_password")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, first_name, last_name, phone_number
        FROM PhoneBook
        WHERE first_name LIKE %s
           OR last_name LIKE %s
           OR phone_number LIKE %s
    """, (f'%{pattern}%', f'%{pattern}%', f'%{pattern}%'))

    records = cursor.fetchall()
    if records:
        for record in records:
            print(record)
    else:
        print("No matching records found.")

    cursor.close()
    conn.close()

# Пример
search_phonebook("Kamila")

# 2
def insert_update_user(first_name, last_name, phone_number):
    conn = psycopg2.connect("dbname=postgres user=kamilabalabatyr password=your_password")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM PhoneBook WHERE phone_number = %s
    """, (phone_number,))
    
    if cursor.fetchone():
        cursor.execute("""
            UPDATE PhoneBook
            SET first_name = %s, last_name = %s
            WHERE phone_number = %s
        """, (first_name, last_name, phone_number))
        print(f"User with phone {phone_number} updated.")
    else:
        cursor.execute("""
            INSERT INTO PhoneBook (first_name, last_name, phone_number)
            VALUES (%s, %s, %s)
        """, (first_name, last_name, phone_number))
        print(f"User {first_name} {last_name} added.")

    conn.commit()
    cursor.close()
    conn.close()

# Пример 
insert_update_user("Kamila", "Balabatyr", "87021151445")

# 3
def insert_many_users(user_data):
    conn = psycopg2.connect("dbname=postgres user=kamilabalabatyr password=your_password")
    cursor = conn.cursor()

    for user_record in user_data:
        user_info = user_record.split(',')
        
        if len(user_info) == 3:  
            first_name, last_name, phone_number = user_info
            if phone_number.isdigit() and len(phone_number) == 10:
                cursor.execute("""
                    INSERT INTO PhoneBook (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                """, (first_name, last_name, phone_number))
                print(f"User {first_name} {last_name} added.")
            else:
                print(f"Invalid phone number: {phone_number}")
        else:
            print(f"Invalid data format: {user_record}")

    conn.commit()
    cursor.close()
    conn.close()

# Пример 
user_data = ['Kamila,Balabatyr,87021151445', 'Mama,Papa,87787014509']
insert_many_users(user_data)

#4
def get_phonebook_paginated(limit, offset):
    conn = psycopg2.connect("dbname=postgres user=kamilabalabatyr password=your_password")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, first_name, last_name, phone_number
        FROM PhoneBook
        LIMIT %s OFFSET %s
    """, (limit, offset))

    records = cursor.fetchall()
    for record in records:
        print(record)

    cursor.close()
    conn.close()

# Пример 
get_phonebook_paginated(10, 0)

#5
def delete_phonebook_data(identifier):
    conn = psycopg2.connect("dbname=postgres user=kamilabalabatyr password=your_password")
    cursor = conn.cursor()

    if identifier.isdigit() and len(identifier) == 10:  
        cursor.execute("""
            DELETE FROM PhoneBook
            WHERE phone_number = %s
        """, (identifier,))
        print(f"Record with phone number {identifier} deleted.")
    else:  
        cursor.execute("""
            DELETE FROM PhoneBook
            WHERE first_name = %s OR last_name = %s
        """, (identifier, identifier))
        print(f"Record with name {identifier} deleted.")

    conn.commit()
    cursor.close()
    conn.close()

# Пример
delete_phonebook_data('87021151445')  
delete_phonebook_data('Kamila')  
