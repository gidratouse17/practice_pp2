import json
import csv
from connect import connect_to_db

conn = connect_to_db()
cur = conn.cursor()

# Run schema and procedures
for f in ['schema.sql', 'procedures.sql']:
    with open(f, encoding='utf-8') as file:
        cur.execute(file.read())
conn.commit()
print("Schema and procedures ready")


def import_csv(filename='contacts.csv'):
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # get or create group
            cur.execute("SELECT id FROM groups WHERE name=%s", (row['group'],))
            g = cur.fetchone()
            if not g:
                cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (row['group'],))
                g = cur.fetchone()
            group_id = g[0]

            # insert contact if not exists
            cur.execute("SELECT id FROM contacts WHERE first_name=%s", (row['first_name'],))
            c = cur.fetchone()
            if not c:
                cur.execute(
                    "INSERT INTO contacts(first_name, email, birthday, group_id) VALUES(%s,%s,%s,%s) RETURNING id",
                    (row['first_name'], row['email'], row['birthday'], group_id)
                )
                c = cur.fetchone()
            contact_id = c[0]

            # insert phone
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                (contact_id, row['phone'], row['phone_type'])
            )
    conn.commit()
    print("CSV imported")


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    bday = input("Birthday (YYYY-MM-DD or leave empty): ").strip() or None
    group = input("Group (Family/Work/Friend/Other): ")

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()
    if not g:
        cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
        g = cur.fetchone()
    group_id = g[0]

    cur.execute(
        "INSERT INTO contacts(first_name, email, birthday, group_id) VALUES(%s,%s,%s,%s) RETURNING id",
        (name, email, bday, group_id)
    )
    contact_id = cur.fetchone()[0]

    while True:
        phone = input("Phone (or leave empty to stop): ").strip()
        if not phone:
            break
        ptype = input("Type (home/work/mobile): ").strip()
        cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)", (contact_id, phone, ptype))

    conn.commit()
    print(f"Contact {name} added!")


def search():
    q = input("Search (name / email / phone): ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()
    if not rows:
        print("Nothing found")
        return
    for r in rows:
        print(f"ID:{r[0]} | {r[1]} | email:{r[2]} | bday:{r[3]} | group:{r[4]}")
        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (r[0],))
        phones = cur.fetchall()
        for p in phones:
            print(f"    {p[0]} ({p[1]})")


def filter_by_group():
    group = input("Group name: ")
    sort = input("Sort by (name/birthday/id): ").strip() or "first_name"
    if sort == "name":
        sort = "first_name"
    if sort not in ("first_name", "birthday", "id"):
        sort = "first_name"
    cur.execute(f"""
        SELECT c.id, c.first_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.{sort}
    """, (group,))
    rows = cur.fetchall()
    if not rows:
        print("No contacts in this group")
        return
    for r in rows:
        print(f"ID:{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")


def paginated_view():
    page_size = 3
    page = 1
    while True:
        cur.execute("""
            SELECT c.id, c.first_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (page_size, (page-1)*page_size))
        rows = cur.fetchall()
        if not rows:
            print("No more contacts")
            page = max(1, page-1)
            continue
        print(f"\n--- Page {page} ---")
        for r in rows:
            print(f"ID:{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
        cmd = input("next / prev / quit: ").strip()
        if cmd == "next":
            page += 1
        elif cmd == "prev":
            page = max(1, page-1)
        elif cmd == "quit":
            break


def add_phone_to_contact():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    print("Phone added!")


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    print(f"{name} moved to {group}")


def export_json():
    cur.execute("""
        SELECT c.id, c.first_name, c.email, c.birthday::text, g.name
        FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
    """)
    contacts = cur.fetchall()
    result = []
    for c in contacts:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (c[0],))
        phones = cur.fetchall()
        result.append({
            "id": c[0], "name": c[1], "email": c[2],
            "birthday": c[3], "group": c[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })
    with open("contacts_export.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Exported to contacts_export.json")


def import_json():
    filename = input("JSON filename: ").strip()
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    for c in data:
        cur.execute("SELECT id FROM contacts WHERE first_name=%s", (c["name"],))
        existing = cur.fetchone()
        if existing:
            ans = input(f"{c['name']} already exists. Skip or overwrite? (s/o): ")
            if ans.lower() != "o":
                continue
            cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE first_name=%s",
                        (c.get("email"), c.get("birthday"), c["name"]))
        else:
            group_id = None
            if c.get("group"):
                cur.execute("SELECT id FROM groups WHERE name=%s", (c["group"],))
                g = cur.fetchone()
                if not g:
                    cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (c["group"],))
                    g = cur.fetchone()
                group_id = g[0]
            cur.execute(
                "INSERT INTO contacts(first_name, email, birthday, group_id) VALUES(%s,%s,%s,%s) RETURNING id",
                (c.get("name"), c.get("email"), c.get("birthday"), group_id)
            )
            contact_id = cur.fetchone()[0]
            for p in c.get("phones", []):
                cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                            (contact_id, p["phone"], p["type"]))
    conn.commit()
    print("JSON imported")


while True:
    print("\n===== PhoneBook TSIS1 =====")
    print("1  - Import from CSV")
    print("2  - Add contact manually")
    print("3  - Search (name/email/phone)")
    print("4  - Filter by group")
    print("5  - Browse pages (next/prev)")
    print("6  - Add phone to contact")
    print("7  - Move contact to group")
    print("8  - Export to JSON")
    print("9  - Import from JSON")
    print("0  - Exit")

    choice = input("Choice: ").strip()

    if choice == "1":
        import_csv()
    elif choice == "2":
        add_contact()
    elif choice == "3":
        search()
    elif choice == "4":
        filter_by_group()
    elif choice == "5":
        paginated_view()
    elif choice == "6":
        add_phone_to_contact()
    elif choice == "7":
        move_to_group()
    elif choice == "8":
        export_json()
    elif choice == "9":
        import_json()
    elif choice == "0":
        print("Bye!")
        break
    else:
        print("Wrong input")

cur.close()
conn.close()