#Somesh Ramdas jatti
#Task-3 Simple Password Generator


import string
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import re
import sqlite3
import pyperclip  # for clipboard integration

# Updated password complexity rules
complexity_rules = {
    'uppercase': True,
    'lowercase': True,
    'digits': True,
    'special_chars': True,
}

# Function to generate a password with given complexity
def generate_password(length, rules):
    password = ''
    allowed_chars = ''

    if rules['uppercase']:
        allowed_chars += string.ascii_uppercase
    if rules['lowercase']:
        allowed_chars += string.ascii_lowercase
    if rules['digits']:
        allowed_chars += string.digits
    if rules['special_chars']:
        allowed_chars += string.punctuation

    if allowed_chars:
        password = ''.join(random.choice(allowed_chars) for _ in range(length))
    else:
        messagebox.showerror("Error", "Please select at least one character type for complexity.")

    return password

class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        root.title('Password Generator')
        root.geometry('660x500')
        root.resizable(False, False)

        fr1 = Frame(root, width=200, height=2, bg='black')
        fr1.place(relx=0.39, rely=0.23)

        fr2 = Frame(root, width=50, height=2, bg='black')
        fr2.place(relx=0.43, rely=0.33)

        self.label = Label(text="Password Generator", anchor=N, font=('Georgia', 15, 'bold'),fg='black',bg='white',border=0)
        self.label.place(relx=0.5, rely=0.05, anchor=N)

        self.user = Label(text="Enter username: ", font=('Georgia', 13),fg='black',bg='white',border=0)
        self.user.place(relx=0.15, rely=0.2, anchor=W)

        self.textfield = Entry(textvariable=self.n_username, font=('Georgia', 13),width=25,fg='black',border=0,bg="white")
        self.textfield.place(relx=0.39, rely=0.2, anchor=W)

        self.length = Label(text="Enter password length: ", font=('Georgia', 13),fg='black',bg='white',border=0)
        self.length.place(relx=0.14, rely=0.3, anchor=W)

        self.length_textfield = Entry(textvariable=self.n_passwordlen, font=('Georgia', 13),border=0)
        self.length_textfield.place(relx=0.43, rely=0.3, anchor=W)

        self.generated_password = Label(text="Generated password: ", font=("Georgia", 13),fg='black',bg='white',border=0)
        self.generated_password.place(relx=0.15, rely=0.4, anchor=W)

        self.generated_password_textfield =Label(textvariable=self.n_generatedpassword, font=('Book Antiqua', 14,'bold'),border=0,fg='black',bg='white')
        self.generated_password_textfield.place(relx=0.41, rely=0.4, anchor=W)

        self.generate = Button(text="GENERATE PASSWORD", padx=10, pady=1, font=('Georgia', 13, 'bold'),
                               fg='white', bg='green', command=self.generate_pass)
        self.generate.place(relx=0.28, rely=0.52, anchor=W)

        self.copy_to_clipboard = Button(text="COPY TO CLIPBOARD", padx=10, pady=1, border=0,font=('Georgia', 13), fg='white', bg='black', command=self.copy_to_clipboard)
        self.copy_to_clipboard.place(relx=0.31, rely=0.63, anchor=W)

        self.accept = Button(text="ACCEPT", bd=3, padx=10, pady=1, font=('Georgia', 13),
                             bg='#00BFFF',fg='white', command=self.accept_fields)
        self.accept.place(relx=0.28, rely=0.75, anchor=W)

        self.reset = Button(text="RESET", padx=10, pady=1, font=('Georgia', 13,'bold'),
                            bg='RED',fg='white', command=self.reset_fields)
        self.reset.place(relx=0.46, rely=0.75, anchor=W)

    def generate_pass(self):
        name = self.n_username.get()
        leng = self.n_passwordlen.get()
        password = generate_password(leng, complexity_rules)

        self.n_generatedpassword.set(password)

    def copy_to_clipboard(self):
        password = self.n_generatedpassword.get()
        pyperclip.copy(password)
        messagebox.showinfo("Clipboard Copy", "Password copied to clipboard.")

    def accept_fields(self):
        with sqlite3.connect("Account.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM User_Account WHERE Username = ?"
            cursor.execute(find_user, (self.n_username.get(),))

            if cursor.fetchall():
                messagebox.showerror("This username already exists!", "Please use another username")
            else:
                insert = "INSERT INTO User_Account(Username, GeneratedPassword) VALUES(?, ?)"
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password generated and saved successfully")

    def reset_fields(self):
        self.n_username.set('')
        self.n_passwordlen.set('')
        self.n_generatedpassword.set('')

if __name__ == '__main__':
    root = Tk()
    root.configure(bg='white')
    pass_gen = GUI(root)
    root.mainloop()
