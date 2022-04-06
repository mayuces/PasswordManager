from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
CANVAS_HEIGHT = 200
CANVAS_WIDTH = 200


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for char in range(randint(2, 4))]
    password_numbers = [choice(numbers) for char in range(randint(2, 4))]

    password_list = password_symbols + password_letters + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_dict = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Ooops", message="Some fields are empty")
    else:
        try:
            with open("password_file.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("password_file.json", "w") as data_file:
                #create if no file
                json.dump(new_dict, data_file, indent=4)
        else:
            # updating old data with new data
            data.update(new_dict)
            with open("password_file.json", "w") as data_file:
                #saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open("password_file.json", "r") as data_file:
            # reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File is empty")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


window = Tk()
window.title("Password Manager")
window.config(padx=CANVAS_WIDTH/5, pady=CANVAS_HEIGHT/5)

canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
main_img = PhotoImage(file="logo.png")
canvas.create_image(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, image=main_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Usarname:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, columnspan=1, sticky="EW")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "myucesoylu@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2, sticky="EW")





window.mainloop()