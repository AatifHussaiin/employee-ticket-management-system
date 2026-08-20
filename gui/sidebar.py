import tkinter as tk

from utils.theme import *


class Sidebar:

    def __init__(self, parent, dashboard):

        self.parent = parent
        self.dashboard = dashboard

        self.create_sidebar()

    # ==========================================
    # CREATE SIDEBAR
    # ==========================================

    def create_sidebar(self):

        self.frame = tk.Frame(
            self.parent,
            bg=SIDEBAR,
            width=240
        )

        self.frame.pack(
            side="left",
            fill="y"
        )

        self.frame.pack_propagate(False)

        # ======================================
        # LOGO
        # ======================================

        tk.Label(
            self.frame,
            text="🏢",
            bg=SIDEBAR,
            fg="white",
            font=("Segoe UI Emoji", 40)
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            self.frame,
            text="Employee Ticket\nManagement",
            bg=SIDEBAR,
            fg="white",
            font=("Segoe UI", 15, "bold"),
            justify="center"
        ).pack(
            pady=(0, 30)
        )

        # ======================================
        # COMMON MENU
        # ======================================

        self.create_button(
            "🏠  Dashboard",
            self.dashboard.show_home
        )

        self.create_button(
            "🎫  Raise Ticket",
            self.dashboard.show_raise_ticket
        )

        self.create_button(
            "📋  My Tickets",
            self.dashboard.show_my_tickets
        )

        self.create_button(
            "👤  Profile",
            self.dashboard.show_profile
        )

        self.create_button(
            "📊  Reports",
            self.dashboard.show_reports
        )

        # ======================================
        # ADMIN MENU
        # ======================================

        if self.dashboard.user.get("role") == "Admin":

            self.create_button(
                "🛠  Admin Panel",
                self.dashboard.show_admin,
                color="#7C3AED"
            )

        # ======================================
        # SPACER
        # ======================================

        tk.Label(
            self.frame,
            bg=SIDEBAR
        ).pack(
            expand=True,
            fill="both"
        )

        # ======================================
        # LOGOUT
        # ======================================

        self.create_button(
            "🚪  Logout",
            self.dashboard.logout,
            color=DANGER
        )

    # ==========================================
    # CREATE BUTTON
    # ==========================================

    def create_button(
        self,
        text,
        command,
        color=PRIMARY
    ):

        btn = tk.Button(
            self.frame,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground="#2563EB",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=20,
            font=BUTTON_FONT
        )

        btn.pack(
            fill="x",
            padx=15,
            pady=6,
            ipady=8
        )