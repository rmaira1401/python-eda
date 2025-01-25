import tkinter as tk
from tkinter import ttk, messagebox
from db_hotel import Database
import gui_guests
import gui_reservations
import gui_billing

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x400")

        self.db = Database(password="mySQLroot#24")

        ttk.Label(root, text="Hotel Management System", font=("Helvetica", 18, "bold")).pack(pady=(10,20))
        ttk.Button(root, text="Manage Guests", command=self.guest_management).pack(pady=(10,5))
        ttk.Button(root, text="Manage Reservations", command=self.reservation_management).pack(pady=5)
        ttk.Button(root, text="Manage Billing", command=self.billing_management).pack(pady=(5,10))
        ttk.Button(root, text="Exit", command=self.exit_app).pack(pady=10)

    def guest_management(self):
        gui_guests.GuestManagement(self.db)

    def reservation_management(self):
        gui_reservations.ReservationManagement(self.db)

    def billing_management(self):
        gui_billing.InvoiceManagement(self.db)

    def exit_app(self):
        self.db.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
