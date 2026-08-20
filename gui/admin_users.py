import tkinter as tk
from tkinter import ttk, messagebox

from models.user import User
from utils.theme import *


class AdminUsersPage:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user

        self.create_page()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_page(self):

        self.outer = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        self.outer.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # TITLE
        # ======================================

        title_frame = tk.Frame(
            self.outer,
            bg=BACKGROUND
        )

        title_frame.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        tk.Label(
            title_frame,
            text="Employee Management",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(side="left")

        tk.Label(
            title_frame,
            text="Manage registered employees",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            side="right",
            pady=8
        )

        # ======================================
        # SEARCH BAR
        # ======================================

        search_frame = tk.Frame(
            self.outer,
            bg="white",
            bd=1,
            relief="solid"
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 15)
        )

        tk.Label(
            search_frame,
            text="Search:",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(15, 5),
            pady=15
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            width=30
        )

        self.search_entry.pack(
            side="left",
            ipady=5
        )

        tk.Button(
            search_frame,
            text="Search",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.search_users
        ).pack(
            side="left",
            padx=15,
            ipadx=10,
            ipady=4
        )

        tk.Button(
            search_frame,
            text="Reset",
            bg="#64748B",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.reset_search
        ).pack(
            side="left",
            padx=5,
            ipadx=10,
            ipady=4
        )

        tk.Button(
            search_frame,
            text="Refresh",
            bg=SUCCESS,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.load_users
        ).pack(
            side="right",
            padx=15,
            ipadx=10,
            ipady=4
        )

        # ======================================
        # USER TABLE
        # ======================================

        table_container = tk.Frame(
            self.outer,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

        header = tk.Frame(
            table_container,
            bg="white"
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="Registered Employees",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        self.count_label = tk.Label(
            header,
            text="",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        )

        self.count_label.pack(
            side="right",
            padx=20
        )

        table_frame = tk.Frame(
            table_container,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columns = (
            "employee_id",
            "full_name",
            "email",
            "department",
            "role",
            "created_at"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "employee_id": "Employee ID",
            "full_name": "Full Name",
            "email": "Email",
            "department": "Department",
            "role": "Role",
            "created_at": "Registered"
        }

        widths = {
            "employee_id": 120,
            "full_name": 180,
            "email": 260,
            "department": 150,
            "role": 100,
            "created_at": 160
        }

        for column in columns:

            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.column(
            "full_name",
            anchor="w"
        )

        self.table.column(
            "email",
            anchor="w"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ======================================
        # DOUBLE CLICK
        # ======================================

        self.table.bind(
            "<Double-1>",
            self.show_user_details
        )

        # ======================================
        # DELETE BUTTON
        # ======================================

        button_frame = tk.Frame(
            table_container,
            bg="white"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        tk.Button(
            button_frame,
            text="Delete Selected Employee",
            bg=DANGER,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.delete_selected_user
        ).pack(
            side="right",
            ipadx=10,
            ipady=5
        )

        # ======================================
        # LOAD USERS
        # ======================================

        self.load_users()

    # ==========================================
    # LOAD USERS
    # ==========================================

    def load_users(self):

        try:

            users = User.get_all_users()

            self.display_users(users)

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load employees.\n\n{error}"
            )

    # ==========================================
    # DISPLAY USERS
    # ==========================================

    def display_users(self, users):

        for item in self.table.get_children():

            self.table.delete(item)

        for user in users:

            self.table.insert(
                "",
                "end",
                values=(
                    user[0],
                    user[1],
                    user[2],
                    user[3],
                    user[4],
                    user[5]
                )
            )

        self.count_label.config(
            text=f"{len(users)} employee(s)"
        )

        if not users:

            self.table.insert(
                "",
                "end",
                values=(
                    "",
                    "No employees found.",
                    "",
                    "",
                    "",
                    ""
                )
            )

    # ==========================================
    # SEARCH USERS
    # ==========================================

    def search_users(self):

        search_text = self.search_entry.get().strip()

        try:

            users = User.search_users(
                search_text
            )

            self.display_users(users)

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                f"Unable to search employees.\n\n{error}"
            )

    # ==========================================
    # RESET SEARCH
    # ==========================================

    def reset_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.load_users()

    # ==========================================
    # DELETE USER
    # ==========================================

    def delete_selected_user(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an employee first."
            )

            return

        item = self.table.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values or not values[0]:

            return

        employee_id = values[0]
        full_name = values[1]
        role = values[4]

        # Prevent accidental admin deletion

        if role == "Admin":

            messagebox.showwarning(
                "Action Not Allowed",
                "Administrator accounts cannot be deleted."
            )

            return

        answer = messagebox.askyesno(
            "Delete Employee",
            f"Are you sure you want to delete:\n\n"
            f"{full_name}\n"
            f"Employee ID: {employee_id}\n\n"
            f"This action cannot be undone."
        )

        if not answer:

            return

        try:

            deleted = User.delete_user(
                employee_id
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Employee deleted successfully."
                )

                self.load_users()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to delete employee."
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to delete employee.\n\n{error}"
            )

    # ==========================================
    # USER DETAILS
    # ==========================================

    def show_user_details(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values or not values[0]:
            return

        window = tk.Toplevel(
            self.parent
        )

        window.title(
            "Employee Details"
        )

        window.geometry(
            "500x450"
        )

        window.configure(
            bg=BACKGROUND
        )

        window.transient(
            self.parent
        )

        tk.Label(
            window,
            text="Employee Details",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(25, 20)
        )

        card = tk.Frame(
            window,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        details = [
            ("Employee ID", values[0]),
            ("Full Name", values[1]),
            ("Email", values[2]),
            ("Department", values[3]),
            ("Role", values[4]),
            ("Registered", values[5])
        ]

        for label, value in details:

            row = tk.Frame(
                card,
                bg="white"
            )

            row.pack(
                fill="x",
                padx=25,
                pady=10
            )

            tk.Label(
                row,
                text=label,
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                width=15,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=value,
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10),
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        tk.Button(
            card,
            text="Close",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=window.destroy
        ).pack(
            pady=20,
            ipadx=20,
            ipady=5
        )