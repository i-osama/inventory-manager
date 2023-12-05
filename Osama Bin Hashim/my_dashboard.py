from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os
from add_product import add_main_runner
from sell_product import sell_main_runner
import sqlite3


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.getcwd()+"\image"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# def main_dashboard_property(root):

def fetch_total_products():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM available_products")
    total_products = cursor.fetchone()[0]
    return total_products

def fetch_sold_products():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM selling_products")
    total_products = cursor.fetchone()[0]
    return total_products


def my_dashboard_engine():
    window = Tk()

    window.geometry("780x550")
    window.configure(bg = "#343541")

    # main_dashboard_property(root)
    # print("total products ",fetch_total_products())

    
    # window = root
    canvas = Canvas(
        window,
        bg = "#f4ebeb",
        height = 550,
        width = 780,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )


    # canvas.place(x = 0, y = 0)
    # image_image_1 = PhotoImage(
    #     file=relative_to_assets("image_1.png"))
    # image_1 = canvas.create_image(
    #     390.0,
    #     50.0,
    #     image=image_image_1
    # )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file= ASSETS_PATH+"\image_1.png")
    image_1 = canvas.create_image(
        390.0,
        50.0,
        image=image_image_1
    )

    canvas.create_text(
        304.0,
        14.0,
        anchor="nw",
        text="Hishab",
        fill="#FFFFFF",
        font=("Kavoon Regular", 48 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        216.0,
        212.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        216.0,
        391.0,
        image=image_image_3
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_main_runner(),
        relief="flat"
    )
    button_1.place(
        x=470.0,
        y=219.0,
        width=249.0,
        height=105.0
    )

    canvas.create_text(
        64.0,
        353.0,
        anchor="nw",
        text=f"Available products: {fetch_total_products()} ",
        fill="#FFFFFF",
        font=("Arial BoldMT", 24 * -1)
    )

    canvas.create_text(
        64.0,
        400.0,
        anchor="nw",
        text=f"Sold products: {fetch_sold_products()} ",
        fill="#FFFFFF",
        font=("Arial BoldMT", 24 * -1)
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: sell_main_runner(),
        relief="flat"
    )
    button_2.place(
        x=470.0,
        y=361.0,
        width=249.0,
        height=105.0
    )

    window.resizable(False, False)
    window.mainloop()

def dashboard_runner():
    my_dashboard_engine()

if __name__=="__main__":
    # my_dashboard_engine()
    dashboard_runner()