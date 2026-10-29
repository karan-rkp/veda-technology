
import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import date, datetime
from collections import defaultdict

# Charts for the Analytics page (install with: pip install matplotlib)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================================================
# CONFIGURATION
# =========================================================

APP_NAME = "PennyWise"
CURRENCY = "₹"

BG = "#F4F7FB"
WHITE = "#FFFFFF"
NAVY = "#111827"
NAVY_LIGHT = "#1F2937"
TEAL = "#0D9488"
TEAL_LIGHT = "#CCFBF1"
TEXT = "#172033"
MUTED = "#778196"
BORDER = "#E4E9F1"
RED = "#DC5656"
ORANGE = "#E8A23A"

THEMES = {
    "light": {
        "BG": "#F4F7FB", "WHITE": "#FFFFFF", "NAVY": "#111827",
        "NAVY_LIGHT": "#1F2937", "TEAL": "#0D9488", "TEAL_LIGHT": "#CCFBF1",
        "TEXT": "#172033", "MUTED": "#778196", "BORDER": "#E4E9F1",
        "RED": "#DC5656", "ORANGE": "#E8A23A",
    },
    "dark": {
        "BG": "#0B1120", "WHITE": "#111B2E", "NAVY": "#070D19",
        "NAVY_LIGHT": "#17243A", "TEAL": "#2DD4BF", "TEAL_LIGHT": "#153B3B",
        "TEXT": "#E8EEF8", "MUTED": "#9AAAC1", "BORDER": "#26354B",
        "RED": "#FB7185", "ORANGE": "#FBBF24",
    },
}
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

EXPENSE_FILE = DATA_DIR / "expenses.json"
BUDGET_FILE = DATA_DIR / "budgets.json"

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills",
    "Education", "Health", "Entertainment", "Travel", "Other"
]

CATEGORY_COLORS = [
    "#0D9488", "#6485E8", "#E8A23A", "#A277D5",
    "#E16D8A", "#3B9CC8", "#75A85B", "#D88C55", "#8792A6"
]


def load_json(path, default):
    if not path.exists():
        return default

    try:
        with path.open("r", encoding="utf-8") as file:
            result = json.load(file)

        if not isinstance(result, type(default)):
            raise ValueError("Unexpected JSON data format.")

        return result

    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Data loading error",
            f"Could not load {path}.\n\n{error}\n\n"
            "The original file has not been overwritten."
        )
        raise SystemExit(1)


def save_json(path, content):
    temp = path.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    temp.replace(path)


def money(amount):
    return f"{CURRENCY}{amount:,.2f}"


# =========================================================
# MAIN APPLICATION
# =========================================================

class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PennyWise | Expense & Budget Tracker")
        self.geometry("1320x820")
        self.minsize(1000, 650)
        self.theme_name = "light"
        self.apply_theme()
        self.configure(bg=BG)

        self.expenses = load_json(EXPENSE_FILE, [])
        self.budgets = load_json(BUDGET_FILE, {})

        self.current_page = "Dashboard"
        self.search_var = tk.StringVar()
        self.month_var = tk.StringVar(
            value=date.today().strftime("%Y-%m")
        )

        self.setup_styles()
        self.build_layout()
        self.show_dashboard()

    # -----------------------------------------------------
    # STYLES
    # -----------------------------------------------------

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 9, "bold"),
            padding=12,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", TEAL_LIGHT)],
            foreground=[("selected", NAVY)]
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=("Segoe UI", 10)
        )

    def label(self, parent, text, size=10, color=TEXT,
              bold=False, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            bg=kwargs.pop("bg", WHITE),
            fg=color,
            **kwargs
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold" if primary else "normal"),
            bg=TEAL if primary else WHITE,
            fg=WHITE if primary else TEXT,
            activebackground="#0F766E" if primary else "#EAF0F6",
            activeforeground=WHITE if primary else TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10
        )

    def apply_theme(self):
        """Apply the selected palette to the app's shared color variables."""
        global BG, WHITE, NAVY, NAVY_LIGHT, TEAL, TEAL_LIGHT
        global TEXT, MUTED, BORDER, RED, ORANGE
        palette = THEMES[self.theme_name]
        BG = palette["BG"]
        WHITE = palette["WHITE"]
        NAVY = palette["NAVY"]
        NAVY_LIGHT = palette["NAVY_LIGHT"]
        TEAL = palette["TEAL"]
        TEAL_LIGHT = palette["TEAL_LIGHT"]
        TEXT = palette["TEXT"]
        MUTED = palette["MUTED"]
        BORDER = palette["BORDER"]
        RED = palette["RED"]
        ORANGE = palette["ORANGE"]

    def toggle_theme(self):
        """Switch between light and dark mode and redraw the current page."""
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.apply_theme()

        # Rebuild the shell so sidebar, cards, tables and page widgets
        # all pick up the new palette. Expense and budget data stay untouched.
        for widget in self.winfo_children():
            widget.destroy()

        self.configure(bg=BG)
        self.setup_styles()
        self.build_layout()
        self.navigate(self.current_page)

    # -----------------------------------------------------
    # LAYOUT
    # -----------------------------------------------------

    def build_layout(self):
        self.sidebar = tk.Frame(self, bg=NAVY, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=NAVY)
        brand.pack(fill="x", padx=20, pady=(27, 30))

        tk.Label(
            brand,
            text="◈",
            font=("Segoe UI", 27, "bold"),
            fg="#5EEAD4",
            bg=NAVY
        ).pack(side="left")

        tk.Label(
            brand,
            text="PennyWise\nPERSONAL FINANCE",
            justify="left",
            font=("Segoe UI", 12, "bold"),
            fg=WHITE,
            bg=NAVY
        ).pack(side="left", padx=9)

        self.nav_buttons = {}

        nav_items = [
            ("▦", "Dashboard"),
            ("↔", "Transactions"),
            ("◉", "Budgets"),
            ("▥", "Analytics"),
        ]

        for icon, name in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}     {name}",
                command=lambda page=name: self.navigate(page),
                anchor="w",
                font=("Segoe UI", 11),
                bg=NAVY,
                fg="#C5CEDB",
                activebackground=NAVY_LIGHT,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                padx=18,
                pady=14,
                cursor="hand2"
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        spacer = tk.Frame(self.sidebar, bg=NAVY)
        spacer.pack(expand=True, fill="both")

        tk.Frame(
            self.sidebar, bg="#374151", height=1
        ).pack(fill="x", padx=20, pady=15)

        tk.Label(
            self.sidebar,
            text="YOUR MONEY, YOUR CONTROL",
            font=("Segoe UI", 8, "bold"),
            fg="#8D9AAF",
            bg=NAVY
        ).pack(anchor="w", padx=20, pady=(0, 7))

        tk.Label(
            self.sidebar,
            text="Local storage • Private by default",
            font=("Segoe UI", 8),
            fg="#8D9AAF",
            bg=NAVY
        ).pack(anchor="w", padx=20, pady=(0, 24))

        self.workspace = tk.Frame(self, bg=BG)
        self.workspace.pack(
            side="left", fill="both", expand=True
        )

        # Top bar
        self.topbar = tk.Frame(self.workspace, bg=WHITE, height=65)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title = tk.Label(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 17, "bold"),
            fg=TEXT,
            bg=WHITE
        )
        self.page_title.pack(side="left", padx=28)

        self.date_label = tk.Label(
            self.topbar,
            text=date.today().strftime("%A, %d %B %Y"),
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=WHITE
        )
        self.date_label.pack(side="right", padx=(12, 22))

        self.theme_btn = tk.Button(
            self.topbar,
            text=("☀  Light mode" if self.theme_name == "dark" else "☾  Dark mode"),
            command=self.toggle_theme,
            font=("Segoe UI", 9, "bold"),
            bg=BG, fg=TEXT, activebackground=BORDER, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2", padx=13, pady=8
        )
        self.theme_btn.pack(side="right", padx=(0, 12), pady=12)

        self.content = tk.Frame(self.workspace, bg=BG)
        self.content.pack(
            fill="both", expand=True, padx=26, pady=23
        )

    def navigate(self, page):
        self.current_page = page

        for name, btn in self.nav_buttons.items():
            selected = name == page
            btn.configure(
                bg=NAVY_LIGHT if selected else NAVY,
                fg="#5EEAD4" if selected else "#C5CEDB"
            )

        self.page_title.configure(text=page)

        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Transactions":
            self.show_transactions()
        elif page == "Budgets":
            self.show_budgets()
        elif page == "Analytics":
            self.show_analytics()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def section_heading(self, title, subtitle):
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 18))

        left = tk.Frame(top, bg=BG)
        left.pack(side="left", fill="x", expand=True)

        self.label(
            left, title, 19, TEXT, True, bg=BG
        ).pack(anchor="w")

        self.label(
            left, subtitle, 10, MUTED, bg=BG
        ).pack(anchor="w", pady=(5, 0))

        self.button(
            top, "+ Add Expense", self.add_expense, True
        ).pack(side="right", padx=(10, 0))

    def card(self, parent, title, value, hint, accent=TEAL):
        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Frame(frame, bg=accent, height=4).pack(fill="x")

        inner = tk.Frame(frame, bg=WHITE)
        inner.pack(fill="both", expand=True, padx=17, pady=16)

        self.label(
            inner, title.upper(), 9, MUTED, True
        ).pack(anchor="w")

        self.label(
            inner, value, 21, TEXT, True
        ).pack(anchor="w", pady=(10, 5))

        self.label(
            inner, hint, 9, MUTED
        ).pack(anchor="w")

        return frame

    # -----------------------------------------------------
    # DATA HELPERS
    # -----------------------------------------------------

    def total_spending(self, month=None):
        return sum(
            float(e["amount"])
            for e in self.expenses
            if month is None or e.get("date", "").startswith(month)
        )

    def monthly_budget(self, month):
        return float(self.budgets.get(month, 0))

    def recent_expenses(self, limit=6):
        return sorted(
            self.expenses,
            key=lambda e: (e.get("date", ""), e.get("id", 0)),
            reverse=True
        )[:limit]

    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    def show_dashboard(self):
        self.clear_content()

        month = date.today().strftime("%Y-%m")
        spent = self.total_spending(month)
        budget = self.monthly_budget(month)
        remaining = budget - spent if budget else 0

        self.section_heading(
            "Good day! 👋",
            "Here is your financial snapshot for this month."
        )

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 20))

        stats = [
            ("Monthly Spending", money(spent),
             "Expenses this month", TEAL),
            ("Monthly Budget", money(budget),
             "Your planned spending limit", "#6485E8"),
            ("Remaining Budget",
             money(remaining) if budget else "Not set",
             "Budget minus spending" if budget else "Set a monthly budget",
             ORANGE if budget and remaining < 0 else "#75A85B"),
            ("Total Transactions", str(len(self.expenses)),
             "All recorded expenses", "#A277D5"),
        ]

        for index, (title, value, hint, accent) in enumerate(stats):
            cards.grid_columnconfigure(index, weight=1)
            self.card(
                cards, title, value, hint, accent
            ).grid(
                row=0, column=index, sticky="nsew",
                padx=(0 if index == 0 else 7, 0)
            )

        middle = tk.Frame(self.content, bg=BG)
        middle.pack(fill="both", expand=True)

        left = tk.Frame(
            middle, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        left.pack(side="left", fill="both", expand=True)

        self.label(
            left, "Recent Transactions", 12, TEXT, True
        ).pack(anchor="w", padx=18, pady=(17, 4))

        self.label(
            left, "Your latest recorded expenses", 9, MUTED
        ).pack(anchor="w", padx=18, pady=(0, 12))

        self.create_tree(
            left,
            [
                ("date", "DATE", 95),
                ("title", "DESCRIPTION", 175),
                ("category", "CATEGORY", 110),
                ("amount", "AMOUNT", 100),
            ],
            self.recent_expenses(7)
        ).pack(fill="both", expand=True, padx=12, pady=(0, 12))

        right = tk.Frame(
            middle, bg=WHITE, width=255,
            highlightbackground=BORDER, highlightthickness=1
        )
        right.pack(side="left", fill="y", padx=(16, 0))
        right.pack_propagate(False)

        self.label(
            right, "Budget Progress", 12, TEXT, True
        ).pack(anchor="w", padx=17, pady=(17, 4))

        self.label(
            right, month, 9, MUTED
        ).pack(anchor="w", padx=17, pady=(0, 15))

        if budget <= 0:
            self.label(
                right,
                "No budget set yet.\n\nSet a monthly limit to\ntrack your progress.",
                10, MUTED, bg=WHITE, justify="left"
            ).pack(anchor="w", padx=17, pady=12)

            self.button(
                right, "Set Monthly Budget",
                lambda: self.navigate("Budgets"), True
            ).pack(fill="x", padx=16, pady=8)
        else:
            ratio = spent / budget
            progress = min(ratio * 100, 100)

            self.label(
                right, f"{progress:.1f}% used", 20, TEXT, True
            ).pack(anchor="w", padx=17, pady=(8, 4))

            bar_bg = tk.Frame(right, bg=BORDER, height=10)
            bar_bg.pack(fill="x", padx=17, pady=8)

            fill_width = max(0, min(100, progress))
            tk.Frame(
                bar_bg,
                bg=RED if ratio > 1 else TEAL,
                height=10
            ).place(relwidth=fill_width / 100, relheight=1)

            self.label(
                right, f"Spent: {money(spent)}", 9, MUTED
            ).pack(anchor="w", padx=17, pady=(12, 4))

            self.label(
                right, f"Limit: {money(budget)}", 9, MUTED
            ).pack(anchor="w", padx=17, pady=4)

            if ratio > 1:
                status = "Budget exceeded"
                status_color = RED
            elif ratio >= 0.8:
                status = "Approaching limit"
                status_color = ORANGE
            else:
                status = "Within budget"
                status_color = TEAL

            self.label(
                right, status, 10, status_color, True
            ).pack(anchor="w", padx=17, pady=(15, 0))

    # -----------------------------------------------------
    # TREEVIEW
    # -----------------------------------------------------

    def create_tree(self, parent, columns, records):
        container = tk.Frame(parent, bg=WHITE)

        keys = [column[0] for column in columns]

        tree = ttk.Treeview(
            container,
            columns=keys,
            show="headings",
            selectmode="browse"
        )

        for key, title, width in columns:
            tree.heading(key, text=title)
            tree.column(key, width=width, minwidth=65, anchor="w")

        for item in records:
            values = []

            for key in keys:
                if key == "amount":
                    values.append(money(float(item.get(key, 0))))
                else:
                    values.append(item.get(key, ""))

            tree.insert("", "end", iid=str(item["id"]), values=values)

        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return container

    # -----------------------------------------------------
    # TRANSACTIONS
    # -----------------------------------------------------

    def show_transactions(self):
        self.clear_content()

        self.section_heading(
            "Transactions",
            "View, search and manage every expense."
        )

        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", pady=(0, 13))

        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief="flat",
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT
        )
        search_entry.pack(side="left", ipady=10, ipadx=10, fill="x", expand=True)

        search_entry.bind("<KeyRelease>", lambda event: self.refresh_transactions())

        self.button(
            toolbar, "Clear Search", self.clear_search
        ).pack(side="left", padx=8)

        self.button(
            toolbar, "Delete Selected", self.delete_selected
        ).pack(side="left")

        self.transaction_container = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        self.transaction_container.pack(fill="both", expand=True)

        self.refresh_transactions()

    def clear_search(self):
        self.search_var.set("")
        self.refresh_transactions()

    def refresh_transactions(self):
        if not hasattr(self, "transaction_container"):
            return

        for widget in self.transaction_container.winfo_children():
            widget.destroy()

        query = self.search_var.get().strip().lower()

        filtered = [
            item for item in self.expenses
            if query in " ".join(str(v) for v in item.values()).lower()
        ]

        filtered.sort(
            key=lambda e: e.get("date", ""), reverse=True
        )

        self.create_tree(
            self.transaction_container,
            [
                ("date", "DATE", 105),
                ("title", "DESCRIPTION", 200),
                ("category", "CATEGORY", 125),
                ("amount", "AMOUNT", 125),
            ],
            filtered
        ).pack(fill="both", expand=True, padx=8, pady=8)

    def delete_selected(self):
        selection = self.transaction_container.winfo_children()[0]
        tree = selection.winfo_children()[0]
        selected = tree.selection()

        if not selected:
            messagebox.showinfo(
                "Select transaction", "Choose a transaction first."
            )
            return

        record_id = int(selected[0])
        record = next(
            (e for e in self.expenses if e["id"] == record_id),
            None
        )

        if not record:
            return

        if not messagebox.askyesno(
            "Confirm deletion",
            f"Delete '{record['title']}' ({money(record['amount'])})?"
        ):
            return

        index = self.expenses.index(record)
        self.expenses.pop(index)

        try:
            save_json(EXPENSE_FILE, self.expenses)
        except OSError as error:
            self.expenses.insert(index, record)
            messagebox.showerror("Save failed", str(error))
            return

        self.refresh_transactions()
        messagebox.showinfo("Deleted", "Transaction deleted successfully.")

    # -----------------------------------------------------
    # ADD EXPENSE DIALOG
    # -----------------------------------------------------

    def add_expense(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Expense")
        dialog.geometry("470x570")
        dialog.resizable(False, False)
        dialog.configure(bg=WHITE)
        dialog.transient(self)
        dialog.grab_set()

        tk.Frame(dialog, bg=TEAL, height=6).pack(fill="x")

        body = tk.Frame(dialog, bg=WHITE)
        body.pack(fill="both", expand=True, padx=28, pady=23)

        self.label(
            body, "Add a new expense", 19, TEXT, True
        ).pack(anchor="w")

        self.label(
            body, "Record where your money goes.", 10, MUTED
        ).pack(anchor="w", pady=(4, 20))

        fields = {}

        def make_field(label_text, key, default=""):
            self.label(
                body, label_text, 10, TEXT, True
            ).pack(anchor="w", pady=(9, 5))

            entry = tk.Entry(
                body, font=("Segoe UI", 10),
                bg=BG, fg=TEXT,
                relief="flat", insertbackground=TEXT
            )
            entry.pack(fill="x", ipady=9)

            if default:
                entry.insert(0, default)

            fields[key] = entry

        make_field("Expense title *", "title")
        make_field("Amount in rupees *", "amount")

        self.label(
            body, "Category *", 10, TEXT, True
        ).pack(anchor="w", pady=(13, 5))

        category_var = tk.StringVar(value=CATEGORIES[0])
        category_box = ttk.Combobox(
            body, textvariable=category_var,
            values=CATEGORIES, state="readonly"
        )
        category_box.pack(fill="x")
        
        make_field("Date (YYYY-MM-DD)", "date", date.today().isoformat())
        make_field("Note (optional)", "note")

        def save_expense():
            title = fields["title"].get().strip()
            amount_text = fields["amount"].get().strip()
            expense_date = fields["date"].get().strip()
            note = fields["note"].get().strip()

            if not title:
                messagebox.showwarning(
                    "Missing title", "Enter an expense title.", parent=dialog
                )
                return

            try:
                amount = float(amount_text)
                if amount <= 0 or amount == float("inf") or amount != amount:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Invalid amount",
                    "Enter an amount greater than zero.",
                    parent=dialog
                )
                return

            try:
                parsed_date = datetime.strptime(
                    expense_date, "%Y-%m-%d"
                ).date()
                expense_date = parsed_date.isoformat()
            except ValueError:
                messagebox.showwarning(
                    "Invalid date",
                    "Use the date format YYYY-MM-DD.",
                    parent=dialog
                )
                return

            record = {
                "id": max(
                    (int(e.get("id", 0)) for e in self.expenses),
                    default=0
                ) + 1,
                "title": title,
                "amount": round(amount, 2),
                "category": category_var.get(),
                "date": expense_date,
                "note": note,
                "created_at": datetime.now().isoformat(timespec="seconds")
            }

            self.expenses.append(record)

            try:
                save_json(EXPENSE_FILE, self.expenses)
            except OSError as error:
                self.expenses.pop()
                messagebox.showerror(
                    "Save failed", str(error), parent=dialog
                )
                return

            dialog.destroy()
            self.navigate(self.current_page)
            messagebox.showinfo(
                "Expense saved",
                f"{title}\n{money(amount)}\n\nSaved successfully."
            )

        self.button(
            body, "Save Expense", save_expense, True
        ).pack(fill="x", pady=(20, 0))

    # -----------------------------------------------------
    # BUDGETS
    # -----------------------------------------------------

    def show_budgets(self):
        self.clear_content()

        self.section_heading(
            "Budget Planner",
            "Set monthly limits and keep your spending under control."
        )

        panel = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        panel.pack(fill="x", pady=(0, 18))

        inner = tk.Frame(panel, bg=WHITE)
        inner.pack(fill="x", padx=23, pady=23)

        self.label(
            inner, "Monthly Budget Settings", 14, TEXT, True
        ).pack(anchor="w", pady=(0, 16))

        form = tk.Frame(inner, bg=WHITE)
        form.pack(fill="x")

        month_var = tk.StringVar(
            value=date.today().strftime("%Y-%m")
        )
        budget_var = tk.StringVar()

        self.label(form, "Month (YYYY-MM)", 10, MUTED).grid(
            row=0, column=0, sticky="w", padx=(0, 12)
        )
        self.label(form, "Budget amount (₹)", 10, MUTED).grid(
            row=0, column=1, sticky="w", padx=(0, 12)
        )

        tk.Entry(
            form, textvariable=month_var,
            font=("Segoe UI", 11), relief="flat",
            bg=BG
        ).grid(row=1, column=0, sticky="ew", padx=(0, 12), ipady=10)

        tk.Entry(
            form, textvariable=budget_var,
            font=("Segoe UI", 11), relief="flat",
            bg=BG
        ).grid(row=1, column=1, sticky="ew", padx=(0, 12), ipady=10)

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        def save_budget():
            month = month_var.get().strip()
            try:
                datetime.strptime(month, "%Y-%m")
                amount = float(budget_var.get().strip())
                if amount <= 0 or amount == float("inf") or amount != amount:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Invalid input",
                    "Enter a valid month (YYYY-MM) and positive budget."
                )
                return

            old = self.budgets.get(month)
            self.budgets[month] = round(amount, 2)

            try:
                save_json(BUDGET_FILE, self.budgets)
            except OSError as error:
                if old is None:
                    self.budgets.pop(month, None)
                else:
                    self.budgets[month] = old

                messagebox.showerror("Save failed", str(error))
                return

            messagebox.showinfo(
                "Budget saved",
                f"Budget for {month}: {money(amount)}"
            )
            self.show_budgets()

        self.button(
            inner, "Save Monthly Budget", save_budget, True
        ).pack(anchor="w", pady=(18, 0))

        self.label(
            self.content, "Your Budgets", 14, TEXT, True, bg=BG
        ).pack(anchor="w", pady=(5, 13))

        for month, amount in sorted(self.budgets.items(), reverse=True):
            spent = self.total_spending(month)
            remaining = amount - spent
            ratio = spent / amount if amount else 0

            row = tk.Frame(
                self.content, bg=WHITE,
                highlightbackground=BORDER, highlightthickness=1
            )
            row.pack(fill="x", pady=5)

            info = tk.Frame(row, bg=WHITE)
            info.pack(fill="x", padx=18, pady=14)

            self.label(
                info, month, 11, TEXT, True
            ).pack(side="left")

            self.label(
                info, f"{money(spent)} / {money(amount)}",
                10, MUTED
            ).pack(side="right")

            bar = tk.Frame(info, bg=BORDER, height=8)
            bar.pack(fill="x", pady=(13, 7))
            bar.pack_propagate(False)

            tk.Frame(
                bar, bg=RED if ratio > 1 else TEAL
            ).place(relwidth=min(ratio, 1), relheight=1)

            status = (
                f"Over budget by {money(abs(remaining))}"
                if remaining < 0 else
                f"{money(remaining)} remaining"
            )

            self.label(
                info, status, 9, RED if remaining < 0 else TEAL
            ).pack(anchor="w")

    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    def show_analytics(self):
        self.clear_content()

        self.section_heading(
            "Spending Analytics",
            "Explore spending trends and category breakdowns for the last 6 months."
        )

        # Build six calendar months, including the current month.
        today = date.today()
        months = []
        year, month_num = today.year, today.month
        for _ in range(6):
            months.append(f"{year:04d}-{month_num:02d}")
            month_num -= 1
            if month_num == 0:
                month_num = 12
                year -= 1
        months.reverse()

        monthly_totals = {month: 0.0 for month in months}
        monthly_counts = {month: 0 for month in months}
        category_totals = defaultdict(float)

        for item in self.expenses:
            expense_month = item.get("date", "")[:7]
            try:
                amount = float(item.get("amount", 0))
            except (TypeError, ValueError):
                continue

            if expense_month in monthly_totals:
                monthly_totals[expense_month] += amount
                monthly_counts[expense_month] += 1
                category_totals[item.get("category", "Other")] += amount

        six_month_total = sum(monthly_totals.values())
        six_month_count = sum(monthly_counts.values())
        average_monthly = six_month_total / 6
        average_transaction = (
            six_month_total / six_month_count if six_month_count else 0
        )
        highest_month = max(monthly_totals, key=monthly_totals.get)
        highest_amount = monthly_totals[highest_month]

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 18))

        stats = [
            ("Last 6 Months", money(six_month_total), "Total recorded spending", TEAL),
            ("Monthly Average", money(average_monthly), "Average across 6 months", "#6485E8"),
            ("Transactions", str(six_month_count), "Transactions in this period", "#A277D5"),
            ("Highest Month", highest_month, money(highest_amount) + " spent", ORANGE),
        ]
        for index, stat in enumerate(stats):
            cards.grid_columnconfigure(index, weight=1)
            self.card(
                cards, stat[0], stat[1], stat[2], stat[3]
            ).grid(
                row=0, column=index, sticky="nsew",
                padx=(0 if index == 0 else 8, 0)
            )

        # Charts panel
        chart_panel = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        chart_panel.pack(fill="both", expand=True, pady=(0, 14))

        self.label(
            chart_panel, "6-Month Spending Trends", 13, TEXT, True
        ).pack(anchor="w", padx=18, pady=(15, 2))
        self.label(
            chart_panel,
            "Months with no recorded expenses are shown as ₹0. Charts use your saved expense records.",
            9, MUTED
        ).pack(anchor="w", padx=18, pady=(0, 6))

        # Match Matplotlib chart colors to the application's current theme.
        # This fixes black labels/titles becoming invisible in dark mode.
        chart_bg = WHITE
        chart_text = TEXT
        chart_muted = MUTED
        chart_grid = BORDER
        chart_bar = TEAL
        chart_edge = BORDER
        pie_text = TEXT
        percentage_text = "#FFFFFF" if self.theme_name == "dark" else "#FFFFFF"

        figure = Figure(figsize=(10, 3.8), dpi=100, facecolor=chart_bg)
        monthly_ax = figure.add_subplot(1, 2, 1, facecolor=chart_bg)
        category_ax = figure.add_subplot(1, 2, 2, facecolor=chart_bg)

        month_labels = []
        for month in months:
            try:
                month_labels.append(datetime.strptime(month, "%Y-%m").strftime("%b %Y"))
            except ValueError:
                month_labels.append(month)

        amounts = [monthly_totals[month] for month in months]
        bars = monthly_ax.bar(
            month_labels, amounts, color=chart_bar, width=0.65,
            edgecolor=chart_edge, linewidth=0.5
        )
        monthly_ax.set_title(
            "Expenses by Month", fontsize=11, pad=12,
            color=chart_text, fontweight="bold"
        )
        monthly_ax.set_ylabel("Amount (₹)", color=chart_text, fontsize=9)
        monthly_ax.tick_params(
            axis="x", labelrotation=25, labelsize=8, colors=chart_text
        )
        monthly_ax.tick_params(axis="y", labelsize=8, colors=chart_text)
        monthly_ax.grid(
            axis="y", linestyle="--", alpha=0.45, color=chart_grid
        )
        monthly_ax.set_axisbelow(True)
        for spine in monthly_ax.spines.values():
            spine.set_color(chart_edge)
        for bar, amount in zip(bars, amounts):
            if amount > 0:
                monthly_ax.annotate(
                    f"₹{amount:,.0f}",
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8,
                    color=chart_text, fontweight="bold"
                )

        if category_totals and sum(category_totals.values()) > 0:
            sorted_categories = sorted(
                category_totals.items(), key=lambda pair: pair[1], reverse=True
            )
            category_labels = [pair[0] for pair in sorted_categories]
            category_amounts = [pair[1] for pair in sorted_categories]
            category_colors = [
                CATEGORY_COLORS[
                    CATEGORIES.index(category) if category in CATEGORIES else 0
                ]
                for category in category_labels
            ]
            wedges, label_texts, percentage_texts = category_ax.pie(
                category_amounts,
                labels=category_labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=category_colors,
                textprops={"fontsize": 8, "color": pie_text},
                wedgeprops={"edgecolor": chart_bg, "linewidth": 1.5},
                pctdistance=0.65,
                labeldistance=1.10
            )
            # Keep category names readable outside the pie and percentages
            # readable on top of colored slices in both themes.
            for label in label_texts:
                label.set_color(chart_text)
                label.set_fontweight("bold")
            for percentage in percentage_texts:
                percentage.set_color(percentage_text)
                percentage.set_fontweight("bold")
                percentage.set_fontsize(8)
            category_ax.set_title(
                "Spending by Category (6 Months)", fontsize=11, pad=12,
                color=chart_text, fontweight="bold"
            )
            category_ax.set_aspect("equal")
        else:
            category_ax.text(
                0.5, 0.5, "No expense data\nfor the last 6 months",
                ha="center", va="center", fontsize=10, color=chart_muted
            )
            category_ax.set_title(
                "Spending by Category (6 Months)", fontsize=11, pad=12,
                color=chart_text, fontweight="bold"
            )
            category_ax.axis("off")

        # Set tick/label/title colors explicitly; Matplotlib otherwise uses
        # black defaults which are hard to see on the app's dark background.
        figure.tight_layout(pad=2.0)
        canvas = FigureCanvasTkAgg(figure, master=chart_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Six-month detail table
        table_panel = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        table_panel.pack(fill="x", pady=(0, 14))
        self.label(
            table_panel, "Monthly Breakdown", 13, TEXT, True
        ).pack(anchor="w", padx=18, pady=(14, 8))

        columns = [
            ("month", "MONTH", 150),
            ("transactions", "TRANSACTIONS", 140),
            ("amount", "TOTAL SPENT", 180),
            ("change", "VS PREVIOUS MONTH", 220),
        ]
        tree_container = tk.Frame(table_panel, bg=WHITE)
        tree_container.pack(fill="x", padx=12, pady=(0, 12))
        tree = ttk.Treeview(
            tree_container,
            columns=[column[0] for column in columns],
            show="headings",
            height=6
        )
        for key, heading, width in columns:
            tree.heading(key, text=heading)
            tree.column(key, width=width, minwidth=90, anchor="w")

        previous_amount = None
        for month in months:
            amount = monthly_totals[month]
            if previous_amount is None:
                change = "—"
            elif previous_amount == 0:
                change = "— (previous month ₹0)"
            else:
                percent = ((amount - previous_amount) / previous_amount) * 100
                change = f"{percent:+.1f}%"
            tree.insert(
                "", "end",
                values=(
                    month,
                    monthly_counts[month],
                    money(amount),
                    change
                )
            )
            previous_amount = amount

        tree.pack(fill="x")

        # Category summary for the six-month period
        category_panel = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        category_panel.pack(fill="x", pady=(0, 14))
        self.label(
            category_panel, "Category Totals (Last 6 Months)", 13, TEXT, True
        ).pack(anchor="w", padx=18, pady=(14, 8))

        if not category_totals:
            self.label(
                category_panel, "No expenses recorded in the last 6 months.",
                10, MUTED
            ).pack(anchor="w", padx=18, pady=(0, 15))
        else:
            total_categories = sum(category_totals.values())
            for category, amount in sorted(
                category_totals.items(), key=lambda pair: pair[1], reverse=True
            ):
                row = tk.Frame(category_panel, bg=WHITE)
                row.pack(fill="x", padx=18, pady=5)
                color = CATEGORY_COLORS[
                    CATEGORIES.index(category) if category in CATEGORIES else 0
                ]
                tk.Frame(row, bg=color, width=5, height=30).pack(side="left")
                self.label(row, category, 10, TEXT, True).pack(
                    side="left", padx=10
                )
                percent = amount / total_categories * 100 if total_categories else 0
                self.label(
                    row, f"{money(amount)}  •  {percent:.1f}%",
                    10, MUTED
                ).pack(side="right", padx=5)

        self.button(
            self.content, "Export All Expenses to CSV",
            self.export_csv, True
        ).pack(anchor="w", pady=(0, 8))

    # -----------------------------------------------------
    # CSV EXPORT
    # -----------------------------------------------------

    def export_csv(self):
        if not self.expenses:
            messagebox.showinfo(
                "No data", "Add some expenses before exporting."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Export expenses",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="expenses_export.csv"
        )

        if not path:
            return

        fields = [
            "id", "title", "amount", "category",
            "date", "note", "created_at"
        ]

        try:
            with open(
                path, "w", newline="", encoding="utf-8-sig"
            ) as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.expenses)

            messagebox.showinfo(
                "Export complete",
                f"Expenses exported successfully:\n{path}"
            )

        except OSError as error:
            messagebox.showerror("Export failed", str(error))


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    try:
        app = ExpenseTracker()
        app.mainloop()
    except (KeyboardInterrupt, EOFError):
        pass
