import tkinter as tk
from tkinter import ttk, messagebox

from models.ticket import Ticket
from models.user import User
from utils.theme import *


class AdminPage:

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
            pady=(25, 10)
        )

        tk.Label(
            title_frame,
            text="IT Support Admin Panel",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text=f"Welcome, {self.user.get('full_name', 'Administrator')}",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            side="right",
            pady=8
        )

        # ======================================
        # STATISTICS
        # ======================================

        try:

            counts = Ticket.get_admin_counts()

        except Exception:

            counts = {
                "total": 0,
                "open": 0,
                "pending": 0,
                "resolved": 0,
                "high_priority": 0
            }

        cards = tk.Frame(
            self.outer,
            bg=BACKGROUND
        )

        cards.pack(
            fill="x",
            padx=35,
            pady=10
        )

        for i in range(5):

            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_card(
            cards,
            "Total Tickets",
            counts["total"],
            PRIMARY,
            0
        )

        self.create_card(
            cards,
            "Open",
            counts["open"],
            PRIMARY,
            1
        )

        self.create_card(
            cards,
            "Pending",
            counts["pending"],
            WARNING,
            2
        )

        self.create_card(
            cards,
            "Resolved",
            counts["resolved"],
            SUCCESS,
            3
        )

        self.create_card(
            cards,
            "High Priority",
            counts["high_priority"],
            DANGER,
            4
        )

        # ======================================
        # SEARCH / FILTER BAR
        # ======================================

        filter_frame = tk.Frame(
            self.outer,
            bg="white",
            bd=1,
            relief="solid"
        )

        filter_frame.pack(
            fill="x",
            padx=35,
            pady=(15, 10)
        )

        tk.Label(
            filter_frame,
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
            filter_frame,
            font=("Segoe UI", 10),
            width=25
        )

        self.search_entry.pack(
            side="left",
            ipady=5
        )

        tk.Label(
            filter_frame,
            text="Status:",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.status_filter = ttk.Combobox(
            filter_frame,
            state="readonly",
            values=[
                "All",
                "Open",
                "Pending",
                "Resolved"
            ],
            width=12
        )

        self.status_filter.current(0)

        self.status_filter.pack(
            side="left"
        )

        tk.Label(
            filter_frame,
            text="Priority:",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.priority_filter = ttk.Combobox(
            filter_frame,
            state="readonly",
            values=[
                "All",
                "Low",
                "Medium",
                "High"
            ],
            width=12
        )

        self.priority_filter.current(0)

        self.priority_filter.pack(
            side="left"
        )

        tk.Button(
            filter_frame,
            text="Search",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.search_tickets
        ).pack(
            side="left",
            padx=15,
            ipadx=10,
            ipady=4
        )

        tk.Button(
            filter_frame,
            text="Reset",
            bg="#64748B",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.reset_filters
        ).pack(
            side="left",
            padx=5,
            ipadx=10,
            ipady=4
        )

        tk.Button(
            filter_frame,
            text="Refresh",
            bg=SUCCESS,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.refresh
        ).pack(
            side="right",
            padx=15,
            ipadx=10,
            ipady=4
        )

        # ======================================
        # TICKET TABLE
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

        tk.Label(
            table_container,
            text="All Employee Tickets",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=15
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
            "ticket_id",
            "employee_id",
            "category",
            "subject",
            "priority",
            "status",
            "assigned_to",
            "created_at"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "ticket_id": "Ticket ID",
            "employee_id": "Employee ID",
            "category": "Category",
            "subject": "Subject",
            "priority": "Priority",
            "status": "Status",
            "assigned_to": "Assigned To",
            "created_at": "Created"
        }

        widths = {
            "ticket_id": 120,
            "employee_id": 110,
            "category": 110,
            "subject": 250,
            "priority": 90,
            "status": 100,
            "assigned_to": 120,
            "created_at": 150
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
            "subject",
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
            self.open_ticket
        )

        # ======================================
        # LOAD DATA
        # ======================================

        self.load_tickets()

    # ==========================================
    # CREATE CARD
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
            height=105,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nsew"
        )

        card.grid_propagate(False)

        tk.Frame(
            card,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 9)
        ).pack(
            pady=(18, 2)
        )

        tk.Label(
            card,
            text=str(value),
            bg="white",
            fg=color,
            font=("Segoe UI", 22, "bold")
        ).pack()

    # ==========================================
    # LOAD TICKETS
    # ==========================================

    def load_tickets(
        self,
        tickets=None
    ):

        for item in self.table.get_children():

            self.table.delete(item)

        if tickets is None:

            tickets = Ticket.get_all_tickets()

        for ticket in tickets:

            assigned_to = ""

            if len(ticket) > 7:
                assigned_to = ticket[7]

            self.table.insert(
                "",
                "end",
                values=(
                    ticket[0],
                    ticket[1],
                    ticket[2],
                    ticket[3],
                    ticket[4],
                    ticket[5],
                    assigned_to if assigned_to else "Unassigned",
                    ticket[6]
                )
            )

        if not tickets:

            self.table.insert(
                "",
                "end",
                values=(
                    "",
                    "",
                    "",
                    "No tickets found.",
                    "",
                    "",
                    "",
                    ""
                )
            )

    # ==========================================
    # SEARCH
    # ==========================================

    def search_tickets(self):

        search_text = self.search_entry.get().strip()

        status = self.status_filter.get()

        priority = self.priority_filter.get()

        try:

            tickets = Ticket.search_all_tickets(
                search_text,
                status,
                priority
            )

            self.load_tickets(
                tickets
            )

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                f"Unable to search tickets.\n\n{error}"
            )

    # ==========================================
    # RESET
    # ==========================================

    def reset_filters(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.status_filter.current(0)

        self.priority_filter.current(0)

        self.load_tickets()

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        self.search_tickets()

    # ==========================================
    # OPEN TICKET
    # ==========================================

    def open_ticket(self, event=None):

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

        if not values:
            return

        ticket_id = values[0]

        if not ticket_id:
            return

        self.show_ticket_details(
            ticket_id
        )

    # ==========================================
    # TICKET DETAILS
    # ==========================================

    def show_ticket_details(
        self,
        ticket_id
    ):

        ticket = Ticket.get_ticket(
            ticket_id
        )

        if ticket is None:

            messagebox.showerror(
                "Error",
                "Ticket could not be found."
            )

            return

        window = tk.Toplevel(
            self.parent
        )

        window.title(
            f"Ticket Details - {ticket_id}"
        )

        window.geometry(
            "700x700"
        )

        window.configure(
            bg=BACKGROUND
        )

        window.transient(
            self.parent
        )

        # ======================================
        # TITLE
        # ======================================

        tk.Label(
            window,
            text="Ticket Details",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            window,
            text=ticket_id,
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            pady=(0, 20)
        )

        # ======================================
        # DETAILS CARD
        # ======================================

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
            pady=(0, 25)
        )

        # Database order:
        #
        # 0 id
        # 1 ticket_id
        # 2 employee_id
        # 3 category
        # 4 subject
        # 5 description
        # 6 priority
        # 7 status
        # 8 created_at
        # 9 updated_at
        # 10 assigned_to

        self.create_detail_row(
            card,
            "Employee ID",
            ticket[2]
        )

        self.create_detail_row(
            card,
            "Category",
            ticket[3]
        )

        self.create_detail_row(
            card,
            "Subject",
            ticket[4]
        )

        self.create_detail_row(
            card,
            "Priority",
            ticket[6]
        )

        # ======================================
        # DESCRIPTION
        # ======================================

        tk.Label(
            card,
            text="Description",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        description = tk.Text(
            card,
            height=6,
            font=("Segoe UI", 10),
            wrap="word"
        )

        description.pack(
            fill="x",
            padx=25
        )

        description.insert(
            "1.0",
            ticket[5]
        )

        description.config(
            state="disabled"
        )

        # ======================================
        # ASSIGNMENT
        # ======================================

        assignment_frame = tk.Frame(
            card,
            bg="white"
        )

        assignment_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 5)
        )

        tk.Label(
            assignment_frame,
            text="Assign To",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left"
        )

        self.load_assignment_box(
            assignment_frame,
            ticket_id,
            ticket
        )

        # ======================================
        # STATUS
        # ======================================

        status_frame = tk.Frame(
            card,
            bg="white"
        )

        status_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        tk.Label(
            status_frame,
            text="Status",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left"
        )

        status_box = ttk.Combobox(
            status_frame,
            state="readonly",
            values=[
                "Open",
                "Pending",
                "Resolved"
            ],
            width=15
        )

        status_box.set(
            ticket[7]
        )

        status_box.pack(
            side="left",
            padx=15
        )

        # ======================================
        # SAVE STATUS
        # ======================================

        def save_status():

            new_status = status_box.get()

            if not new_status:

                messagebox.showerror(
                    "Error",
                    "Please select a status.",
                    parent=window
                )

                return

            try:

                updated = Ticket.update_status(
                    ticket_id,
                    new_status
                )

                if updated:

                    messagebox.showinfo(
                        "Success",
                        "Ticket status updated successfully.",
                        parent=window
                    )

                    window.destroy()

                    self.refresh()

                else:

                    messagebox.showerror(
                        "Error",
                        "Unable to update ticket status.",
                        parent=window
                    )

            except Exception as error:

                messagebox.showerror(
                    "Database Error",
                    f"Unable to update ticket.\n\n{error}",
                    parent=window
                )

        tk.Button(
            card,
            text="Update Status",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=save_status
        ).pack(
            pady=10
        )

    # ==========================================
    # ASSIGNMENT BOX
    # ==========================================

    def load_assignment_box(
        self,
        parent,
        ticket_id,
        ticket
    ):

        try:

            employees = User.get_all_employees()

        except Exception as error:

            tk.Label(
                parent,
                text="Unable to load employees",
                bg="white",
                fg=DANGER,
                font=("Segoe UI", 10)
            ).pack(
                side="left",
                padx=15
            )

            return

        employee_values = [
            "Unassigned"
        ]

        employee_map = {}

        for employee in employees:

            employee_id = employee[0]
            full_name = employee[1]

            display = f"{employee_id} - {full_name}"

            employee_values.append(
                display
            )

            employee_map[display] = employee_id

        assignment_box = ttk.Combobox(
            parent,
            state="readonly",
            values=employee_values,
            width=30
        )

        assigned_employee = ""

        if len(ticket) > 10:
            assigned_employee = ticket[10]

        selected_display = "Unassigned"

        for display, employee_id in employee_map.items():

            if employee_id == assigned_employee:

                selected_display = display

                break

        assignment_box.set(
            selected_display
        )

        assignment_box.pack(
            side="left",
            padx=15
        )

        def assign_ticket():

            selected = assignment_box.get()

            if selected == "Unassigned":

                employee_id = None

            else:

                employee_id = employee_map.get(
                    selected
                )

            try:

                updated = Ticket.assign_ticket(
                    ticket_id,
                    employee_id
                )

                if updated:

                    messagebox.showinfo(
                        "Success",
                        "Ticket assignment updated successfully."
                    )

                    self.refresh()

                else:

                    messagebox.showerror(
                        "Error",
                        "Unable to update ticket assignment."
                    )

            except Exception as error:

                messagebox.showerror(
                    "Assignment Error",
                    f"Unable to assign ticket.\n\n{error}"
                )

        tk.Button(
            parent,
            text="Assign",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=assign_ticket
        ).pack(
            side="left",
            padx=5
        )

    # ==========================================
    # DETAIL ROW
    # ==========================================

    def create_detail_row(
        self,
        parent,
        label,
        value
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=7
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

        tk.Label(
            frame,
            text=value,
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10),
            anchor="w"
        ).pack(
            side="left"
        )