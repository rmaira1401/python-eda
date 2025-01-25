import tkinter as tk
from tkinter import ttk, messagebox, IntVar
from datetime import datetime
from tkcalendar import DateEntry

class ReservationManagement:
    def __init__(self, db):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("Reservation Management")
        self.window.geometry("600x400")

        ttk.Label(self.window, text="Reservation Management", font=("Helvetica", 16, "bold")).pack(pady=(10,20))
        ttk.Button(self.window, text="Add New Reservation", command=self.add_new_reservation).pack(pady=(10,5))
        ttk.Button(self.window, text="Update Reservation", command=self.update_reservation).pack(pady=(10,5))
        ttk.Button(self.window, text="Cancel Reservation", command=self.cancel_reservation).pack(pady=(10,5))
        ttk.Button(self.window, text="View All Reservations", command=self.view_reservation).pack(pady=(5,10))
        ttk.Button(self.window, text="Back", command=self.window.destroy).pack(pady=10)

    def add_new_reservation(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add New Reservation")

        ttk.Label(add_window, text="Enter Guest ID:").grid(row=0, column=0, pady=5, padx=10)
        guestID_entry = ttk.Entry(add_window)
        guestID_entry.grid(row=0, column=1, padx=10)

        def validate_guest_id():
            guestID = guestID_entry.get()

            if not guestID:
                messagebox.showerror("Error", "Guest ID cannot be empty!")
                return

            result1 = self.db.fetch_all("""
                SELECT g.id, g.name FROM guests g WHERE g.id = %s
            """, (guestID,))

            if not result1:
                messagebox.showerror("Error", "Guest not found!")
                return

            result2 = self.db.fetch_all("""
                SELECT * FROM reservations WHERE guestID = %s
            """, (guestID,))
            if result2:
                messagebox.showwarning("Warning", f"Reservation already exists for Guest ID *{guestID}*")
                return

            show_additional_fields(guestID)

        def show_additional_fields(guestID):
            ttk.Label(add_window, text="Room Type:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Number of Guests:").grid(row=3, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Number of Rooms:").grid(row=4, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Check-In Date:").grid(row=5, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Check-Out Date:").grid(row=6, column=0, pady=5, padx=10, sticky="w")
            ttk.Label(add_window, text="Status:").grid(row=7, column=0, pady=5, padx=10, sticky="w")

            roomtype_var = tk.StringVar(value="Select Room Type")
            room_options = ["Single", "Double", "Triple", "Quad"]
            roomtype_entry = ttk.OptionMenu(add_window, roomtype_var, *room_options)

            totalguests_var = IntVar(value=1)
            totalrooms_var = IntVar(value=1)
            totalguests_entry = ttk.Spinbox(add_window, from_=1, to=30, textvariable=totalguests_var)
            totalrooms_entry = ttk.Spinbox(add_window, from_=1, to=30, textvariable=totalrooms_var)

            checkin_entry = DateEntry(add_window, date_pattern='mm/dd/yy')
            checkout_entry = DateEntry(add_window, date_pattern='mm/dd/yy')
            status_var = tk.StringVar(value="Select Status")
            status_options = ["Confirmed", "Not Confirmed", "Completed"]
            status_entry = ttk.OptionMenu(add_window, status_var, *status_options)

            roomtype_entry.grid(row=2, column=1, padx=10)
            totalguests_entry.grid(row=3, column=1, padx=10)
            totalrooms_entry.grid(row=4, column=1, padx=10)
            checkin_entry.grid(row=5, column=1, padx=10)
            checkout_entry.grid(row=6, column=1, padx=10)
            status_entry.grid(row=7, column=1, padx=10)

            def save_reservation():
                roomType = roomtype_var.get().capitalize()
                totalguests = totalguests_var.get()
                totalrooms = totalrooms_var.get()
                checkin = checkin_entry.get()
                checkout = checkout_entry.get()
                status = status_var.get()

                if not (roomType and totalguests and totalrooms and checkin and checkout and status):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                try:
                    checkin = datetime.strptime(checkin, '%m/%d/%y').strftime('%Y-%m-%d')
                    checkout = datetime.strptime(checkout, '%m/%d/%y').strftime('%Y-%m-%d')
                    dateofreserve = datetime.now().strftime("%Y-%m-%d")

                    query = """
                        INSERT INTO reservations
                        (guestID, roomType, numberofguests, numberofrooms, checkin, checkout, status, dateofreserve)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    self.db.execute_query(query, (guestID, roomType, totalguests, totalrooms, checkin, checkout, status, dateofreserve))
                    messagebox.showinfo("Success", "New Reservation Added!")
                    add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(add_window, text="Save Reservation", command=save_reservation).grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(add_window, text="Validate", command=validate_guest_id).grid(row=1, column=0, columnspan=2, pady=10)


    def update_reservation(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Update Reservation")

        ttk.Label(update_window, text="Enter Reservation ID to update:").grid(row=0, column=0, pady=5, padx=10)
        reserveID_entry = ttk.Entry(update_window)
        reserveID_entry.grid(row=0, column=1, pady=5, padx=10)

        def validate_reserve_id():
            reserveID = reserveID_entry.get()

            if not reserveID:
                messagebox.showerror("Error", "Reservation ID cannot be empty.")
                return

            # Fetch reservation details
            result = self.db.fetch_all("SELECT roomType, numberofguests, numberofrooms, checkin, checkout, status FROM reservations WHERE id = %s", (reserveID,))
            if not result:
                messagebox.showerror("Error", f"Reservation with ID {reserveID} not found.")
                return

            # Pass the fetched data to the show_fields function
            show_fields(reserveID, result[0])

        def show_fields(reserveID, reservation_data):
            ttk.Label(update_window, text="Room Type:").grid(row=2, column=0, pady=5, padx=10)
            ttk.Label(update_window, text="Number of Guests:").grid(row=3, column=0, pady=5, padx=10)
            ttk.Label(update_window, text="Number of Rooms:").grid(row=4, column=0, pady=5, padx=10)
            ttk.Label(update_window, text="Check-In Date:").grid(row=5, column=0, pady=5, padx=10)
            ttk.Label(update_window, text="Check-Out Date:").grid(row=6, column=0, pady=5, padx=10)
            ttk.Label(update_window, text="Status:").grid(row=7, column=0, pady=5, padx=10)

            # Unpack fetched data
            roomType, numberofguests, numberofrooms, checkin, checkout, status = reservation_data

            # Room Type Dropdown
            roomtype_var = tk.StringVar(value=roomType)  # Set the default value
            room_options = ["Single", "Double", "Triple", "Quad"]
            roomtype_entry = ttk.OptionMenu(update_window, roomtype_var, roomType, *room_options)

            # Number of Guests and Rooms
            totalguests_var = tk.IntVar(value=numberofguests)
            totalrooms_var = tk.IntVar(value=numberofrooms)
            totalguests_entry = ttk.Spinbox(update_window, from_=1, to=30, textvariable=totalguests_var)
            totalrooms_entry = ttk.Spinbox(update_window, from_=1, to=30, textvariable=totalrooms_var)

            checkin_entry = DateEntry(update_window, date_pattern='mm/dd/yy')
            checkout_entry = DateEntry(update_window, date_pattern='mm/dd/yy')
            checkin_entry.set_date(checkin)
            checkout_entry.set_date(checkout)

            # Status Dropdown
            status_var = tk.StringVar(value=status)  # Set default value
            status_options = ["Confirmed", "Not Confirmed", "Completed"]
            status_entry = ttk.OptionMenu(update_window, status_var, status, *status_options)

            # Place the widgets
            roomtype_entry.grid(row=2, column=1, padx=10)
            totalguests_entry.grid(row=3, column=1, padx=10)
            totalrooms_entry.grid(row=4, column=1, padx=10)
            checkin_entry.grid(row=5, column=1, padx=10)
            checkout_entry.grid(row=6, column=1, padx=10)
            status_entry.grid(row=7, column=1, padx=10)

            def update_reserve():
                # Fetch updated values
                roomType = roomtype_var.get()
                totalguests = totalguests_var.get()
                totalrooms = totalrooms_var.get()
                checkin = checkin_entry.get_date().strftime('%Y-%m-%d')  # Retrieve and format date
                checkout = checkout_entry.get_date().strftime('%Y-%m-%d')  # Retrieve and format date
                status = status_var.get()

                # Validation
                if not all([roomType, totalguests, totalrooms, checkin, checkout, status]):
                    messagebox.showwarning("Warning", "Fields cannot be empty!")
                    return

                try:
                    # Update the database
                    self.db.execute_query(
                        "UPDATE reservations SET roomType = %s, numberofguests = %s, numberofrooms = %s, "
                        "checkin = %s, checkout = %s, status = %s WHERE id = %s",
                        (roomType, totalguests, totalrooms, checkin, checkout, status, reserveID)
                    )
                    messagebox.showinfo("Success", "Reservation updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update reservation: {str(e)}")

            ttk.Button(update_window, text="Update Reservation", command=update_reserve).grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(update_window, text="Validate", command=validate_reserve_id).grid(row=1, column=0, columnspan=2, pady=10)

    def cancel_reservation(self):
        cancel_window = tk.Toplevel(self.window)
        cancel_window.title("Cancel Reservation")

        ttk.Label(cancel_window, text="Enter Reservation ID to cancel:").grid(row=0, column=0, pady=5, padx=10)
        reserveID_entry = ttk.Entry(cancel_window)
        reserveID_entry.grid(row=0, column=1, pady=5, padx=10)

        def cancel_reserve():
            reserveID = reserveID_entry.get()

            if not reserveID:
                messagebox.showerror("Error", "Reservation ID cannot be empty!")
                return

            result = self.db.fetch_all("""
                SELECT * FROM reservations WHERE id = %s
            """, (reserveID,))

            if not result:
                messagebox.showerror("Error", f"Reservation with ID {reserveID} not found.")
                return

            try:
                query = "UPDATE reservations SET status = 'Cancelled' WHERE id = %s"
                self.db.execute_query(query, (reserveID,))
                messagebox.showinfo("Success", f"Reservation with ID {reserveID} has been cancelled.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(cancel_window, text="Cancel Reservation Now", command=cancel_reserve).grid(row=1, column=0, columnspan=2, pady=10)



    def view_reservation(self):
        view_window = tk.Toplevel(self.window)
        view_window.title("Reservations List")

        columns = ("Reservation ID", "Guest", "Room Type", "Total Guests", "Total Rooms", "Check-In Date", "Check-Out Date", "Status", "Date")
        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        query = """
        SELECT r.id, g.name, r.roomType, r.numberofguests, r.numberofrooms, r.checkin, r.checkout, r.status, r.dateofreserve
        FROM reservations r
        JOIN guests g ON g.id = r.guestID
        """
        results = self.db.fetch_all(query)
        for bill in results:
            tree.insert("", tk.END, values=bill)

        tree.pack(fill=tk.BOTH, expand=True)
