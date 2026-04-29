import psycopg2
import csv
from connect import get_connection



# 1. Create table

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table created (or already exists)")


# 2. Insert from CSV

def insert_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO phonebook (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING;
            """, (row["first_name"], row["phone"]))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data loaded from CSV")


# 3. Insert from console
def insert_from_console():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO phonebook (first_name, phone)
            VALUES (%s, %s);
        """, (name, phone))
        conn.commit()
        print("✅ Contact added")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("❌ This phone number already exists")
    finally:
        cur.close()
        conn.close()



# 4. Update contact
def update_contact():
    print("What to update?")
    print("1 - Name by phone")
    print("2 - Phone by name")
    choice = input("Choice: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        phone = input("Enter contact phone: ").strip()
        new_name = input("New name: ").strip()
        cur.execute("""
            UPDATE phonebook SET first_name = %s WHERE phone = %s;
        """, (new_name, phone))
    elif choice == "2":
        name = input("Enter contact name: ").strip()
        new_phone = input("New phone: ").strip()
        cur.execute("""
            UPDATE phonebook SET phone = %s WHERE first_name = %s;
        """, (new_phone, name))
    else:
        print("❌ Invalid choice")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("✅ Contact updated")
    cur.close()
    conn.close()


# ──────────────────────────────────────────
# 5. Search / filter contacts
# ──────────────────────────────────────────
def search_contacts():
    print("Search by:")
    print("1 - Name")
    print("2 - Phone prefix")
    print("3 - All contacts")
    choice = input("Choice: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name (or part): ").strip()
        cur.execute("""
            SELECT * FROM phonebook WHERE first_name ILIKE %s;
        """, (f"%{name}%",))
    elif choice == "2":
        prefix = input("Enter phone prefix: ").strip()
        cur.execute("""
            SELECT * FROM phonebook WHERE phone LIKE %s;
        """, (f"{prefix}%",))
    elif choice == "3":
        cur.execute("SELECT * FROM phonebook ORDER BY first_name;")
    else:
        print("❌ Invalid choice")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()
    if rows:
        print(f"\n{'ID':<5} {'Name':<20} {'Phone'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
    else:
        print("No contacts found")

    cur.close()
    conn.close()


# ──────────────────────────────────────────
# 6. Delete contact
# ──────────────────────────────────────────
def delete_contact():
    print("Delete by:")
    print("1 - Name")
    print("2 - Phone")
    choice = input("Choice: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ").strip()
        cur.execute("DELETE FROM phonebook WHERE first_name = %s;", (name,))
    elif choice == "2":
        phone = input("Enter phone: ").strip()
        cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
    else:
        print("❌ Invalid choice")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("✅ Contact deleted")
    cur.close()
    conn.close()


# ──────────────────────────────────────────
# Main menu
# ──────────────────────────────────────────
def main():
    create_table()
    while True:
        print("\n========= PhoneBook =========")
        print("1 - Load from CSV")
        print("2 - Add manually")
        print("3 - Update contact")
        print("4 - Search contacts")
        print("5 - Delete contact")
        print("0 - Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()