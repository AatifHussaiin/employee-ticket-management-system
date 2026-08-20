import tkinter as tk
from tkinter import messagebox

from models.user import User
from utils.theme import *


class ProfilePage:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user

        self.create_page()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_page(self):

        # ======================================
        # OUTER CONTAINER
        # ======================================

        self.outer = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        self.outer.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # CANVAS
        # ======================================

        self.canvas = tk.Canvas(
            self.outer,
            bg=BACKGROUND,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ======================================
        # SCROLLBAR
        # ======================================

        scrollbar = tk.Scrollbar(
            self.outer,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        # ======================================
        # SCROLLABLE FRAME
        # ======================================

        self.container = tk.Frame(
            self.canvas,
            bg=BACKGROUND
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.container,
            anchor="nw"
        )

        # ======================================
        # UPDATE SCROLL REGION
        # ======================================

        self.container.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas_window
        )

        # ======================================
        # MOUSE WHEEL
        # ======================================

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # ======================================
        # BUILD PAGE
        # ======================================

        self.build_content()

    # ==========================================
    # SCROLL REGION
    # ==========================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==========================================
    # RESIZE INNER FRAME
    # ==========================================

    def resize_canvas_window(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # ==========================================
    # MOUSE WHEEL
    # ==========================================

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================
    # BUILD CONTENT
    # ==========================================

    def build_content(self):

        content = tk.Frame(
            self.container,
            bg=BACKGROUND
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=25
        )

        # ======================================
        # PAGE TITLE
        # ======================================

        tk.Label(
            content,
            text="My Profile",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            content,
            text="View and manage your employee account.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(3, 20)
        )

        # ======================================
        # TWO COLUMN AREA
        # ======================================

        columns = tk.Frame(
            content,
            bg=BACKGROUND
        )

        columns.pack(
            fill="x"
        )

        columns.grid_columnconfigure(
            0,
            weight=3
        )

        columns.grid_columnconfigure(
            1,
            weight=2
        )

        # ======================================
        # PROFILE CARD
        # ======================================

        profile_card = tk.Frame(
            columns,
            bg="white",
            bd=1,
            relief="solid"
        )

        profile_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        tk.Label(
            profile_card,
            text="Profile Information",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        tk.Label(
            profile_card,
            text="Update your personal information below.",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        self.create_field(
            profile_card,
            "Employee ID",
            self.user.get("employee_id", ""),
            "employee_id",
            readonly=True
        )

        self.create_field(
            profile_card,
            "Full Name",
            self.user.get("full_name", ""),
            "full_name"
        )

        self.create_field(
            profile_card,
            "Email",
            self.user.get("email", ""),
            "email"
        )

        self.create_field(
            profile_card,
            "Department",
            self.user.get("department", ""),
            "department"
        )

        self.create_field(
            profile_card,
            "Role",
            self.user.get("role", "Employee"),
            "role",
            readonly=True
        )

        tk.Button(
            profile_card,
            text="Save Profile Changes",
            bg=SUCCESS,
            fg="white",
            activebackground="#247A4B",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            width=22,
            command=self.update_profile
        ).pack(
            pady=20
        )

        # ======================================
        # PASSWORD CARD
        # ======================================

        password_card = tk.Frame(
            columns,
            bg="white",
            bd=1,
            relief="solid"
        )

        password_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        tk.Label(
            password_card,
            text="Change Password",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        tk.Label(
            password_card,
            text="Update your account password securely.",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        self.create_password_field(
            password_card,
            "Current Password",
            "current_password"
        )

        self.create_password_field(
            password_card,
            "New Password",
            "new_password"
        )

        self.create_password_field(
            password_card,
            "Confirm Password",
            "confirm_password"
        )

        tk.Label(
            password_card,
            text="Minimum 6 characters",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        tk.Button(
            password_card,
            text="Change Password",
            bg=PRIMARY,
            fg="white",
            activebackground="#0B3A63",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            width=22,
            command=self.change_password
        ).pack(
            pady=15
        )

        # ======================================
        # SECURITY INFORMATION
        # ======================================

        security_frame = tk.Frame(
            password_card,
            bg="#F1F5F9"
        )

        security_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 25)
        )

        tk.Label(
            security_frame,
            text="🔒 Security",
            bg="#F1F5F9",
            fg=PRIMARY,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 3)
        )

        tk.Label(
            security_frame,
            text="Your password is securely stored and\n"
                 "never displayed in plain text.",
            bg="#F1F5F9",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 9),
            justify="left"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )

        # ======================================
        # ACCOUNT INFORMATION
        # ======================================

        account_card = tk.Frame(
            content,
            bg="white",
            bd=1,
            relief="solid"
        )

        account_card.pack(
            fill="x",
            pady=(25, 20)
        )

        tk.Label(
            account_card,
            text="Account Information",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        tk.Label(
            account_card,
            text="Your account is protected by password authentication.",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # ==========================================
    # PROFILE FIELD
    # ==========================================

    def create_field(
        self,
        parent,
        label,
        value,
        attribute,
        readonly=False
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=6
        )

        tk.Label(
            frame,
            text=label,
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
            width=15,
            anchor="w"
        ).pack(
            side="left"
        )

        entry = tk.Entry(
            frame,
            font=("Segoe UI", 10)
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5
        )

        entry.insert(
            0,
            value
        )

        if readonly:

            entry.config(
                state="readonly",
                readonlybackground="#F1F5F9"
            )

        setattr(
            self,
            attribute + "_entry",
            entry
        )

    # ==========================================
    # PASSWORD FIELD
    # ==========================================

    def create_password_field(
        self,
        parent,
        label,
        attribute
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=8
        )

        tk.Label(
            frame,
            text=label,
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        entry = tk.Entry(
            frame,
            show="*",
            font=("Segoe UI", 10)
        )

        entry.pack(
            fill="x",
            ipady=6,
            pady=(4, 0)
        )

        setattr(
            self,
            attribute,
            entry
        )

    # ==========================================
    # UPDATE PROFILE
    # ==========================================

    def update_profile(self):

        full_name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        department = self.department_entry.get().strip()

        if full_name == "":

            messagebox.showerror(
                "Validation Error",
                "Full Name cannot be empty."
            )

            return

        if email == "":

            messagebox.showerror(
                "Validation Error",
                "Email cannot be empty."
            )

            return

        if "@" not in email:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address."
            )

            return

        if department == "":

            messagebox.showerror(
                "Validation Error",
                "Department cannot be empty."
            )

            return

        try:

            updated = User.update_profile(
                self.user["employee_id"],
                full_name,
                email,
                department
            )

            if updated:

                self.user["full_name"] = full_name
                self.user["email"] = email
                self.user["department"] = department

                messagebox.showinfo(
                    "Profile Updated",
                    "Your profile has been updated successfully."
                )

            else:

                messagebox.showerror(
                    "Update Failed",
                    "Unable to update your profile."
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to update profile.\n\n{error}"
            )

    # ==========================================
    # CHANGE PASSWORD
    # ==========================================

    def change_password(self):

        current_password = self.current_password.get()
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        if current_password == "":

            messagebox.showerror(
                "Validation Error",
                "Please enter your current password."
            )

            self.current_password.focus_set()

            return

        if new_password == "":

            messagebox.showerror(
                "Validation Error",
                "Please enter a new password."
            )

            self.new_password.focus_set()

            return

        if len(new_password) < 6:

            messagebox.showerror(
                "Validation Error",
                "New password must contain at least 6 characters."
            )

            self.new_password.focus_set()

            return

        if confirm_password == "":

            messagebox.showerror(
                "Validation Error",
                "Please confirm your new password."
            )

            self.confirm_password.focus_set()

            return

        if new_password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "New passwords do not match."
            )

            self.confirm_password.focus_set()

            return

        if current_password == new_password:

            messagebox.showerror(
                "Password Error",
                "New password must be different from your current password."
            )

            return

        try:

            valid = User.verify_current_password(
                self.user["employee_id"],
                current_password
            )

            if not valid:

                messagebox.showerror(
                    "Password Error",
                    "Current password is incorrect."
                )

                self.current_password.focus_set()

                return

            changed = User.change_password(
                self.user["employee_id"],
                new_password
            )

            if changed:

                self.current_password.delete(
                    0,
                    tk.END
                )

                self.new_password.delete(
                    0,
                    tk.END
                )

                self.confirm_password.delete(
                    0,
                    tk.END
                )

                messagebox.showinfo(
                    "Password Changed",
                    "Your password has been changed successfully."
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to change password."
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to change password.\n\n{error}"
            )