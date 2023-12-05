import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
from customtkinter import *
from register import Register_User, regRunner
from CTkMessagebox import CTkMessagebox
from my_dashboard import dashboard_runner
import sqlite3
import subprocess


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Interface")
        self.root.geometry("800x400+50+50")
        self.root.resizable(False, False)
        self.LoggedIn_User_ID = ''

        self.left_frame = tk.Frame(self.root, width=400, height=500)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.root, width=400, height=500)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.load_image()
        self.create_login_form()

    def load_image(self):
        image = Image.open("image/login_bg.jpg")  # Replace "img.jpg" with your image file
        # w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        # image = image.resize((int(w * 0.4), h), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.left_frame, image=photo, height=400, width=500)
        label.image = photo
        label.pack(fill="both", expand=True)

    def create_login_form(self):
        self.banner_label = tk.Label(self.right_frame, text="Login here",  font=("Lemon", 26))
        self.banner_label.pack(pady=(3,10), anchor='n', padx=20)

        self.username_label = tk.Label(self.right_frame, text="Username:", font="Kavivanar 12 italic")
        self.username_label.pack(pady=(20,1), anchor='w', padx=20)

        self.username_entry = tk.Entry(self.right_frame, width=200, font="Kavivanar 11 normal",bd=1)
        self.username_entry.pack(pady=4, padx=20, ipadx=5, ipady=5)

        self.password_label = tk.Label(self.right_frame, text="Password:", font="Kavivanar 12 italic")
        self.password_label.pack(pady=2, anchor='w', padx=20)

        self.password_entry = tk.Entry(self.right_frame, show="*", width=200, font="Kavivanar 11 normal",bd=1)
        self.password_entry.pack(pady=(2,6), padx=20,  ipadx=5, ipady=5)

        self.login_button = tk.Button(self.right_frame, text="Login",font="Kavivanar 13 bold", bg="green", fg="white", command=self.login)
        self.login_button.pack(pady=(20,2), padx=20, ipadx=50, ipady=4)

        self.login_button = tk.Button(self.right_frame, text="Register",font="Kavivanar 10 normal", bg="#f0f0f0", fg="green", bd=0, command=self.register_user)
        self.login_button.pack(pady=1, padx=20, ipadx=50, ipady=4)

        self.error_label = tk.Label(self.right_frame, text="", fg="red")
        self.error_label.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check login credentials (replace this with your verification logic)
        if username == "" or password == "":
            CTkMessagebox(title="Blank box", message="Please enter the username and password")
            # self.open_dashboard()
            # self.root.destroy()
        
        elif username=="AUTHOR-00" and password =="who is author?":
            tk.messagebox.showinfo("AUTHOR","""This Program is created by\nOSAMA BIN HASHIM
            \nEmail: osama.binhashim.me@gmail.com
            \nFacebook: https://www.facebook.com/osama.binhashim.56/
            """)

        else:
            conn = sqlite3.connect("storage.db")
            cur = conn.cursor()
            cur.execute("SELECT *,oid FROM users WHERE username=? AND password=?", (username, password))
            result = cur.fetchone()
            # print(result)
            if result != None:
                self.LoggedIn_User_ID= result[-1]
                # ------------------------ Go to the dashboard window ---------------
                # dashboard_main()

                subprocess.Popen(["python", "my_dashboard.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')

                # # # self.root.quit()
                # self.new_win = CTkToplevel(self.root)
                # # self.new_win.lift()
                # self.dashboard_win = Dashboard(self.new_win)
                # self.root.withdraw()
                # self.root.destroy()

                # dashboard_runner()
                # self.root.destroy()


            # print("ID ",result[-1])

            conn.commit()
            conn.close()

    def register_user(self):
        self.new_win = CTkToplevel(self.root)
        # self.register_win = regRunner()
        self.register_win = Register_User(self.new_win)
        # self.root.withdraw()
        # self.root.quit()

    # def register_user(self):
    #     self.root.withdraw()  # Hide the main window
    #     self.second_window = Register_User(self.root, self.close_main_window)

    def close_main_window(self):
        self.root.destroy()  # Close the main window


if __name__ == "__main__":
    # global LoggedIn_User_ID
    # LoggedIn_User_ID = ''
    root = tk.Tk()
    # root = CTk()
    # database()
    app = LoginApp(root)
    root.resizable(False, False)
    root.mainloop()
