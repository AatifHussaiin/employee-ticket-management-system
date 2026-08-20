import tkinter as tk
from tkinter import messagebox

from gui.register import RegisterWindow
from gui.dashboard import Dashboard
from models.user import User


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Employee Ticket Management System")
        self.root.geometry("950x550")
        self.root.configure(bg="#F4F6F9")
        self.root.resizable(False, False)

        self.password_visible = False

        self.center_window()
        self.create_widgets()

    # ==========================================
    # CENTER WINDOW
    # ==========================================

    def center_window(self):

        width = 950
        height = 550

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ==========================================
    # CREATE LOGIN UI
    # ==========================================

    def create_widgets(self):

        # ======================================
        # LEFT PANEL
        # ======================================

        left = tk.Frame(
            self.root,
            bg="#0F4C81",
            width=350
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="🏢",
            font=("Segoe UI Emoji", 48),
            bg="#0F4C81",
            fg="white"
        ).pack(
            pady=(60, 10)
        )

        tk.Label(
            left,
            text="Employee\nTicket System",
            font=("Segoe UI", 24, "bold"),
            bg="#0F4C81",
            fg="white",
            justify="center"
        ).pack()

        tk.Label(
            left,
            text="IT Help Desk Portal\n"
                 "Raise and Track Tickets Easily",
            font=("Segoe UI", 12),
            bg="#0F4C81",
            fg="white",
            justify="center"
        ).pack(
            pady=20
        )

        # ======================================
        # RIGHT PANEL
        # ======================================

        right = tk.Frame(
            self.root,
            bg="white"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            right,
            text="Welcome Back",
            font=("Segoe UI", 24, "bold"),
            bg="white"
        ).pack(
            pady=(60, 15)
        )

        # Employee ID

        tk.Label(
            right,
            text="Employee ID",
            bg="white",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            padx=70
        )

        self.emp_entry = tk.Entry(
            right,
            font=("Segoe UI", 12)
        )

        self.emp_entry.pack(
            fill="x",
            padx=70,
            ipady=6,
            pady=(5, 20)
        )

        # Password

        tk.Label(
            right,
            text="Password",
            bg="white",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            padx=70
        )

        self.pass_entry = tk.Entry(
            right,
            show="*",
            font=("Segoe UI", 12)
        )

        self.pass_entry.pack(
            fill="x",
            padx=70,
            ipady=6
        )

        # Show Password

        self.show_btn = tk.Button(
            right,
            text="Show Password",
            command=self.toggle_password
        )

        self.show_btn.pack(
            anchor="e",
            padx=70,
            pady=10
        )

        # Login

        tk.Button(
            right,
            text="Login",
            bg="#0F4C81",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=self.login
        ).pack(
            fill="x",
            padx=70,
            ipady=8,
            pady=10
        )

        # Register

        tk.Button(
            right,
            text="Register",
            bg="#2E8B57",
            fg="white",
            font=("Segoe UI", 11),
            cursor="hand2",
            command=self.register
        ).pack(
            fill="x",
            padx=70,
            ipady=8
        )

        # Exit

        tk.Button(
            right,
            text="Exit",
            bg="#C0392B",
            fg="white",
            font=("Segoe UI", 11),
            cursor="hand2",
            command=self.root.destroy
        ).pack(
            fill="x",
            padx=70,
            ipady=8,
            pady=15
        )

        self.emp_entry.focus_set()

    # ==========================================
    # SHOW / HIDE PASSWORD
    # ==========================================

    def toggle_password(self):

        if self.password_visible:

            self.pass_entry.config(
                show="*"
            )

            self.show_btn.config(
                text="Show Password"
            )

            self.password_visible = False

        else:

            self.pass_entry.config(
                show=""
            )

            self.show_btn.config(
                text="Hide Password"
            )

            self.password_visible = True

    # ==========================================
    # LOGIN
    # ==========================================

    def login(self):

        employee_id = self.emp_entry.get().strip()
        password = self.pass_entry.get()

        if employee_id == "" or password == "":

            messagebox.showerror(
                "Error",
                "Please enter Employee ID and Password."
            )

            return

        user = User.login(
            employee_id,
            password
        )

        if user:

            self.root.destroy()

            dashboard_root = tk.Tk()

            Dashboard(
                dashboard_root,
                user
            )

            dashboard_root.mainloop()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Employee ID or Password."
            )

    # ==========================================
    # SHOW LOGIN
    # ==========================================

    def show_login(self):

        self.root.deiconify()

    # ==========================================
    # REGISTER
    # ==========================================

    def register(self):

        self.root.withdraw()

        RegisterWindow(
            self.root,
            self.show_login
        )