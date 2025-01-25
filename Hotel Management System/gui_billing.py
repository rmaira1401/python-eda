import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class InvoiceManagement:
    def __init__(self, db):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("Invoice Management")
        self.window.geometry("600x400")

        ttk.Label(self.window, text="Invoice Management", font=("Helvetica", 16, "bold")).pack(pady=(10,20))
        ttk.Button(self.window, text="Add New Bill", command=self.add_new_bill).pack(pady=(10,5))
        ttk.Button(self.window, text="View All Invoice", command=self.view_invoice).pack(pady=(5,10))
        ttk.Button(self.window, text="Back", command=self.window.destroy).pack(pady=10)

    def add_new_bill(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add New Invoice")

        ttk.Label(add_window, text="Enter Reservation ID:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
        reserveID_entry = ttk.Entry(add_window)
        reserveID_entry.grid(row=0, column=1, padx=10)

        def validate_reserve_id():
            reserveID = reserveID_entry.get()

            if not reserveID:
                messagebox.showerror("Error", "Reservation ID cannot be empty!")
                return

            query_reserve = """
                SELECT r.roomType, r.checkin, r.checkout
                FROM reservations r
                WHERE r.id = %s
            """
            result1 = self.db.fetch_all(query_reserve, (reserveID,))
            if not result1:
                messagebox.showerror("Error", "Reservation not found!")
                return

            query_bill = """
                SELECT * FROM billing where reserveID = %s
            """
            result2 = self.db.fetch_all(query_bill, (reserveID,))
            if result2:
                messagebox.showwarning("Warning", f"Bill already exists for Reservation ID *{reserveID}*")
                return

            show_additional_fields(reserveID, result1)

        def show_additional_fields(reserveID, result1):
            ttk.Label(add_window, text="Days Stayed:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Total Cost:").grid(row=3, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Date of Bill:").grid(row=4, column=0, pady=5, padx=10, sticky="w")

            room_type, check_in, check_out = result1[0]
            price_per_day = {"Single": 50, "Double": 100, "Triple": 150, "Quad": 200}.get(room_type, 0)
            total_days = (check_out - check_in).days
            total_amount = price_per_day * total_days
            billDate = datetime.now().strftime("%Y-%m-%d")

            days_entry = ttk.Entry(add_window)
            totalcost_entry = ttk.Entry(add_window)
            date_entry = ttk.Entry(add_window)

            days_entry.insert(0, total_days)
            totalcost_entry.insert(0, total_amount)
            date_entry.insert(0, billDate)
            
            days_entry.config(state='readonly')
            totalcost_entry.config(state='readonly')
            date_entry.config(state='readonly')

            days_entry.grid(row=2, column=1)
            totalcost_entry.grid(row=3, column=1)
            date_entry.grid(row=4, column=1)

            def save_bill():
                days_stayed = days_entry.get()
                totalcost = totalcost_entry.get()
                dateofbill = date_entry.get()

                if not (days_stayed and totalcost and dateofbill):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                try:
                    days_stayed = int(days_stayed)
                    totalcost = int(totalcost)
                    query = "INSERT INTO billing (reserveID, days_stayed, totalcost, dateofbill) VALUES (%s, %s, %s, %s)"
                    self.db.execute_query(query, (reserveID, days_stayed, totalcost, dateofbill))
                    messagebox.showinfo("Success", "New Bill Added!")
                    add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(add_window, text="Add", command=save_bill).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(add_window, text="Validate", command=validate_reserve_id).grid(row=1, column=0, columnspan=2, pady=10)

    def view_invoice(self):
        view_window = tk.Toplevel(self.window)
        view_window.title("Invoice List")

        columns = ("Bill ID", "Reservation", "Days Stayed", "Total Cost ($)", "Date of Bill")
        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        query = """
        SELECT b.id, g.name, b.days_stayed, b.totalcost, b.dateofbill
        FROM billing b
        JOIN reservations r ON r.id = b.reserveID
        JOIN guests g ON g.id = r.guestID
        """
        results = self.db.fetch_all(query)
        for bill in results:
            tree.insert("", tk.END, values=bill)

        tree.pack(fill=tk.BOTH, expand=True)
