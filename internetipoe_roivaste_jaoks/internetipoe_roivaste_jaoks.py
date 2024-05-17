import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def create_database(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tooted'")
    result = c.fetchone()
    if result is None:
        c.execute('''CREATE TABLE Tooted (
                        toote_id INTEGER PRIMARY KEY,
                        toote_nimi TEXT,
                        hind REAL,
                        kategooria_id INTEGER,
                        brändi_id INTEGER,
                        FOREIGN KEY (kategooria_id) REFERENCES Kategooriad(kategooria_id),
                        FOREIGN KEY (brändi_id) REFERENCES Brändid(brändi_id)
                    )''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS Kategooriad (
                        kategooria_id INTEGER PRIMARY KEY,
                        kategooria_nimi TEXT UNIQUE
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Brändid (
                        brändi_id INTEGER PRIMARY KEY,
                        brändi_nimi TEXT UNIQUE
                    )''')
        conn.commit()

def populate_tree(tree, conn):
    c = conn.cursor()
    tree.delete(*tree.get_children())
    c.execute('''SELECT Tooted.toote_id, Tooted.toote_nimi, Tooted.hind, Kategooriad.kategooria_nimi, Brändid.brändi_nimi 
                    FROM Tooted 
                    INNER JOIN Kategooriad ON Tooted.kategooria_id = Kategooriad.kategooria_id 
                    INNER JOIN Brändid ON Tooted.brändi_id = Brändid.brändi_id''')
    for row in c.fetchall():
        tree.insert("", "end", text=row[0], values=row[1:])

def add_new_category(conn, category_name, category_combobox, add_category_window):
    c = conn.cursor()
    c.execute("SELECT kategooria_nimi FROM Kategooriad WHERE kategooria_nimi=?", (category_name,))
    existing_category = c.fetchone()
    if existing_category is None:
        c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", (category_name,))
        conn.commit()
        category_combobox['values'] = get_categories(conn)
        category_combobox.set(category_name)  
        category_combobox.update()  
        add_category_window.destroy()  
    else:
        messagebox.showerror("Error", "Kategooria juba eksisteerib.") 

def add_new_brand(conn, brand_name, brand_combobox, add_brand_window):
    c = conn.cursor()
    c.execute("SELECT brändi_nimi FROM Brändid WHERE brändi_nimi=?", (brand_name,))
    existing_brand = c.fetchone()
    if existing_brand is None:
        c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", (brand_name,))
        conn.commit()
        brand_combobox['values'] = get_brands(conn)
        brand_combobox.set(brand_name) 
        brand_combobox.update() 
        add_brand_window.destroy()  
    else:
        messagebox.showerror("Error", "Bränd juba eksisteerib.")  

def add_new_brand_window(conn, brand_combobox):
    add_brand_window = tk.Toplevel()
    add_brand_window.title("Lisa uus bränd")

    tk.Label(add_brand_window, text="Uus brändи nimi:").grid(row=0, column=0)
    new_brand_name_entry = tk.Entry(add_brand_window)
    new_brand_name_entry.grid(row=0, column=1)

    add_button = ttk.Button(add_brand_window, text="Lisa", command=lambda: add_new_brand(conn, new_brand_name_entry.get(), brand_combobox, add_brand_window))
    add_button.grid(row=1, columnspan=2)

    return add_brand_window  

def add_new_category_window(conn, category_combobox):
    add_category_window = tk.Toplevel()
    add_category_window.title("Lisa uus kategooria")

    tk.Label(add_category_window, text="Uus kategooria nimi:").grid(row=0, column=0)
    new_category_name_entry = tk.Entry(add_category_window)
    new_category_name_entry.grid(row=0, column=1)

    add_button = ttk.Button(add_category_window, text="Lisa", command=lambda: add_new_category(conn, new_category_name_entry.get(), category_combobox, add_category_window))
    add_button.grid(row=1, columnspan=2)

    return add_category_window  

def open_add_window(conn, tree, new_kategooria, new_brand):
    add_window = tk.Toplevel()
    add_window.title("Lisa uus toode")

    tk.Label(add_window, text="Toote nimi:").grid(row=0, column=0)
    new_toote_nimi = tk.Entry(add_window)
    new_toote_nimi.grid(row=0, column=1)

    tk.Label(add_window, text="Hind:").grid(row=1, column=0)
    new_toote_hind = tk.Entry(add_window)
    new_toote_hind.grid(row=1, column=1)

    tk.Label(add_window, text="Kategooria:").grid(row=2, column=0)
    new_kategooria_combobox = ttk.Combobox(add_window, values=get_categories(conn))
    new_kategooria_combobox.grid(row=2, column=1)

    tk.Label(add_window, text="Bränd:").grid(row=3, column=0)
    new_brand_combobox = ttk.Combobox(add_window, values=get_brands(conn))
    new_brand_combobox.grid(row=3, column=1)

    add_button = ttk.Button(add_window, text="Lisa", command=lambda: add_toode(conn, new_toote_nimi.get(), new_toote_hind.get(), new_kategooria_combobox.get(), new_brand_combobox.get(), add_window, tree))
    add_button.grid(row=4, columnspan=2)

def add_toode(conn, toote_nimi, hind, kategooria, bränd, add_window, tree):
    if toote_nimi.strip() == '' or hind.strip() == '':
        messagebox.showerror("Error", "Toote nimi ja hind ei tohi olla tühjad.")
        return

    try:
        hind = float(hind)
    except ValueError:
        messagebox.showerror("Error", "Hind peab olema number.")
        return

    c = conn.cursor()

    c.execute("SELECT kategooria_id FROM Kategooriad WHERE kategooria_nimi=?", (kategooria,))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", (kategooria,))
        conn.commit()
        kategooria_id = c.lastrowid
    else:
        kategooria_id = result[0]

    c.execute("SELECT brändi_id FROM Brändid WHERE brändi_nimi=?", (bränd,))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", (bränd,))
        conn.commit()
        brändi_id = c.lastrowid
    else:
        brändi_id = result[0]

    c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)",
                (toote_nimi, hind, kategooria_id, brändi_id))
    conn.commit()

    populate_tree(tree, conn)
    add_window.destroy()

def delete_by_category_from_db(conn, tree, category_combobox):
    category_name = category_combobox.get()
    if category_name:
        delete_category_from_db(conn, tree, category_combobox)

def delete_by_brand_from_db(conn, tree, brand_combobox):
    brand_name = brand_combobox.get()
    if brand_name:
        delete_brand_from_db(conn, tree, brand_combobox)

def delete_category_from_db(conn, tree, category_combobox):
    category_name = category_combobox.get()
    if category_name:
        c = conn.cursor()
        c.execute("DELETE FROM Tooted WHERE kategooria_id=(SELECT kategooria_id FROM Kategooriad WHERE kategooria_nimi=?)", (category_name,))
        c.execute("DELETE FROM Kategooriad WHERE kategooria_nimi=?", (category_name,))
        conn.commit()
        populate_tree(tree, conn)
        category_combobox['values'] = get_categories(conn)  
        category_combobox.set("")  


def delete_brand_from_db(conn, tree, brand_combobox):
    brand_name = brand_combobox.get()
    if brand_name:
        c = conn.cursor()
        c.execute("DELETE FROM Tooted WHERE brändi_id=(SELECT brändi_id FROM Brändid WHERE brändi_nimi=?)", (brand_name,))
        c.execute("DELETE FROM Brändid WHERE brändi_nimi=?", (brand_name,))
        conn.commit()
        populate_tree(tree, conn)
        brand_combobox['values'] = get_brands(conn)  
        brand_combobox.set("")


def get_categories(conn):
    c = conn.cursor()
    c.execute("SELECT kategooria_nimi FROM Kategooriad")
    categories = [row[0] for row in c.fetchall()]
    return categories

def get_brands(conn):
    c = conn.cursor()
    c.execute("SELECT brändi_nimi FROM Brändid")
    brands = [row[0] for row in c.fetchall()]
    return brands

def main():
    conn = sqlite3.connect('tooted.db')
    create_database(conn)

    root = tk.Tk()
    root.title("Andmebaasi Haldur")

    tree = ttk.Treeview(root)
    tree["columns"] = ("toote_nimi", "hind", "kategooria", "brändi")
    tree.heading("#0", text="ID")
    tree.heading("toote_nimi", text="Toote nimi")
    tree.heading("hind", text="Hind")
    tree.heading("kategooria", text="Kategooria")
    tree.heading("brändi", text="Brändi")
    tree.pack()

    populate_tree(tree, conn)

    button_frame = tk.Frame(root)
    button_frame.pack(side='top')

    add_button = ttk.Button(button_frame, text="Lisa uus toode", command=lambda: open_add_window(conn, tree, new_kategooria, new_brand))
    add_button.pack(side='left')

    add_category_button = ttk.Button(button_frame, text="Lisa uus kategooria", command=lambda: add_new_category_window(conn, new_kategooria))
    add_category_button.pack(side='left')

    add_brand_button = ttk.Button(button_frame, text="Lisa uus bränd", command=lambda: add_new_brand_window(conn, new_brand))
    add_brand_button.pack(side='left')

    delete_category_button = ttk.Button(button_frame, text="Kustuta kategooria", command=lambda: delete_by_category_from_db(conn, tree, new_kategooria))
    delete_category_button.pack(side='left')

    delete_brand_button = ttk.Button(button_frame, text="Kustuta brändi järgi", command=lambda: delete_by_brand_from_db(conn, tree, new_brand))
    delete_brand_button.pack(side='left')

    new_kategooria_label = tk.Label(root, text="Valige kategooria:")
    new_kategooria_label.pack()

    new_kategooria = ttk.Combobox(root, values=get_categories(conn))
    new_kategooria.pack()

    new_brand_label = tk.Label(root, text="Valige bränd:")
    new_brand_label.pack()

    new_brand = ttk.Combobox(root, values=get_brands(conn))
    new_brand.pack()


    root.mainloop()

if __name__ == "__main__":
    main()
