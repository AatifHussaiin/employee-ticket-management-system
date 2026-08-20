import tkinter as tk
from tkinter import ttk, messagebox

from models.ticket import Ticket
from utils.theme import *


class RaiseTicketPage:

    def __init__(
        self,
        parent,
        employee_id,
        success_callback=None
    ):

        self.parent = parent
        self.employee_id = employee_id
        self.success_callback = success_callback

        self.create_page()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_page(self):

        container = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        # ======================================
        # PAGE TITLE
        # ======================================

        tk.Label(
            container,
            text="Raise New Ticket",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            container,
            text="Submit an IT support request to the help desk.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(3, 15)
        )

        # ======================================
        # FORM
        # ======================================

        form = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid"
        )

        form.pack(
            fill="x"
        )

        # ======================================
        # CATEGORY
        # ======================================

        tk.Label(
            form,
            text="Category *",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 4)
        )

        self.category = ttk.Combobox(
            form,
            state="readonly",
            values=[
                "Hardware",
                "Software",
                "Network",
                "Email",
                "Printer",
                "Others"
            ],
            font=("Segoe UI", 10)
        )

        self.category.pack(
            fill="x",
            padx=30
        )

        self.category.current(0)

        # ======================================
        # SUBJECT
        # ======================================

        tk.Label(
            form,
            text="Subject *",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(12, 4)
        )

        self.subject = tk.Entry(
            form,
            font=("Segoe UI", 10)
        )

        self.subject.pack(
            fill="x",
            padx=30,
            ipady=5
        )

        # ======================================
        # DESCRIPTION
        # ======================================

        tk.Label(
            form,
            text="Description *",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(12, 4)
        )

        self.description = tk.Text(
            form,
            height=5,
            font=("Segoe UI", 10),
            wrap="word"
        )

        self.description.pack(
            fill="x",
            padx=30
        )

        # ======================================
        # PRIORITY
        # ======================================

        tk.Label(
            form,
            text="Priority *",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(12, 4)
        )

        self.priority = ttk.Combobox(
            form,
            state="readonly",
            values=[
                "Low",
                "Medium",
                "High"
            ],
            font=("Segoe UI", 10)
        )

        self.priority.pack(
            fill="x",
            padx=30
        )

        self.priority.current(1)

        # ======================================
        # BUTTONS
        # ======================================

        button_frame = tk.Frame(
            form,
            bg="white"
        )

        button_frame.pack(
            pady=18
        )

        tk.Button(
            button_frame,
            text="Submit Ticket",
            bg=SUCCESS,
            fg="white",
            activebackground="#247A4B",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            width=18,
            command=self.submit_ticket
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        tk.Button(
            button_frame,
            text="Clear Form",
            bg="#64748B",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            width=18,
            command=self.clear_form
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        # ======================================
        # REQUIRED FIELD NOTE
        # ======================================

        tk.Label(
            form,
            text="* Required fields",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 12)
        )

    # ==========================================
    # CLEAR FORM
    # ==========================================

    def clear_form(self):

        self.category.current(0)

        self.subject.delete(
            0,
            tk.END
        )

        self.description.delete(
            "1.0",
            tk.END
        )

        self.priority.current(1)

        self.subject.focus_set()

    # ==========================================
    # SUBMIT TICKET
    # ==========================================

    def submit_ticket(self):

        category = self.category.get().strip()

        subject = self.subject.get().strip()

        description = self.description.get(
            "1.0",
            tk.END
        ).strip()

        priority = self.priority.get().strip()

        # ======================================
        # VALIDATION
        # ======================================

        if category == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a category."
            )

            return

        if subject == "":

            messagebox.showerror(
                "Validation Error",
                "Please enter a subject."
            )

            self.subject.focus_set()

            return

        if len(subject) < 3:

            messagebox.showerror(
                "Validation Error",
                "Subject must contain at least 3 characters."
            )

            self.subject.focus_set()

            return

        if description == "":

            messagebox.showerror(
                "Validation Error",
                "Please describe the problem."
            )

            self.description.focus_set()

            return

        if len(description) < 10:

            messagebox.showerror(
                "Validation Error",
                "Description must contain at least 10 characters."
            )

            self.description.focus_set()

            return

        if priority == "":

            messagebox.showerror(
                "Validation Error",
                "Please select a priority."
            )

            return

        # ======================================
        # SAVE TICKET
        # ======================================

        try:

            ticket_id = Ticket.generate_ticket_id()

            Ticket.create_ticket(
                (
                    ticket_id,
                    self.employee_id,
                    category,
                    subject,
                    description,
                    priority,
                    "Open"
                )
            )

            messagebox.showinfo(
                "Ticket Created",
                "Your ticket has been created successfully.\n\n"
                f"Ticket ID: {ticket_id}\n"
                f"Priority: {priority}\n"
                f"Status: Open"
            )

            self.clear_form()

            if self.success_callback:

                self.success_callback()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                "Unable to create the ticket.\n\n"
                f"Error: {error}"
            )