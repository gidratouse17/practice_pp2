from connect import connect_to_db

conn = connect_to_db()
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(50)
    )
""")
conn.commit()

# Create functions and procedures from .sql files
for sql_file in ['functions.sql', 'procedures.sql']:
    with open(sql_file, 'r', encoding='utf-8') as f:
        cursor.execute(f.read())
conn.commit()
print("Functions and procedures created")


def search(pattern):
    cursor.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cursor.fetchall()
    print(f"\n--- Search results for '{pattern}' ---")
    for r in rows:
        print(f"ID:{r[0]} | {r[1]} | {r[2]}")

def upsert(name, phone):
    cursor.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f" {name} added/updated")

def insert_many(names, phones):
    cursor.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
    conn.commit()
    print(" Bulk insert completed")

def get_page(page_num, page_size=3):
    cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_num, page_size))
    rows = cursor.fetchall()
    print(f"\n--- Page {page_num} ---")
    for r in rows:
        print(f"ID:{r[0]} | {r[1]} | {r[2]}")

def delete(name=None, phone=None):
    cursor.execute("CALL delete_contact(%s, %s)", (name, phone))
    conn.commit()
    print(" Contact deleted")


while True:
    print("\n========= PhoneBook (Practice 8) =========")
    print("1 - Search contact")
    print("2 - Add/update contact (upsert)")
    print("3 - Bulk insert")
    print("4 - View by page")
    print("5 - Delete contact")
    print("0 - Exit")
    choice = input("Choice: ")

    if choice == "1":
        p = input("Enter name or phone: ")
        search(p)
    elif choice == "2":
        n = input("Name: ")
        ph = input("Phone: ")
        upsert(n, ph)
    elif choice == "3":
        count = int(input("How many contacts to add? "))
        names = []
        phones = []
        for i in range(count):
            names.append(input(f"Name {i+1}: "))
            phones.append(input(f"Phone {i+1}: "))
        insert_many(names, phones)
    elif choice == "4":
        pg = int(input("Page number: "))
        get_page(pg)
    elif choice == "5":
        print("Delete by: 1 - name, 2 - phone")
        c = input("Choice: ")
        if c == "1":
            delete(name=input("Name: "))
        elif c == "2":
            delete(phone=input("Phone: "))
    elif choice == "0":
        break

cursor.close()
conn.close()