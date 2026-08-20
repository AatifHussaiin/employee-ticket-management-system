import tkinter as tk
from tkinter import ttk


# ==========================================
# START APPLICATION
# ==========================================

def start_application():

    root = tk.Tk()
    SplashScreen(root)
    root.mainloop()


# ==========================================
# SPLASH SCREEN
# ==========================================

class SplashScreen:

    def __init__(self, root):

        self.root = root

        self.root.title("Employee Ticket Management System")
        self.root.geometry("700x450")
        self.root.resizable(False, False)

        self.center_window()

        self.root.configure(bg="#1E3A8A")

        tk.Label(
            self.root,
            text="Employee Ticket Management System",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#1E3A8A"
        ).pack(pady=80)

        tk.Label(
            self.root,
            text="IT Help Desk Solution",
            font=("Segoe UI", 14),
            fg="white",
            bg="#1E3A8A"
        ).pack()

        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=450,
            mode="determinate"
        )

        self.progress.pack(pady=50)

        self.value = 0

        self.load()

    # ==========================================

    def center_window(self):

        width = 700
        height = 450

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # ==========================================

    def load(self):

        if self.value < 100:

            self.value += 2

            self.progress["value"] = self.value

            self.root.after(40, self.load)

        else:

            self.root.destroy()

            from gui.login import LoginWindow

            login_root = tk.Tk()

            LoginWindow(login_root)

            login_root.mainloop()


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    start_application()