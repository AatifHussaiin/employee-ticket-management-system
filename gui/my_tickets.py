import tkinter as tk
from tkinter import ttk, messagebox

from models.ticket import Ticket
from utils.theme import *


class MyTicketsPage:

    def __init__(self, parent, employee_id):

        self.parent = parent
        self.employee_id = employee_id

        self.all_tickets = []

        self.create_page()

        self.load_tickets()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_page(self):

        self.container = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        # ======================================
        # TITLE
        # ======================================

        tk.Label(
            self.container,
            text="My Tickets",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            self.container,
            text="View and track all your support requests.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(3, 20)
        )

        # ======================================
        # FILTER BAR
        # ======================================

        filter_frame = tk.Frame(
            self.container,
            bg="white",
            bd=1,
            relief="solid"
        )

        filter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        # Search

        tk.Label(
            filter_frame,
            text="Search",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(20, 5),
            pady=15
        )

        self.search_entry = tk.Entry(
            filter_frame,
            font=("Segoe UI", 10),
            width=30
        )

        self.search_entry.pack(
            side="left",
            ipady=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        # Status

        tk.Label(
            filter_frame,
            text="Status",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(25, 5)
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
            width=13,
            font=("Segoe UI", 10)
        )

        self.status_filter.pack(
            side="left"
        )

        self.status_filter.current(0)

        self.status_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # Priority

        tk.Label(
            filter_frame,
            text="Priority",
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
            width=13,
            font=("Segoe UI", 10)
        )

        self.priority_filter.pack(
            side="left"
        )

        self.priority_filter.current(0)

        self.priority_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # Refresh

        tk.Button(
            filter_frame,
            text="Refresh",
            bg=PRIMARY,
            fg="white",
            activebackground="#0B3A63",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.load_tickets
        ).pack(
            side="right",
            padx=20
        )

        # ======================================
        # TABLE FRAME
        # ======================================

        table_frame = tk.Frame(
            self.container,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # SCROLLBARS
        # ======================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        # ======================================
        # TREEVIEW
        # ======================================

        columns = (
            "ticket_id",
            "category",
            "subject",
            "priority",
            "status",
            "assigned_to",
            "created_at"
        )

        self.ticket_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        vertical_scrollbar.config(
            command=self.ticket_table.yview
        )

        horizontal_scrollbar.config(
            command=self.ticket_table.xview
        )

        # ======================================
        # COLUMN HEADINGS
        # ======================================

        self.ticket_table.heading(
            "ticket_id",
            text="Ticket ID"
        )

        self.ticket_table.heading(
            "category",
            text="Category"
        )

        self.ticket_table.heading(
            "subject",
            text="Subject"
        )

        self.ticket_table.heading(
            "priority",
            text="Priority"
        )

        self.ticket_table.heading(
            "status",
            text="Status"
        )

        self.ticket_table.heading(
            "assigned_to",
            text="Assigned To"
        )

        self.ticket_table.heading(
            "created_at",
            text="Created Date"
        )

        # ======================================
        # COLUMN WIDTHS
        # ======================================

        self.ticket_table.column(
            "ticket_id",
            width=130,
            anchor="center"
        )

        self.ticket_table.column(
            "category",
            width=130,
            anchor="center"
        )

        self.ticket_table.column(
            "subject",
            width=300,
            anchor="w"
        )

        self.ticket_table.column(
            "priority",
            width=110,
            anchor="center"
        )

        self.ticket_table.column(
            "status",
            width=110,
            anchor="center"
        )

        self.ticket_table.column(
            "assigned_to",
            width=180,
            anchor="center"
        )

        self.ticket_table.column(
            "created_at",
            width=180,
            anchor="center"
        )

        # ======================================
        # TABLE PACK
        # ======================================

        self.ticket_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )

        # ======================================
        # ROW COLORS
        # ======================================

        self.ticket_table.tag_configure(
            "open",
            foreground="#0F4C81"
        )

        self.ticket_table.tag_configure(
            "pending",
            foreground="#D97706"
        )

        self.ticket_table.tag_configure(
            "resolved",
            foreground="#2E8B57"
        )

        self.ticket_table.tag_configure(
            "high",
            foreground="#C0392B"
        )

        # ======================================
        # DOUBLE CLICK
        # ======================================

        self.ticket_table.bind(
            "<Double-1>",
            self.show_ticket_details
        )

        # ======================================
        # BOTTOM INFORMATION
        # ======================================

        self.info_label = tk.Label(
            self.container,
            text="",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        )

        self.info_label.pack(
            anchor="w",
            pady=(8, 0)
        )

    # ==========================================
    # LOAD TICKETS
    # ==========================================

    def load_tickets(self):

        try:

            self.all_tickets = Ticket.get_employee_tickets(
                self.employee_id
            )

            self.apply_filters()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                "Unable to load tickets.\n\n"
                f"Error: {error}"
            )

    # ==========================================
    # APPLY FILTERS
    # ==========================================

    def apply_filters(self):

        search_text = self.search_entry.get().strip().lower()

        selected_status = self.status_filter.get()

        selected_priority = self.priority_filter.get()

        # Clear table

        for item in self.ticket_table.get_children():

            self.ticket_table.delete(item)

        visible_count = 0

        for ticket in self.all_tickets:

            ticket_id = str(ticket[0])
            category = str(ticket[1])
            subject = str(ticket[2])
            priority = str(ticket[3])
            status = str(ticket[4])
            assigned_to = str(ticket[5])

            # Handle empty assignment

            if not assigned_to or assigned_to == "None":

                assigned_to = "Unassigned"

            created_at = str(ticket[6])

            # Search

            search_content = (
                ticket_id + " "
                + category + " "
                + subject + " "
                + priority + " "
                + status + " "
                + assigned_to
            ).lower()

            if search_text not in search_content:

                continue

            # Status filter

            if (
                selected_status != "All"
                and status != selected_status
            ):

                continue

            # Priority filter

            if (
                selected_priority != "All"
                and priority != selected_priority
            ):

                continue

            # Determine row tag

            if status.lower() == "open":

                tag = "open"

            elif status.lower() == "pending":

                tag = "pending"

            elif status.lower() == "resolved":

                tag = "resolved"

            else:

                tag = ""

            # Insert row

            self.ticket_table.insert(
                "",
                "end",
                values=(
                    ticket_id,
                    category,
                    subject,
                    priority,
                    status,
                    assigned_to,
                    created_at
                ),
                tags=(tag,)
            )

            visible_count += 1

        self.info_label.config(
            text=f"Showing {visible_count} ticket(s)"
        )

    # ==========================================
    # SHOW TICKET DETAILS
    # ==========================================

    def show_ticket_details(self, event=None):

        selected = self.ticket_table.selection()

        if not selected:

            return

        item = self.ticket_table.item(
            selected[0]
        )

        values = item.get("values")

        if not values:

            return

        ticket_id = values[0]

        try:

            ticket = Ticket.get_ticket(
                ticket_id
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load ticket details.\n\n{error}"
            )

            return

        if not ticket:

            messagebox.showerror(
                "Error",
                "Ticket could not be found."
            )

            return

        self.open_details_window(
            ticket_id,
            values,
            ticket
        )

    # ==========================================
    # DETAILS WINDOW
    # ==========================================

    def open_details_window(
        self,
        ticket_id,
        values,
        ticket
    ):

        window = tk.Toplevel(
            self.parent
        )

        window.title(
            f"Ticket Details - {ticket_id}"
        )

        window.geometry(
            "650x650"
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
        # DETAILS FRAME
        # ======================================

        details = tk.Frame(
            window,
            bg="white",
            bd=1,
            relief="solid"
        )

        details.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.add_detail(
            details,
            "Ticket ID",
            str(values[0])
        )

        self.add_detail(
            details,
            "Category",
            str(values[1])
        )

        self.add_detail(
            details,
            "Subject",
            str(values[2])
        )

        self.add_detail(
            details,
            "Priority",
            str(values[3])
        )

        self.add_detail(
            details,
            "Status",
            str(values[4])
        )

        self.add_detail(
            details,
            "Assigned To",
            str(values[5])
        )

        self.add_detail(
            details,
            "Created Date",
            str(values[6])
        )

        # ======================================
        # DESCRIPTION
        # ======================================

        tk.Label(
            details,
            text="Description",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        description_text = ""

        # Complete ticket database order:
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
        #
        # Therefore description is ticket[5].

        if len(ticket) >= 6:

            description_text = str(
                ticket[5]
            )

        description_box = tk.Text(
            details,
            height=7,
            font=("Segoe UI", 10),
            wrap="word",
            bg="#F8FAFC"
        )

        description_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        description_box.insert(
            "1.0",
            description_text
        )

        description_box.config(
            state="disabled"
        )

        # ======================================
        # CLOSE BUTTON
        # ======================================

        tk.Button(
            window,
            text="Close",
            bg=PRIMARY,
            fg="white",
            activebackground="#0B3A63",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            width=15,
            command=window.destroy
        ).pack(
            pady=15
        )

    # ==========================================
    # DETAIL ROW
    # ==========================================

    def add_detail(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=6
        )

        tk.Label(
            row,
            text=label,
            bg="white",
            fg=LIGHT_TEXT,
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