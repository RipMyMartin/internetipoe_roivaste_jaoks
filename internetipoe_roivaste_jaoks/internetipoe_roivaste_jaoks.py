import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class AndmebaasiHaldur:
    def __init__(self, master):
        self.master = master
        self.master.title("Andmebaasi Haldur")

        
        self.conn = sqlite3.connect('tooted.db')
        self.c = self.conn.cursor()
        self.create_database()

        self.create_widgets()

    def create_database(self):
        
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tooted'")
        result = self.c.fetchone()
        if result is None:
            
            self.c.execute('''CREATE TABLE Tooted (
                                toote_id INTEGER PRIMARY KEY,
                                toote_nimi TEXT,
                                hind REAL,
                                kategooria_id INTEGER,
                                brändi_id INTEGER,
                                FOREIGN KEY (kategooria_id) REFERENCES Kategooriad(kategooria_id),
                                FOREIGN KEY (brändi_id) REFERENCES Brändid(brändi_id)
                            )''')
            self.conn.commit()

           
            self.c.execute('''CREATE TABLE IF NOT EXISTS Kategooriad (
                                kategooria_id INTEGER PRIMARY KEY,
                                kategooria_nimi TEXT UNIQUE
                            )''')
            self.c.execute('''CREATE TABLE IF NOT EXISTS Brändid (
                                brändi_id INTEGER PRIMARY KEY,
                                brändi_nimi TEXT UNIQUE
                            )''')
            self.conn.commit()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("toote_nimi", "hind", "kategooria", "bränd")
        self.tree.heading("#0", text="ID")
        self.tree.heading("toote_nimi", text="Toote nimi")
        self.tree.heading("hind", text="Hind")
        self.tree.heading("kategooria", text="Kategooria")
        self.tree.heading("bränd", text="Bränd")
        self.tree.pack()

        self.populate_tree()

        
        button_frame = tk.Frame(self.master)
        button_frame.pack(side='top')

        add_button = ttk.Button(button_frame, text="Lisa uus toode", command=self.open_add_window)
        add_button.pack(side='left')

        edit_button = ttk.Button(button_frame, text="Muuda valitud toodet", command=self.open_edit_window)
        edit_button.pack(side='left')

        delete_button = ttk.Button(button_frame, text="Kustuta valitud toode", command=self.delete_selected_toode)
        delete_button.pack(side='left')

        delete_by_category_button = ttk.Button(button_frame, text="Kustuta kategooria järgi", command=self.delete_by_category)
        delete_by_category_button.pack(side='left')

        delete_by_brand_button = ttk.Button(button_frame, text="Kustuta brändi järgi", command=self.delete_by_brand)
        delete_by_brand_button.pack(side='left')

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.c.execute('''SELECT Tooted.toote_id, Tooted.toote_nimi, Tooted.hind, Kategooriad.kategooria_nimi, Brändid.brändi_nimi 
                        FROM Tooted 
                        INNER JOIN Kategooriad ON Tooted.kategooria_id = Kategooriad.kategooria_id 
                        INNER JOIN Brändid ON Tooted.brändi_id = Brändid.brändi_id''')
        for row in self.c.fetchall():
            self.tree.insert("", "end", text=row[0], values=row[1:])

    def open_add_window(self):
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title("Lisa uus toode")

        tk.Label(self.add_window, text="Toote nimi:").grid(row=0, column=0)
        self.new_toote_nimi = tk.Entry(self.add_window)
        self.new_toote_nimi.grid(row=0, column=1)

        tk.Label(self.add_window, text="Hind:").grid(row=1, column=0)
        self.new_toote_hind = tk.Entry(self.add_window)
        self.new_toote_hind.grid(row=1, column=1)

        tk.Label(self.add_window, text="Kategooria:").grid(row=2, column=0)
        self.new_kategooria = tk.Entry(self.add_window)
        self.new_kategooria.grid(row=2, column=1)

        tk.Label(self.add_window, text="Bränd:").grid(row=3, column=0)
        self.new_bränd = tk.Entry(self.add_window)
        self.new_bränd.grid(row=3, column=1)

        add_button = ttk.Button(self.add_window, text="Lisa", command=self.add_toode)
        add_button.grid(row=4, columnspan=2)

    def add_toode(self):
        toote_nimi = self.new_toote_nimi.get()
        hind = float(self.new_toote_hind.get())
        kategooria = self.new_kategooria.get()
        bränd = self.new_bränd.get()

        
        self.c.execute("SELECT kategooria_id FROM Kategooriad WHERE kategooria_nimi=?", (kategooria,))
        result = self.c.fetchone()
        if result is None:
            self.c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", (kategooria,))
            self.conn.commit()
            kategooria_id = self.c.lastrowid
        else:
            kategooria_id = result[0]

        
        self.c.execute("SELECT brändi_id FROM Brändid WHERE brändi_nimi=?", (bränd,))
        result = self.c.fetchone()
        if result is None:
            self.c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", (bränd,))
            self.conn.commit()
            brändi_id = self.c.lastrowid
        else:
            brändi_id = result[0]

        
        self.c.execute("INSERT INTO Tooted (toote_nimi, hind, kategooria_id, brändi_id) VALUES (?, ?, ?, ?)",
                       (toote_nimi, hind, kategooria_id, brändi_id))
        self.conn.commit()

        self.populate_tree()
        self.add_window.destroy()

    def open_edit_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = self.tree.item(selected_item)
        toode_id = item['text']
        toode_info = item['values']
        if not toode_info:
            return

        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title("Muuda toodet")

        tk.Label(self.edit_window, text="Uus toote nimi:").grid(row=0, column=0)
        self.edit_toote_nimi = tk.Entry(self.edit_window)
        self.edit_toote_nimi.insert(0, toode_info[0])
        self.edit_toote_nimi.grid(row=0, column=1)

        tk.Label(self.edit_window, text="Uus hind:").grid(row=1, column=0)
        self.edit_toote_hind = tk.Entry(self.edit_window)
        self.edit_toote_hind.insert(0, toode_info[1])
        self.edit_toote_hind.grid(row=1, column=1)

        tk.Label(self.edit_window, text="Uus kategooria:").grid(row=2, column=0)
        self.edit_kategooria = tk.Entry(self.edit_window)
        self.edit_kategooria.insert(0, toode_info[2])
        self.edit_kategooria.grid(row=2, column=1)

        tk.Label(self.edit_window, text="Uus bränd:").grid(row=3, column=0)
        self.edit_bränd = tk.Entry(self.edit_window)
        self.edit_bränd.insert(0, toode_info[3])
        self.edit_bränd.grid(row=3, column=1)

        edit_button = ttk.Button(self.edit_window, text="Salvesta muudatused", command=lambda: self.save_edited_toode(toode_id))
        edit_button.grid(row=4, columnspan=2)

    def save_edited_toode(self, toode_id):
        uus_toote_nimi = self.edit_toote_nimi.get()
        uus_hind = float(self.edit_toote_hind.get())
        uus_kategooria = self.edit_kategooria.get()
        uus_bränd = self.edit_bränd.get()

        
        self.c.execute("SELECT kategooria_id FROM Kategooriad WHERE kategooria_nimi=?", (uus_kategooria,))
        result = self.c.fetchone()
        if result is None:
            self.c.execute("INSERT INTO Kategooriad (kategooria_nimi) VALUES (?)", (uus_kategooria,))
            self.conn.commit()
            uus_kategooria_id = self.c.lastrowid
        else:
            uus_kategooria_id = result[0]

        
        self.c.execute("SELECT brändi_id FROM Brändid WHERE brändi_nimi=?", (uus_bränd,))
        result = self.c.fetchone()
        if result is None:
            self.c.execute("INSERT INTO Brändid (brändi_nimi) VALUES (?)", (uus_bränd,))
            self.conn.commit()
            uus_brändi_id = self.c.lastrowid
        else:
            uus_brändi_id = result[0]

        
        self.c.execute('''UPDATE Tooted 
                          SET toote_nimi=?, hind=?, kategooria_id=?, brändi_id=? 
                          WHERE toote_id=?''',
                       (uus_toote_nimi, uus_hind, uus_kategooria_id, uus_brändi_id, toode_id))
        self.conn.commit()

        self.populate_tree()
        self.edit_window.destroy()

    def delete_selected_toode(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        toode_id = self.tree.item(selected_item)['text']
        self.c.execute("DELETE FROM Tooted WHERE toote_id=?", (toode_id,))
        self.conn.commit()
        self.populate_tree()

    def delete_by_category(self):
        category_name = simpledialog.askstring("Delete by Category", "Sisestage kustutatava kategooria nimi:")
        if category_name:
            self.delete_by_category_from_db(category_name)

    def delete_by_brand(self):
        brand_name = simpledialog.askstring("Delete by Brand", "Sisestage kustutatava brändi nimi:")
        if brand_name:
            self.delete_by_brand_from_db(brand_name)

    def delete_by_category_from_db(self, category_name):
        self.c.execute("DELETE FROM Tooted WHERE kategooria_id IN (SELECT kategooria_id FROM Kategooriad WHERE kategooria_nimi=?)", (category_name,))
        self.conn.commit()
        self.populate_tree()

    def delete_by_brand_from_db(self, brand_name):
        self.c.execute("DELETE FROM Tooted WHERE brändi_id IN (SELECT brändi_id FROM Brändid WHERE brändi_nimi=?)", (brand_name,))
        self.conn.commit()
        self.populate_tree()

root = tk.Tk()
app = AndmebaasiHaldur(root)
root.mainloop()
