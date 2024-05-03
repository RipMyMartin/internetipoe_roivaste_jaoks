import sqlite3
import tkinter as tk
from tkinter import ttk

def create_database():
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()

    # Loo tabel Kategooriad
    c.execute('''CREATE TABLE Kategooriad
                 (kategooria_id INTEGER PRIMARY KEY,
                  kategooria_nimi TEXT NOT NULL)''')

    # Loo tabel Brändid
    c.execute('''CREATE TABLE Brändid
                 (brändi_id INTEGER PRIMARY KEY,
                  brändi_nimi TEXT NOT NULL)''')

    # Loo tabel Tooted
    c.execute('''CREATE TABLE Tooted
                 (toote_id INTEGER PRIMARY KEY,
                  toote_nimi TEXT NOT NULL,
                  hind REAL NOT NULL,
                  kategooria_id INTEGER NOT NULL,
                  brändi_id INTEGER NOT NULL,
                  FOREIGN KEY (kategooria_id) REFERENCES Kategooriad(kategooria_id),
                  FOREIGN KEY (brändi_id) REFERENCES Brändid(brändi_id))''')

    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()

    # Lisa kategooriad
    c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", ("Elektroonika",))
    c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", ("Rõivad",))
    c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", ("Mööbel",))

    # Lisa brändid
    c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", ("Apple",))
    c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", ("Nike",))
    c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", ("IKEA",))

    # Lisa tooted
    c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)", ("iPhone 12", 799.99, 1, 1))
    c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)", ("Nike Air Force 1", 99.99, 2, 2))
    c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)", ("IKEA Kallax riiulisüsteem", 79.99, 3, 3))

    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()

    # Kõik tooted koos kategooria ja brändi infoga
    c.execute('''SELECT 
                     Tooted.toote_nimi, 
                     Tooted.hind, 
                     Kategooriad.kategooria_nimi, 
                     Brändid.brändi_nimi
                 FROM Tooted
                 JOIN Kategooriad ON Tooted.kategooria_id = Kategooriad.kategooria_id
                 JOIN Brändid ON Tooted.brändi_id = Brändid.brändi_id''')
    products = c.fetchall()
    for product in products:
        print(f"Toote nimi: {product[0]}, Hind: {product[1]}, Kategooria: {product[2]}, Bränd: {product[3]}")

    # Tooted konkreetses kategoorias
    c.execute("SELECT Tooted.toote_nimi, Tooted.hind FROM Tooted WHERE Tooted.kategooria_id = ?", (1,))
    products = c.fetchall()
    print("\nTooted kategoorias 'Elektroonika':")
    for product in products:
        print(f"Toote nimi: {product[0]}, Hind: {product[1]}")

    # Tooted konkreetse brändi all
    c.execute("SELECT Tooted.toote_nimi, Tooted.hind FROM Tooted WHERE Tooted.brändi_id = ?", (2,))
    products = c.fetchall()
    print("\nTooted brändi 'Nike' all:")
    for product in products:
        print(f"Toote nimi: {product[0]}, Hind: {product[1]}")

    conn.close()

def add_new_product(toote_nimi, hind, kategooria_id, brändi_id):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)", (toote_nimi, hind, kategooria_id, brändi_id))
    conn.commit()
    conn.close()
    print(f"Uus toode '{toote_nimi}' on lisatud andmebaasi.")

def add_new_category(kategooria_nimi):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", (kategooria_nimi,))
    conn.commit()
    conn.close()
    print(f"Uus kategooria '{kategooria_nimi}' on lisatud andmebaasi.")

def add_new_brand(brändi_nimi):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", (brändi_nimi,))
    conn.commit()
    conn.close()
    print(f"Uus bränd '{brändi_nimi}' on lisatud andmebaasi.")

def update_product(toote_id, toote_nimi, hind, kategooria_id, brändi_id):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("UPDATE Tooted SET toote_nimi = ?, hind = ?, kategooria_id = ?, brändi_id = ? WHERE toote_id = ?", (toote_nimi, hind, kategooria_id, brändi_id, toote_id))
    conn.commit()
    conn.close()
    print(f"Toote '{toote_nimi}' informatsioon on uuendatud.")

def update_category(kategooria_id, kategooria_nimi):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("UPDATE Kategooriad SET kategooria_nimi = ? WHERE kategooria_id = ?", (kategooria_nimi, kategooria_id))
    conn.commit()
    conn.close()
    print(f"Kategooria '{kategooria_nimi}' informatsioon on uuendatud.")

def update_brand(brändi_id, brändi_nimi):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("UPDATE Brändid SET brändi_nimi = ? WHERE brändi_id = ?", (brändi_nimi, brändi_id))
    conn.commit()
    conn.close()
    print(f"Brändi '{brändi_nimi}' informatsioon on uuendatud.")

def delete_products_by_category(kategooria_id):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM Tooted WHERE kategooria_id = ?", (kategooria_id,))
    conn.commit()
    conn.close()
    print(f"Kõik tooted kategooriast {kategooria_id} on kustutatud.")

def delete_products_by_brand(brändi_id):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM Tooted WHERE brändi_id = ?", (brändi_id,))
    conn.commit()
    conn.close()
    print(f"Kõik tooted brändist {brändi_id} on kustutatud.")

def drop_and_recreate_table(table_name):
    conn = sqlite3.connect('products_database.db')
    c = conn.cursor()

    # Kustuta tabel
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Taasta tabel
    if table_name == "Tooted":
        c.execute('''CREATE TABLE Tooted
                     (toote_id INTEGER PRIMARY KEY,
                      toote_nimi TEXT NOT NULL,
                      hind REAL NOT NULL,
                      kategooria_id INTEGER NOT NULL,
                      brändi_id INTEGER NOT NULL,
                      FOREIGN KEY (kategooria_id) REFERENCES Kategooriad(kategooria_id),
                      FOREIGN KEY (brändi_id) REFERENCES Brändid(brändi_id))''')
    elif table_name == "Kategooriad":
        c.execute('''CREATE TABLE Kategooriad
                     (kategooria_id INTEGER PRIMARY KEY,
                      kategooria_nimi TEXT NOT NULL)''')
    elif table_name == "Brändid":
        c.execute('''CREATE TABLE Brändid
                     (brändi_id INTEGER PRIMARY KEY,
                      brändi_nimi TEXT NOT NULL)''')

    conn.commit()
    conn.close()
    print(f"Tabel '{table_name}' on kustutatud ja taastatud.")

def create_gui():
    root = tk.Tk()
    root.title("Toodete haldamine")

    # Tabelid
    tree_products = ttk.Treeview(root)
    tree_products.pack(pady=20)

    tree_categories = ttk.Treeview(root)
    tree_categories.pack(pady=20)

    tree_brands = ttk.Treeview(root)
    tree_brands.pack(pady=20)

    # Sisestusväljade loomine
    product_name_label = tk.Label(root, text="Toote nimi:")
    product_name_label.pack(pady=5)
    product_name_entry = tk.Entry(root)
    product_name_entry.pack(pady=5)

    product_price_label = tk.Label(root, text="Toote hind:")
    product_price_label.pack(pady=5)
    product_price_entry = tk.Entry(root)
    product_price_entry.pack(pady=5)

    product_category_label = tk.Label(root, text="Kategooria ID:")
    product_category_label.pack(pady=5)
    product_category_entry = tk.Entry(root)
    product_category_entry.pack(pady=5)

    product_brand_label = tk.Label(root, text="Brändi ID:")
    product_brand_label.pack(pady=5)
    product_brand_entry = tk.Entry(root)
    product_brand_entry.pack(pady=5)

    # Nuppude loomine
    add_product_button = tk.Button(root, text="Lisa uus toode", command=lambda: add_new_product(
        product_name_entry.get(),
        float(product_price_entry.get()),
        int(product_category_entry.get()),
        int(product_brand_entry.get())
    ))
    add_product_button.pack(pady=10)

    add_category_button = tk.Button(root, text="Lisa uus kategooria", command=lambda: add_new_category(
        category_name_entry.get()
    ))
    add_category_button.pack(pady=10)

    add_brand_button = tk.Button(root, text="Lisa uus bränd", command=lambda: add_new_brand(
        brand_name_entry.get()
    ))
    add_brand_button.pack(pady=10)

    root.mainloop()

# Käivita programm
create_database()
insert_data()
get_products()
create_gui()