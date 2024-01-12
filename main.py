from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'
        , 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    new_password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, new_password)
    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == "" or password == "" or email == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        is_okay = messagebox.askokcancel(title=f"{website}", message=f"These are the details \n Email: {email} "
                                                                     f"\n Password: {password} \n is it okay to save?")
        if is_okay:
            try:
                with open("data.json", "r") as read_file:
                    data = json.load(read_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, "end")
                password_entry.delete(0, "end")


# ---------------------------- Search Password ------------------------------- #


def search():
    website = website_entry.get().title()
    try:
        with open("data.json") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Search Result", message=f"Your details are: \nEmail: {email} \n"
                                                           f"Password: {password}")
        else:
            messagebox.showinfo(title="error", message=f"No details for the {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

logo = PhotoImage(file="logo.png", )
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# website label and entry
website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

# email/username label and entry
email_label = Label(text="Email/Username: ")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "parth4055@gmail.com")

# password label, entry and generate password button
password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")

gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(column=2, row=3)

# add button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, sticky="EW", columnspan=2)

# search button
search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)
window.mainloop()