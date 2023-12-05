import customtkinter as ctk
from PIL import Image
from tkinter import *
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import sqlite3

class Register_User:
    def __init__(self, root):        

        self.root = root
        self.root.geometry("400x650+900+100")
        self.root.title("Register | Hishab")
        self.root.focus_force()

        CTkLabel(self.root, text="Sign Up", font=("Lemon", 36)).pack(padx=100, pady=(20,2))
        
        self.canvas = CTkCanvas(self.root, height=0.5, width=400, bg="blue")
        self.canvas.pack(anchor="n")
        # self.canvas.create_line(0, 0, 300, 300)

        # ctk.set_default_color_theme("dark-blue")

        # ctk.CTkLabel(self.root, text="Hello").pack(padx=100, pady=200)
        # self.button = ctk.CTkButton(self.root, text="my button")
        # self.button.pack(padx=20, pady=20)
        self.setTheRegBox()


    def setTheRegBox(self):
        font_name = "Kavivanar"
        font_size = 14

        self.frm1 = ctk.CTkFrame(self.root)

        # CTkLabel(self.root, t )

        # Username Entry
        CTkLabel(self.frm1, text="Username:", font=(font_name, font_size, "italic")).pack(padx=20, pady=(25,2), anchor='w', ipadx= 20)
        self.username_entry = CTkEntry(self.frm1, font=(font_name, font_size, "normal"), width=200)
        self.username_entry.pack(padx=20, pady=1, anchor='w', ipadx= 20, ipady= 5)

        # Password Entry
        CTkLabel(self.frm1, text="Password:", font=(font_name, font_size)).pack(padx=20, pady=5, anchor='w', ipadx= 20)
        self.password_entry = CTkEntry(self.frm1, show="*", font=(font_name, font_size, "normal"), width=200)
        self.password_entry.pack(padx=20, pady=5, anchor='w', ipadx= 20, ipady=5)

        # Re-enter Password Entry
        CTkLabel(self.frm1, text="Re-enter Password:", font=(font_name, font_size, "italic")).pack(padx=20, pady=5, anchor='w', ipadx= 20)
        self.reenter_password_entry = CTkEntry(self.frm1, show="*", font=(font_name, font_size, "normal"), width=200)
        self.reenter_password_entry.pack(padx=20, pady=5, anchor='w', ipadx= 20, ipady=5)

        # Email Entry
        CTkLabel(self.frm1, text="Email:" , font=(font_name, font_size, "italic")).pack(padx=20, pady=5, anchor='w', ipadx= 20)
        self.email_entry = CTkEntry(self.frm1, font=(font_name, font_size, "normal"), width=200)
        self.email_entry.pack(padx=20, pady=5, anchor='w', ipadx= 20, ipady= 5)

        # Role ComboBox
        roles = ["Viewer","Editor", "Admin"]
        CTkLabel(self.frm1, text="Role:", font=(font_name, font_size, "italic")).pack(padx=20, pady=5, anchor='w', ipadx= 20)
        self.role_combobox = CTkComboBox(self.frm1, values=roles, font=(font_name, font_size, "normal"), width=200)
        self.role_combobox.pack(padx=20, pady=5, anchor='w', ipadx= 20, ipady= 5)

        # Sign Up Button
        self.signup_button = CTkButton(self.frm1, text="Sign Up", font=(font_name, 16, "normal"), command=self.register)
        self.signup_button.pack(padx=20, pady=20, ipady= 8)

        self.frm1.pack(anchor='c', pady=20)

    def register(self):
        if self.username_entry.get()=="" or self.email_entry.get()=="" or self.password_entry.get()=="" or self.reenter_password_entry.get()=="":
            CTkMessagebox(title="Error", message="Please fill all the box")
        elif self.password_entry.get() != self.reenter_password_entry.get():
            CTkMessagebox(title="Incorrect", message="Password does not matched!")
        else:    
            conn = sqlite3.connect("storage.db")
            cur = conn.cursor()

            # print(self.role_combobox.get())
            cur.execute("INSERT INTO users VALUES ( :username, :email, :password, :role)",
            {
                'username': self.username_entry.get(),
                'email':self.email_entry.get(),
                'password':self.password_entry.get(),
                'role':self.role_combobox.get()
            })

            conn.commit()
            conn.close()

            CTkMessagebox(title="Complete", message="New user included")
            self.root.destroy()

def regRunner():
    # root = Tk()
    root = CTk()
    Register_User(root)
    # Register_User.close_windows()
    root.mainloop()

if __name__=="__main__":
  regRunner()