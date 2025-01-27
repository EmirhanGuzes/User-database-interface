import tkinter as tk
from tkinter import messagebox, ttk
import database
import re
import phonenumbers

# Email doğrulama fonksiyonu
def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

# Telefon numarası doğrulama fonksiyonu
def is_valid_phone(phone):
    try:
        parsed_number = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False

# Ana pencereyi oluşturma
root = tk.Tk()
root.title("User Interface")

# Kullanıcıları tablo halinde gösterme
tree = ttk.Treeview(root, columns=('ID', 'Username', 'Display Name', 'Phone', 'Email', 'User Role', 'Enable'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Username', text='Username')
tree.heading('Display Name', text='Display Name')
tree.heading('Phone', text='Phone')
tree.heading('Email', text='Email')
tree.heading('User Role', text='User Role')
tree.heading('Enable', text='Enable')
tree.pack()

# Kullanıcıları güncelleme fonksiyonu
def update_user_list():
    show_disabled = show_disabled_var.get()
    users = database.fetch_users(show_disabled)
    for i in tree.get_children():
        tree.delete(i)
    for user in users:
        tree.insert("", "end", values=user)

# Yeni kullanıcı ekleme ekranını açma fonksiyonu
def open_new_user_window():
    new_user_window = tk.Toplevel(root)
    new_user_window.title("Add New User")

    tk.Label(new_user_window, text="Username:").grid(row=0)
    username_entry = tk.Entry(new_user_window)
    username_entry.grid(row=0, column=1)

    tk.Label(new_user_window, text="Display Name:").grid(row=1)
    display_name_entry = tk.Entry(new_user_window)
    display_name_entry.grid(row=1, column=1)

    tk.Label(new_user_window, text="Phone:").grid(row=2)
    phone_entry = tk.Entry(new_user_window)
    phone_entry.grid(row=2, column=1)

    tk.Label(new_user_window, text="Email:").grid(row=3)
    email_entry = tk.Entry(new_user_window)
    email_entry.grid(row=3, column=1)

    tk.Label(new_user_window, text="User Role:").grid(row=4)
    user_role_combobox = ttk.Combobox(new_user_window, values=["guest", "admin", "super admin"])
    user_role_combobox.grid(row=4, column=1)

    tk.Label(new_user_window, text="Enable:").grid(row=5)
    enable_var = tk.BooleanVar()
    enable_checkbox = tk.Checkbutton(new_user_window, variable=enable_var)
    enable_checkbox.grid(row=5, column=1)

    def add_user():
        username = username_entry.get()
        display_name = display_name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        user_role = user_role_combobox.get()
        enable = enable_var.get()

        if not is_valid_email(email):
            messagebox.showwarning("Error", "Invalid email address")
            return

        if not is_valid_phone(phone):
            messagebox.showwarning("Error", "Invalid phone number Please add country code")
            return

        if username and display_name and phone and email and user_role:
            database.insert_user(username, display_name, phone, email, user_role, enable)
            messagebox.showinfo("Success", "User added successfully!")
            update_user_list()
            new_user_window.destroy()
        else:
            messagebox.showwarning("Error", "Please fill in all fields")

    tk.Button(new_user_window, text="Add", command=add_user).grid(row=6, columnspan=2)

# Yeni kullanıcı ekle butonu
tk.Button(root, text="New User", command=open_new_user_window).pack()

# Disable kullanıcıları gizle/göster checkbox
show_disabled_var = tk.BooleanVar()
show_disabled_checkbox = tk.Checkbutton(root, text="Hide disabled users", variable=show_disabled_var, command=update_user_list)
show_disabled_checkbox.pack()

# Kullanıcı listesini güncelle
update_user_list()

# Tkinter ana döngüsünü başlatma
root.mainloop()