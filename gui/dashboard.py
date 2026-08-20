import tkinter as tk
from tkinter import ttk, messagebox

from gui.reports import ReportsPage
from gui.admin import AdminPage
from utils.theme import *
from gui.sidebar import Sidebar
from gui.raise_ticket import RaiseTicketPage
from gui.my_tickets import MyTicketsPage
from gui.profile import ProfilePage
from models.ticket import Ticket


class Dashboard:

    def __init__(self, root, user):

        self.root = root
        self.user = user

        self.employee_id = user["employee_id"]
        self.employee_name = user["full_name"]
        self.role = user.get("role", "Employee")

        self.root.title(
            "Employee Ticket Management System"
        )

        self.root.state("zoomed")

        self.root.configure(
            bg=BACKGROUND
        )

        self.create_layout()

    # ==========================================
    # MAIN LAYOUT
    # ==========================================

    def create_layout(self):

        self.header = tk.Frame(
            self.root,
            bg=PRIMARY,
            height=65
        )

        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(False)

        tk.Label(
            self.header,
            text="Employee Ticket Management System",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(
            side="left",
            padx=25
        )

        self.user_label = tk.Label(
            self.header,
            text=f"👤 {self.employee_name}  |  {self.role}",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 12)
        )

        self.user_label.pack(
            side="right",
            padx=25
        )

        # ======================================
        # BODY
        # ======================================

        self.body = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.body.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # SIDEBAR
        # ======================================

        Sidebar(
            self.body,
            self
        )

        # ======================================
        # CONTENT
        # ======================================

        self.content = tk.Frame(
            self.body,
            bg=BACKGROUND
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_home()

    # ==========================================
    # CLEAR CONTENT
    # ==========================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    # ==========================================
    # HOME
    # ==========================================

    def show_home(self):

        self.clear_content()

        container = tk.Frame(
            self.content,
            bg=BACKGROUND
        )

        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        tk.Label(
            container,
            text=f"Welcome Back, {self.employee_name}",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            container,
            text="Here is an overview of your support tickets.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        try:

            counts = Ticket.get_dashboard_counts(
                self.employee_id
            )

        except Exception:

            counts = {
                "total": 0,
                "open": 0,
                "pending": 0,
                "resolved": 0,
                "high_priority": 0
            }

        # ======================================
        # CARDS
        # ======================================

        cards = tk.Frame(
            container,
            bg=BACKGROUND
        )

        cards.pack(
            fill="x"
        )

        for i in range(4):

            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_card(
            cards,
            "Open Tickets",
            counts.get("open", 0),
            PRIMARY,
            0
        )

        self.create_card(
            cards,
            "Pending",
            counts.get("pending", 0),
            WARNING,
            1
        )

        self.create_card(
            cards,
            "Resolved",
            counts.get("resolved", 0),
            SUCCESS,
            2
        )

        self.create_card(
            cards,
            "High Priority",
            counts.get("high_priority", 0),
            DANGER,
            3
        )

        # ======================================
        # RECENT TICKETS
        # ======================================

        recent = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid"
        )

        recent.pack(
            fill="both",
            expand=True,
            pady=(30, 0)
        )

        header = tk.Frame(
            recent,
            bg="white"
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="Recent Tickets",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=18
        )

        tk.Button(
            header,
            text="View All",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=self.show_my_tickets
        ).pack(
            side="right",
            padx=20
        )

        table_frame = tk.Frame(
            recent,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columns = (
            "ticket_id",
            "subject",
            "priority",
            "status",
            "created_at"
        )

        self.recent_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "ticket_id": "Ticket ID",
            "subject": "Subject",
            "priority": "Priority",
            "status": "Status",
            "created_at": "Created Date"
        }

        widths = {
            "ticket_id": 130,
            "subject": 350,
            "priority": 120,
            "status": 120,
            "created_at": 180
        }

        for column in columns:

            self.recent_table.heading(
                column,
                text=headings[column]
            )

            self.recent_table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.recent_table.column(
            "subject",
            anchor="w"
        )

        self.recent_table.pack(
            fill="both",
            expand=True
        )

        self.load_recent_tickets()

    # ==========================================
    # DASHBOARD CARD
    # ==========================================

    def create_card(
        self,
        parent,
        title,
        value,
        color,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=125,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        card.grid_propagate(False)

        tk.Frame(
            card,
            bg=color,
            width=6
        ).pack(
            side="left",
            fill="y"
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            card,
            text=str(value),
            bg="white",
            fg=color,
            font=("Segoe UI", 25, "bold")
        ).pack()

    # ==========================================
    # LOAD RECENT TICKETS
    # ==========================================

    def load_recent_tickets(self):

        for item in self.recent_table.get_children():

            self.recent_table.delete(item)

        try:

            tickets = Ticket.get_recent_tickets(
                self.employee_id,
                5
            )

            for ticket in tickets:

                self.recent_table.insert(
                    "",
                    "end",
                    values=(
                        ticket[0],
                        ticket[1],
                        ticket[3],
                        ticket[4],
                        ticket[5]
                    )
                )

            if not tickets:

                self.recent_table.insert(
                    "",
                    "end",
                    values=(
                        "",
                        "No tickets created yet.",
                        "",
                        "",
                        ""
                    )
                )

        except Exception:

            self.recent_table.insert(
                "",
                "end",
                values=(
                    "",
                    "Unable to load tickets.",
                    "",
                    "",
                    ""
                )
            )

    # ==========================================
    # RAISE TICKET
    # ==========================================

    def show_raise_ticket(self):

        self.clear_content()

        RaiseTicketPage(
            self.content,
            self.employee_id,
            self.show_home
        )

    # ==========================================
    # MY TICKETS
    # ==========================================

    def show_my_tickets(self):

        self.clear_content()

        MyTicketsPage(
            self.content,
            self.employee_id
        )

    # ==========================================
    # PROFILE
    # ==========================================

    def show_profile(self):

        self.clear_content()

        ProfilePage(
            self.content,
            self.user
        )

    # ==========================================
    # REPORTS
    # ==========================================

    def show_reports(self):

        self.clear_content()

        ReportsPage(
            self.content,
            self.employee_id
        )

    # ==========================================
    # ADMIN PANEL
    # ==========================================

    def show_admin(self):

        if self.role != "Admin":

            messagebox.showerror(
                "Access Denied",
                "You do not have permission to access the Admin Panel."
            )

            return

        self.clear_content()

        AdminPage(
            self.content,
            self.user
        )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:

            self.root.destroy()

            import main

            main.start_application()