import tkinter as tk
from tkinter import messagebox

from models.user import User
from utils.auth import hash_password


class RegisterWindow:

    def __init__(self, root, login_callback):
        self.root = root
        self.login_callback = login_callback

        self.window = tk.Toplevel(root)
        self.window.title("Employee Registration")
        self.window.geometry("500x650")
        self.window.resizable(False, False)
        self.window.configure(bg="#f5f7fa")

        title = tk.Label(
            self.window,
            text="Employee Registration",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f7fa",
            fg="#1f4e79"
        )
        title.pack(pady=20)

        self.entries = {}

        fields = [
            "Full Name",
            "Employee ID",
            "Email",
            "Department",
            "Password",
            "Confirm Password"
        ]

        for field in fields:

            frame = tk.Frame(self.window, bg="#f5f7fa")
            frame.pack(fill="x", padx=40, pady=8)

            tk.Label(
                frame,
                text=field,
                font=("Segoe UI", 11),
                bg="#f5f7fa"
            ).pack(anchor="w")

            show = "*" if "Password" in field else ""

            entry = tk.Entry(
                frame,
                font=("Segoe UI", 11),
                show=show
            )

            entry.pack(fill="x", ipady=6)

            self.entries[field] = entry

        tk.Button(
            self.window,
            text="Register",
            font=("Segoe UI", 12, "bold"),
            bg="#0078D7",
            fg="white",
            command=self.register_user
        ).pack(pady=20, ipadx=15, ipady=5)

        tk.Button(
            self.window,
            text="Back to Login",
            font=("Segoe UI", 11),
            command=self.back
        ).pack()

    def register_user(self):

        full_name = self.entries["Full Name"].get().strip()
        employee_id = self.entries["Employee ID"].get().strip()
        email = self.entries["Email"].get().strip()
        department = self.entries["Department"].get().strip()
        password = self.entries["Password"].get()
        confirm_password = self.entries["Confirm Password"].get()

        if not all([
            full_name,
            employee_id,
            email,
            department,
            password,
            confirm_password
        ]):
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        if password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
            return

        if User.employee_exists(employee_id):
            messagebox.showerror(
                "Error",
                "Employee ID already exists."
            )
            return

        if User.email_exists(email):
            messagebox.showerror(
                "Error",
                "Email already exists."
            )
            return

        hashed_password = hash_password(password)

        try:

            User.register((
                employee_id,
                full_name,
                email,
                department,
                hashed_password
            ))

            messagebox.showinfo(
                "Success",
                "Registration Successful!"
            )

            self.back()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def back(self):

        self.window.destroy()

        self.login_callback()