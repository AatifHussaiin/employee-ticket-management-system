import tkinter as tk
from tkinter import ttk, messagebox

from models.ticket import Ticket
from utils.theme import *


class ReportsPage:

    def __init__(self, parent, employee_id):

        self.parent = parent
        self.employee_id = employee_id

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

        self.scrollbar = tk.Scrollbar(
            self.outer,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        # ======================================
        # INNER FRAME
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

        self.container.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        # ======================================
        # MOUSE WHEEL BINDING
        # ======================================

        self.root = self.parent.winfo_toplevel()

        self.root.bind_all(
            "<MouseWheel>",
            self.mousewheel,
            add="+"
        )

        # Support Linux mouse wheel
        self.root.bind_all(
            "<Button-4>",
            self.mousewheel_linux_up,
            add="+"
        )

        self.root.bind_all(
            "<Button-5>",
            self.mousewheel_linux_down,
            add="+"
        )

        self.build_report()

    # ==========================================
    # SCROLL REGION
    # ==========================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==========================================
    # RESIZE CANVAS
    # ==========================================

    def resize_canvas(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # ==========================================
    # WINDOWS MOUSE WHEEL
    # ==========================================

    def mousewheel(self, event):

        # Only scroll if the Reports page is active
        if not self.canvas.winfo_exists():
            return

        # Windows normally gives delta = 120 or -120
        movement = int(-event.delta / 120)

        if movement != 0:

            self.canvas.yview_scroll(
                movement,
                "units"
            )

    # ==========================================
    # LINUX MOUSE WHEEL UP
    # ==========================================

    def mousewheel_linux_up(self, event):

        if self.canvas.winfo_exists():

            self.canvas.yview_scroll(
                -3,
                "units"
            )

    # ==========================================
    # LINUX MOUSE WHEEL DOWN
    # ==========================================

    def mousewheel_linux_down(self, event):

        if self.canvas.winfo_exists():

            self.canvas.yview_scroll(
                3,
                "units"
            )

    # ==========================================
    # BUILD REPORT
    # ==========================================

    def build_report(self):

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
        # HEADER
        # ======================================

        header = tk.Frame(
            content,
            bg=BACKGROUND
        )

        header.pack(
            fill="x"
        )

        title_frame = tk.Frame(
            header,
            bg=BACKGROUND
        )

        title_frame.pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text="Reports & Analytics",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 26, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Analyze your support ticket activity and performance.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Button(
            header,
            text="↻  Refresh Reports",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief="flat",
            command=self.refresh_reports
        ).pack(
            side="right",
            padx=5,
            pady=10,
            ipadx=10,
            ipady=5
        )

        # ======================================
        # GET DATA
        # ======================================

        try:

            counts = Ticket.get_dashboard_counts(
                self.employee_id
            )

            status_data = Ticket.get_status_report(
                self.employee_id
            )

            priority_data = Ticket.get_priority_report(
                self.employee_id
            )

            category_data = Ticket.get_category_report(
                self.employee_id
            )

            monthly_data = Ticket.get_monthly_report(
                self.employee_id
            )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                f"Unable to load report data.\n\n{error}"
            )

            return

        # ======================================
        # SUMMARY CARDS
        # ======================================

        cards = tk.Frame(
            content,
            bg=BACKGROUND
        )

        cards.pack(
            fill="x",
            pady=(25, 0)
        )

        for i in range(5):

            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_card(
            cards,
            "Total Tickets",
            counts.get("total", 0),
            PRIMARY,
            0
        )

        self.create_card(
            cards,
            "Open",
            counts.get("open", 0),
            PRIMARY,
            1
        )

        self.create_card(
            cards,
            "Pending",
            counts.get("pending", 0),
            WARNING,
            2
        )

        self.create_card(
            cards,
            "Resolved",
            counts.get("resolved", 0),
            SUCCESS,
            3
        )

        self.create_card(
            cards,
            "High Priority",
            counts.get("high_priority", 0),
            DANGER,
            4
        )

        # ======================================
        # STATUS SECTION
        # ======================================

        status_section = self.create_section(
            content,
            "Ticket Status Distribution",
            "Current distribution of your tickets by status."
        )

        self.create_status_bars(
            status_section,
            status_data
        )

        # ======================================
        # PRIORITY SECTION
        # ======================================

        priority_section = self.create_section(
            content,
            "Priority Distribution",
            "Number of tickets according to priority level."
        )

        self.create_priority_bars(
            priority_section,
            priority_data
        )

        # ======================================
        # CATEGORY SECTION
        # ======================================

        category_section = self.create_section(
            content,
            "Tickets by Category",
            "Distribution of tickets across support categories."
        )

        self.create_category_bars(
            category_section,
            category_data
        )

        # ======================================
        # MONTHLY TREND
        # ======================================

        monthly_section = self.create_section(
            content,
            "Monthly Ticket Trend",
            "Number of tickets created during each month."
        )

        self.create_monthly_chart(
            monthly_section,
            monthly_data
        )

        # ======================================
        # SUMMARY TABLE
        # ======================================

        self.create_summary_table(
            content,
            category_data
        )

        # ======================================
        # FOOTER
        # ======================================

        tk.Label(
            content,
            text="Report data is generated from your ticket history.",
            bg=BACKGROUND,
            fg=LIGHT_TEXT,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 30)
        )

    # ==========================================
    # CREATE SECTION
    # ==========================================

    def create_section(
        self,
        parent,
        title,
        subtitle
    ):

        section = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        section.pack(
            fill="x",
            pady=(25, 0)
        )

        tk.Label(
            section,
            text=title,
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            section,
            text=subtitle,
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=20
        )

        return section

    # ==========================================
    # SUMMARY CARD
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
            height=110,
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
            font=("Segoe UI", 10)
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            card,
            text=str(value),
            bg="white",
            fg=color,
            font=("Segoe UI", 23, "bold")
        ).pack()

    # ==========================================
    # STATUS BARS
    # ==========================================

    def create_status_bars(
        self,
        parent,
        data
    ):

        total = sum(
            data.values()
        )

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        colors = {
            "Open": PRIMARY,
            "Pending": WARNING,
            "Resolved": SUCCESS
        }

        for status in [
            "Open",
            "Pending",
            "Resolved"
        ]:

            value = data.get(
                status,
                0
            )

            percentage = (
                value / total * 100
                if total > 0
                else 0
            )

            row = tk.Frame(
                frame,
                bg="white"
            )

            row.pack(
                fill="x",
                pady=7
            )

            tk.Label(
                row,
                text=status,
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                width=12,
                anchor="w"
            ).pack(
                side="left"
            )

            bar_background = tk.Frame(
                row,
                bg="#E5E7EB",
                height=20
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True
            )

            bar = tk.Frame(
                bar_background,
                bg=colors.get(
                    status,
                    PRIMARY
                )
            )

            bar.place(
                relwidth=percentage / 100,
                relheight=1
            )

            tk.Label(
                row,
                text=f"{value}  ({percentage:.0f}%)",
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10),
                width=15,
                anchor="e"
            ).pack(
                side="right"
            )

    # ==========================================
    # PRIORITY BARS
    # ==========================================

    def create_priority_bars(
        self,
        parent,
        data
    ):

        total = sum(
            data.values()
        )

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        colors = {
            "Low": SUCCESS,
            "Medium": WARNING,
            "High": DANGER
        }

        for priority in [
            "Low",
            "Medium",
            "High"
        ]:

            value = data.get(
                priority,
                0
            )

            percentage = (
                value / total * 100
                if total > 0
                else 0
            )

            row = tk.Frame(
                frame,
                bg="white"
            )

            row.pack(
                fill="x",
                pady=7
            )

            tk.Label(
                row,
                text=priority,
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                width=12,
                anchor="w"
            ).pack(
                side="left"
            )

            bar_background = tk.Frame(
                row,
                bg="#E5E7EB",
                height=20
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True
            )

            bar = tk.Frame(
                bar_background,
                bg=colors.get(
                    priority,
                    PRIMARY
                )
            )

            bar.place(
                relwidth=percentage / 100,
                relheight=1
            )

            tk.Label(
                row,
                text=f"{value}  ({percentage:.0f}%)",
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10),
                width=15,
                anchor="e"
            ).pack(
                side="right"
            )

    # ==========================================
    # CATEGORY BARS
    # ==========================================

    def create_category_bars(
        self,
        parent,
        data
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        if not data:

            tk.Label(
                frame,
                text="No ticket data available.",
                bg="white",
                fg=LIGHT_TEXT,
                font=("Segoe UI", 10)
            ).pack(
                pady=15
            )

            return

        maximum = max(
            data.values()
        )

        for category, value in data.items():

            row = tk.Frame(
                frame,
                bg="white"
            )

            row.pack(
                fill="x",
                pady=7
            )

            tk.Label(
                row,
                text=category,
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                width=15,
                anchor="w"
            ).pack(
                side="left"
            )

            bar_background = tk.Frame(
                row,
                bg="#E5E7EB",
                height=20
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True
            )

            percentage = (
                value / maximum
                if maximum > 0
                else 0
            )

            bar = tk.Frame(
                bar_background,
                bg=PRIMARY
            )

            bar.place(
                relwidth=percentage,
                relheight=1
            )

            tk.Label(
                row,
                text=str(value),
                bg="white",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                width=8,
                anchor="e"
            ).pack(
                side="right"
            )

    # ==========================================
    # MONTHLY CHART
    # ==========================================

    def create_monthly_chart(
        self,
        parent,
        monthly_data
    ):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        if not monthly_data:

            tk.Label(
                frame,
                text="No monthly ticket data available.",
                bg="white",
                fg=LIGHT_TEXT,
                font=("Segoe UI", 10)
            ).pack(
                pady=20
            )

            return

        chart_width = 850
        chart_height = 300

        canvas = tk.Canvas(
            frame,
            width=chart_width,
            height=chart_height,
            bg="white",
            highlightthickness=0
        )

        canvas.pack(
            fill="x"
        )

        labels = [
            row[0]
            for row in monthly_data
        ]

        values = [
            row[1]
            for row in monthly_data
        ]

        maximum = max(values)

        if maximum == 0:
            maximum = 1

        left_margin = 60
        right_margin = 30
        top_margin = 30
        bottom_margin = 55

        chart_left = left_margin
        chart_right = chart_width - right_margin
        chart_top = top_margin
        chart_bottom = chart_height - bottom_margin

        chart_height_actual = (
            chart_bottom - chart_top
        )

        chart_width_actual = (
            chart_right - chart_left
        )

        # Y axis

        canvas.create_line(
            chart_left,
            chart_top,
            chart_left,
            chart_bottom,
            fill="#94A3B8"
        )

        # X axis

        canvas.create_line(
            chart_left,
            chart_bottom,
            chart_right,
            chart_bottom,
            fill="#94A3B8"
        )

        # Grid

        grid_count = 5

        for i in range(
            grid_count + 1
        ):

            value = (
                maximum / grid_count
            ) * i

            y = (
                chart_bottom
                -
                (
                    value / maximum
                    *
                    chart_height_actual
                )
            )

            canvas.create_line(
                chart_left,
                y,
                chart_right,
                y,
                fill="#E5E7EB"
            )

            canvas.create_text(
                chart_left - 15,
                y,
                text=str(
                    int(value)
                ),
                fill="#64748B",
                font=("Segoe UI", 9),
                anchor="e"
            )

        count = len(values)

        spacing = (
            chart_width_actual / count
        )

        bar_width = min(
            60,
            spacing * 0.55
        )

        for index, value in enumerate(values):

            center_x = (
                chart_left
                +
                spacing * index
                +
                spacing / 2
            )

            bar_height = (
                value / maximum
                *
                chart_height_actual
            )

            x1 = (
                center_x
                -
                bar_width / 2
            )

            x2 = (
                center_x
                +
                bar_width / 2
            )

            y1 = (
                chart_bottom
                -
                bar_height
            )

            y2 = chart_bottom

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=PRIMARY,
                outline=""
            )

            canvas.create_text(
                center_x,
                y1 - 10,
                text=str(value),
                fill=TEXT,
                font=("Segoe UI", 9, "bold")
            )

            label = labels[index]

            if label and "-" in label:

                parts = label.split("-")

                if len(parts) == 2:

                    label = (
                        parts[0][-2:]
                        + "-"
                        + parts[1]
                    )

            canvas.create_text(
                center_x,
                chart_bottom + 20,
                text=label,
                fill="#64748B",
                font=("Segoe UI", 9)
            )

    # ==========================================
    # SUMMARY TABLE
    # ==========================================

    def create_summary_table(
        self,
        parent,
        category_data
    ):

        frame = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        frame.pack(
            fill="x",
            pady=(25, 0)
        )

        tk.Label(
            frame,
            text="Category Summary",
            bg="white",
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            frame,
            text="Detailed count of tickets by category.",
            bg="white",
            fg=LIGHT_TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=20
        )

        table_frame = tk.Frame(
            frame,
            bg="white"
        )

        table_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        columns = (
            "category",
            "count"
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        table.heading(
            "category",
            text="Category"
        )

        table.heading(
            "count",
            text="Number of Tickets"
        )

        table.column(
            "category",
            width=400,
            anchor="w"
        )

        table.column(
            "count",
            width=200,
            anchor="center"
        )

        for category, count in category_data.items():

            table.insert(
                "",
                "end",
                values=(
                    category,
                    count
                )
            )

        if not category_data:

            table.insert(
                "",
                "end",
                values=(
                    "No tickets created",
                    0
                )
            )

        table.pack(
            fill="x"
        )

    # ==========================================
    # REFRESH REPORTS
    # ==========================================

    def refresh_reports(self):

        for widget in self.container.winfo_children():

            widget.destroy()

        self.build_report()

        self.canvas.yview_moveto(0)