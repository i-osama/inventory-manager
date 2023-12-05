import tkinter as tk
from tkinter import ttk
from tkinter import *
from customtkinter import *
import sqlite3

class ProductSellingInterface:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Product Selling Interface")
        
        # Create database connection
        self.conn = sqlite3.connect('storage.db')
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS selling_products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                selling_date DATE,
                                quantity INTEGER,
                                selling_price REAL,
                                additional_info TEXT,
                                sold_by TEXT
                            )''')
        
        # Top Frame for data entry
        self.top_frame = CTkFrame(self.root)
        self.top_frame.pack(fill=BOTH)

        self.entry_name = self.entry_box("Product Name ")

        self.entry_selling_date = self.entry_box("Selling Date (yyyy-mm-dd)")

        self.entry_quantity= self.entry_box("Quantity")
        self.entry_selling_price = self.entry_box("Selling price")

        self.entry_additional_info = self.entry_box("Additional info: ")

        self.entry_sold_by = self.entry_box("Sold by: ")

        # Buttons
        button_frame = CTkFrame(self.root)
        button_frame.pack(pady=10)

        CTkButton(button_frame, text="Add to Sell List", command=self.add_to_sell_list).pack(side=tk.LEFT, padx=5)
        # CTkButton(button_frame, text="Update", command=self.update_data).pack(side=tk.LEFT, padx=5)
        CTkButton(button_frame, text="Delete", command=self.delete_data).pack(side=tk.LEFT, padx=5)
        CTkButton(button_frame, text="Clear", command=self.clear_entries).pack(side=tk.LEFT, padx=5)

        # Treeview
        custom_font = ("Arial", 12) 
        style = ttk.Style()
        style.configure("Treeview", font=custom_font)

        self.tree = ttk.Treeview(self.root, columns=("","Name", "Selling Date", "Quantity", "Selling Price", "Additional Info", "Sold By"))
        self.tree.pack(fill=tk.BOTH, anchor=tk.W, expand=True)

        # -----------Configurin column properties
        self.tree.column("#0", width=50, minwidth=50, stretch=tk.NO)  # ID column
        self.tree.column("#1", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("#2", width=100, minwidth=100, stretch=tk.NO)  
        self.tree.column("#3", width=80, minwidth=80, stretch=tk.NO)  
        self.tree.column("#4", width=80, minwidth=80, stretch=tk.NO)  
        self.tree.column("#5", width=100, minwidth=100, stretch=tk.NO)  
        self.tree.column("#6", width=100, minwidth=100, stretch=tk.NO)  
        self.tree.column("#7", width=100, minwidth=100, stretch=tk.NO)  

        # # heading
        self.tree.heading("#0", text="ID",  anchor=tk.W)
        self.tree.heading("#1", text="Name",   anchor=tk.W)
        self.tree.heading("#2", text="Selling Date",  anchor=tk.W)
        self.tree.heading("#3", text="Quantity",  anchor=tk.W)
        self.tree.heading("#4", text="Selling Price",  anchor=tk.W)
        self.tree.heading("#5", text="Additional Info",  anchor=tk.W)
        self.tree.heading("#6", text="Sold By", anchor=tk.W)
        self.tree.heading("#7", text="Sold By", anchor=tk.W)
        # # heading
        # self.tree.heading(text="ID", width= 50, expand= True)
        # self.tree.heading(text="Name", width= 50, expand= True)
        # self.tree.heading(text="Selling Date", width= 50, expand= True)
        # self.tree.heading(text="Quantity", width= 50, expand= True)
        # self.tree.heading(text="Selling Price", width= 50, expand= True)
        # self.tree.heading(text="Additional Info", width= 50, expand= True)
        # self.tree.heading(text="Sold By", width= 50, expand= True)
    

        self.refresh_treeview()

    def entry_box(self, label_name):
        frame = CTkFrame(self.top_frame)

        font_name = "Arial"
        font_size = 14
        font_style = "bold"
        label = CTkLabel(frame, text=label_name, font=(font_name, font_size, font_style), text_color='white', anchor='w', width=200)
        label.pack(side= LEFT, padx=(20,10), pady= 5, ipady= 5)

        entry = CTkEntry(frame, fg_color="white", font=(font_name, 13, "bold"), text_color='black', border_width=0.4, width=200)
        entry.pack(side=LEFT, padx=10, pady= 5)

        frame.pack(fill=tk.X)

        return entry


    def add_to_sell_list(self):
        name = self.entry_name.get()
        selling_date = self.entry_selling_date.get()
        quantity = self.entry_quantity.get()
        selling_price = self.entry_selling_price.get()
        additional_info = self.entry_additional_info.get()
        sold_by = self.entry_sold_by.get()

        # Insert data into the database
        self.cursor.execute('''INSERT INTO selling_products 
                                (name, selling_date, quantity, selling_price, additional_info, sold_by) 
                                VALUES (?, ?, ?, ?, ?, ?)''', 
                                (name, selling_date, quantity, selling_price, additional_info, sold_by))
        self.conn.commit()
        self.refresh_treeview()
        self.clear_entries()

    def update_data(self):
        pass

    def delete_data(self):
         # Get the selected item from the treeview
        selected_item = self.tree.selection()
        
        if not selected_item:
            # If no item is selected, prompt the user to select an item
            print("Please select an item to delete.")
            return

        for item in selected_item:
            # Retrieve the item's ID from the treeview
            item_id = self.tree.item(item, "values")[0]

            # Delete the item from the database based on its ID
            self.cursor.execute('''DELETE FROM selling_products WHERE id=?''', (item_id,))
            self.conn.commit()

        # Refresh the treeview after deletion
        self.refresh_treeview()

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_selling_date.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_selling_price.delete(0, tk.END)
        self.entry_additional_info.delete(0, tk.END)
        self.entry_sold_by.delete(0, tk.END)

    def refresh_treeview(self):
        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch data from the database and populate the treeview
        self.cursor.execute('''SELECT * FROM selling_products''')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

def sell_main_runner():
    root = CTk()
    app = ProductSellingInterface(root)
    root.mainloop()

if __name__=="__main__":
    sell_main_runner()
