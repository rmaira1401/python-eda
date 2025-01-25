import tkinter as tk
from tkinter import ttk, messagebox

class GuestManagement:
    def __init__(self, db):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("Guest Management")
        self.window.geometry("600x400")

        ttk.Label(self.window, text="Guest Management", font=("Helvetica", 16, "bold")).pack(pady=(10,20))
        ttk.Button(self.window, text="Add New Guest", command=self.add_new_guest).pack(pady=(10,5))
        ttk.Button(self.window, text="View Guests", command=self.view_guests).pack(pady=5)
        ttk.Button(self.window, text="Delete Guest", command=self.delete_guest).pack(pady=(5,10))
        ttk.Button(self.window, text="Back", command=self.window.destroy).pack(pady=10)

    def add_new_guest(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add New Guest")
        ttk.Label(add_window, text="Name:").grid(row=0, column=0, pady=5, padx=10)
        ttk.Label(add_window, text="CNIC:").grid(row=1, column=0, pady=5, padx=10)
        ttk.Label(add_window, text="Phone:").grid(row=2, column=0, pady=5, padx=10)
        ttk.Label(add_window, text="Email:").grid(row=3, column=0, pady=5, padx=10)

        name_entry = ttk.Entry(add_window)
        cnic_entry = ttk.Entry(add_window)
        phone_entry = ttk.Entry(add_window)
        email_entry = ttk.Entry(add_window)

        name_entry.grid(row=0, column=1, pady=5, padx=10)
        cnic_entry.grid(row=1, column=1, pady=5, padx=10)
        phone_entry.grid(row=2, column=1, pady=5, padx=10)
        email_entry.grid(row=3, column=1, pady=5, padx=10)

        def save_guest():
            name = name_entry.get().title()
            cnic = cnic_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            if not (name and cnic and phone and email):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                query = "INSERT INTO guests(name, cnic, phone, email) VALUES(%s, %s, %s, %s)"
                self.db.execute_query(query, (name, cnic, phone, email))
                messagebox.showinfo("Success", "New Guest Added!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(add_window, text="Save", command=save_guest).grid(row=4, column=0, columnspan=2, pady=20)

    def view_guests(self):
        view_window = tk.Toplevel(self.window)
        view_window.title("Guests List")

        columns = ("Guest ID", "Name", "CNIC", "Phone", "Email")
        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        query = "SELECT * FROM guests"
        results = self.db.fetch_all(query)
        for guest in results:
            tree.insert("", tk.END, values=guest)

        tree.pack(fill=tk.BOTH, expand=True)

    def delete_guest(self):
        delete_window = tk.Toplevel(self.window)
        delete_window.title("Delete Guest")
        ttk.Label(delete_window, text="Enter Guest ID:").grid(row=0, column=0, pady=10, padx=20)

        guest_id_entry = ttk.Entry(delete_window)
        guest_id_entry.grid(row=0, column=1)

        def delete():
            guest_id = guest_id_entry.get()
            if not guest_id.isdigit():
                messagebox.showerror("Error", "Invalid ID!")
                return

            check_query = "SELECT * FROM guests WHERE id = %s"
            guest = self.db.fetch_all(check_query, (guest_id,))
            if not guest:
                messagebox.showerror("Error", f"No guest found with ID {guest_id}.")
                return

            sure = messagebox.askyesno("Deleting record", f"Are you sure you want to delete guest record with ID {guest_id}?")
            if sure == "yes":
                try:
                    query = "DELETE FROM guests WHERE id = %s"
                    self.db.execute_query(query, (guest_id,))
                    messagebox.showinfo("Success", f"Guest with ID {guest_id} deleted.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                    delete_window.destroy()


        ttk.Button(delete_window, text="Delete Record", command=delete).grid(row=1, column=0, columnspan=2, pady=20)
