import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import sqlite3

class AddProductWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700+2+2")
        self.root.title("Product Management")
        self.root.focus_displayof()
        self.database()

        # Left side - Data Insertion
        left_frame = tk.Frame(self.root, padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ============================================================================
        # Data ENTRY
        self.entry_name = self.create_input_field(left_frame, "Product Name:")

        # self.entry_date = self.create_input_field(left_frame, "Entry Date:")
        date_label = CTkLabel(left_frame, text="Date", text_color='black', anchor='w')
        date_label.pack(padx=1)
        self.entry_date = CTkEntry(left_frame, fg_color="white", text_color='black', placeholder_text="yyyy-mm-dd", border_width=0.4)
        self.entry_date.pack()

        self.entry_total_amount = self.create_input_field(left_frame, "Quantity:")
        self.entry_price = self.create_input_field(left_frame, "Price:")

        # --------combo box
        # self.entry_category = self.create_input_field(left_frame, "Category:")
          # Role ComboBox
        self.categories = ["Electronics","Chemical", "Perishable"]
        font_name = "Kavivanar"
        font_size = 14
        CTkLabel(left_frame, text="Category:", font=(font_name, font_size),text_color='black', anchor='w').pack(padx=2)
        self.entry_category = CTkComboBox(left_frame, values=self.categories, font=(font_name, font_size, "normal"), width=150, bg_color="white", fg_color="white", text_color='black', border_width=0.4)
        self.entry_category.pack(ipady= 5)

        self.entry_provider = self.create_input_field(left_frame, "Provider:")
        
        # self.entry_description = self.create_input_field(left_frame, "Description:")
        CTkLabel(left_frame, text="Description", text_color='black', anchor='w').pack(padx= 5)
        self.entry_description = CTkTextbox(left_frame, fg_color="white",height=10, width= 150, text_color='black')
        self.entry_description.pack(ipady=40)

        self.entry_entered_by = self.create_input_field(left_frame, "Entered By:")
        # ============================================================================

        # self.add_button = tk.Button(left_frame, text="Add Product", command=self.add_product, font="Arial 11 bold", bg='green', fg= 'white')
        self.add_button = CTkButton(left_frame, text="Add", command=self.add_product, font=("Arial", 11), fg_color='#5b79a1', text_color="white")
        self.add_button.pack(ipadx=4, ipady=4, pady=10)
        self.update_button = CTkButton(left_frame, text="Update", command=self.update_products, font=("Arial", 11), fg_color='#5b79a1', text_color="white")
        self.update_button.configure(state=tk.DISABLED)
        self.update_button.pack(ipadx=5, ipady=4, pady=10)

        # Right side - Data Viewing (Treeview)
        self.right_frame = tk.Frame(self.root, padx=20, pady=20)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

          # Buttons
        # Create a frame for the buttons
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        # self.edit_btn = CTkButton(button_frame, text="Edit", command=lambda: my_function(value_to_pass))
        self.edit_btn = CTkButton(button_frame, text="Edit", command=self.on_edit_button_click)
        self.edit_btn.pack(side=tk.RIGHT, padx=5, pady=0)

        self.delete_btn = CTkButton(button_frame, text="Delete", command= self.delete_data_from_DB)
        self.delete_btn.pack(side=tk.RIGHT, padx=5, pady=0)

        self.show_from_db_to_treeview(self.right_frame)

    def on_edit_button_click(self):
        selected_item = self.tree.selection()  # Get the selected item
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            # setting value for the entry box
                # item_values = self.tree.item(selected_item, 'values')

            # Assuming item_values is a tuple containing values in the order of entry fields
            if len(item_values) >= 6:  # Assuming you have at least 6 values in item_values
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, item_values[1])  # Assuming Name is the second value in item_values

                self.entry_date.delete(0, tk.END)
                self.entry_date.insert(0, item_values[2])  # Assuming Entry Date is the third value in item_values

                self.entry_total_amount.delete(0, tk.END)
                self.entry_total_amount.insert(0, item_values[3])  # Assuming Quantity is the fourth value in item_values

                self.entry_price.delete(0, tk.END)
                self.entry_price.insert(0, item_values[4])  # Assuming Price is the fifth value in item_values

                # Set the Category Combobox value
                if item_values[5] in self.categories:
                    self.entry_category.set(item_values[5])  # Assuming Category is the sixth value in item_values

                self.entry_provider.delete(0, tk.END)
                self.entry_provider.insert(0, item_values[6])  # Assuming Provider is the seventh value in item_values

                # Assuming Description is the eighth value in item_values
                self.entry_description.delete("1.0", tk.END)
                self.entry_description.insert("1.0", item_values[7])

                self.entry_entered_by.delete(0, tk.END)
                self.entry_entered_by.insert(0, item_values[8]) 

                # ------ Changing the button state -----------------
                self.update_button.configure(state=tk.NORMAL)
                self.add_button.configure(state=tk.DISABLED)

        # ----------- Else --------
        else:
            print("Please select an item to edit.")

    def show_from_db_to_treeview(self, frame):
        # Define a custom font
        custom_font = ("Arial", 12)  # Change the font family and size as needed

        # Create a style object
        style = ttk.Style()
        style.configure("Treeview", font=custom_font)

        self.tree = ttk.Treeview(frame, columns=("ID", "Name", "Entry Date", "Quantity", "Price", "Category", "Provider", "Description", "Entered By"))

        # Configure column properties
        self.tree.column("#0", width=50, minwidth=50, stretch=tk.NO)  # ID column
        self.tree.column("#1", width=100, minwidth=100, stretch=tk.NO)  # Name column
        self.tree.column("#2", width=100, minwidth=100, stretch=tk.NO)  # Entry Date column
        self.tree.column("#3", width=80, minwidth=80, stretch=tk.NO)  # Quantity column
        self.tree.column("#4", width=80, minwidth=80, stretch=tk.NO)  # Price column
        self.tree.column("#5", width=100, minwidth=100, stretch=tk.NO)  # Category column
        self.tree.column("#6", width=100, minwidth=100, stretch=tk.NO)  # Provider column
        self.tree.column("#7", width=150, minwidth=150, stretch=tk.NO)  # Description column
        self.tree.column("#8", width=100, minwidth=100, stretch=tk.NO)  # Entered By column

        # heading
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Name")
        self.tree.heading("#2", text="Entry Date")
        self.tree.heading("#3", text="Quantity")
        self.tree.heading("#4", text="Price")
        self.tree.heading("#5", text="Category")
        self.tree.heading("#6", text="Provider")
        self.tree.heading("#7", text="Description")
        self.tree.heading("#8", text="Entered By")

        self.conn = sqlite3.connect('storage.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM available_products")
        rows = self.cursor.fetchall()

        self.tree.pack(fill=tk.BOTH, expand=True, pady=15)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        for row in rows:
            # Ensure that the order of values matches the order of columns defined in treeview
            self.tree.insert('', tk.END, values=row)

        self.conn.commit()
        self.conn.close()

    def on_tree_select(self, event):
        # -------------Getting a selected value from the tree----------------
        item = self.tree.selection()[0]  # Get the selected item
        item_values = self.tree.item(item, 'values')  # Get the values of the selected item
        # print("Selected Item:", item_values)
        return item_values

    def create_input_field(self, frame, label_text):
        label = CTkLabel(frame, text=label_text, text_color='black', anchor='w')
        label.pack(padx=1)
        entry = CTkEntry(frame, fg_color="white", text_color='black', border_width=0.4, width=150)
        entry.pack()
        return entry

    def add_product(self):
        product_data = (
            self.entry_name.get(),
            self.entry_date.get(),
            self.entry_total_amount.get(),
            self.entry_price.get(),
            self.entry_category.get(),
            self.entry_provider.get(),
            self.entry_description.get("1.0", tk.END),
            self.entry_entered_by.get()
        )

        # database connection and data insertion
        self.conn = sqlite3.connect("storage.db")
        self.cursor = self.conn.cursor()

        # product_data = (
        # "Product Name",
        # "2023-12-31",  # Entry Date in YYYY-MM-DD format
        # 10,            # Quantity
        # 25.99,         # Price
        # "Category",
        # "Provider Name",
        # "Product Description",
        # "Entered By"
        # )

        # SQL command to insert data into the table
        insert_query = '''
            INSERT INTO available_products (Name, Entry_Date, Quantity, Price, Category, Provider, Description, Entered_By)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Execute the SQL command with the sample data
        self.cursor.execute(insert_query, product_data)

        self.conn.commit()
        self.conn.close()

        self.delete_entry_box()

        self.tree.insert("", tk.END, values=product_data)
    
    def update_products(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')

            # Get the updated values from the entry fields
            product_data = (
                self.entry_name.get(),
                self.entry_date.get(),
                self.entry_total_amount.get(),
                self.entry_price.get(),
                self.entry_category.get(),
                self.entry_provider.get(),
                self.entry_description.get("1.0", tk.END),
                self.entry_entered_by.get()
            )

            self.conn = sqlite3.connect("storage.db")
            self.cursor = self.conn.cursor()

            update_query = '''
                UPDATE available_products 
                SET Name=?, Entry_Date=?, Quantity=?, Price=?, Category=?, Provider=?, Description=?, Entered_By=?
                WHERE ID=?
            '''

            self.cursor.execute(update_query, product_data + (item_values[0],))  # Assuming ID is the first value

            self.conn.commit()
            self.conn.close()

            self.restart_window()
        
    def delete_data_from_DB(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()
        if selected_item:     
            self.conn = sqlite3.connect("storage.db")
            self.cursor = self.conn.cursor()

            item_values = self.tree.item(selected_item, 'values')
            item_id = item_values[0]
            # print("id: ", item_id)

            self.cursor.execute("DELETE FROM available_products WHERE ID=?", (item_id,))
            self.conn.commit()

            # Delete the selected item from the treeview
            self.tree.delete(selected_item)
            self.conn.commit()
            self.conn.close()
        
    def restart_window(self):
        # Destroy the current window
        self.root.destroy()

        # Create a new instance of the root window
        new_root = tk.Tk()
        new_root.geometry("1000x700+2+2")
        AddProductWindow(new_root)       


    def delete_entry_box(self):
        self.entry_name.delete(0, 'end'),
        self.entry_date.delete(0, 'end'),
        self.entry_total_amount.delete(0, 'end'),
        self.entry_price.delete(0, 'end'),
        self.entry_provider.delete(0, 'end'),
        self.entry_entered_by.delete(0, 'end'),
        self.entry_description.delete("1.0", tk.END)
   
    def database(self):
        self.conn = sqlite3.connect("storage.db")
        self.cur = self.conn.cursor()

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS available_products (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Entry_Date TEXT,
        Quantity INTEGER,
        Price REAL,
        Category TEXT,
        Provider TEXT,
        Description TEXT,
        Entered_By TEXT
    )
    ''')

        self.conn.commit()
        self.conn.close()

def add_main_runner():
    app = CTk()
    AddProductWindow(app)
    app.mainloop()

if __name__ == "__main__":
    add_main_runner()
