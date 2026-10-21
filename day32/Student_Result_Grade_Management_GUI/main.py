"""
STUDENT RESULT & GRADE MANAGEMENT SYSTEM
Professional desktop GUI built with Python Tkinter.
Features: dashboard, student CRUD, search, grade calculation,
performance chart, JSON persistence, and CSV export.

Requires Python 3.10+ (standard library only).
Run: python main.py
"""

import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "students.json"
SUBJECTS = [
    "Python",
    "Mathematics",
    "English",
    "Computer Science",
    "Database Management",
]
PASS_MARK = 33
MAX_MARK = 100

# Theme
BG = "#F3F6FB"
SIDEBAR = "#172554"
SIDEBAR_HOVER = "#243B75"
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
TEXT = "#172033"
MUTED = "#64748B"
WHITE = "#FFFFFF"
BORDER = "#E2E8F0"
GREEN = "#15803D"
RED = "#B91C1C"
ORANGE = "#C2410C"


def calculate_result(marks):
    total = sum(float(marks.get(subject, 0)) for subject in SUBJECTS)
    maximum = len(SUBJECTS) * MAX_MARK
    percentage = total / maximum * 100 if maximum else 0
    passed = all(float(marks.get(subject, 0)) >= PASS_MARK for subject in SUBJECTS)

    if not passed:
        grade, status = "F", "FAIL"
    elif percentage >= 90:
        grade, status = "A+", "PASS"
    elif percentage >= 80:
        grade, status = "A", "PASS"
    elif percentage >= 70:
        grade, status = "B", "PASS"
    elif percentage >= 60:
        grade, status = "C", "PASS"
    elif percentage >= 50:
        grade, status = "D", "PASS"
    elif percentage >= 33:
        grade, status = "E", "PASS"
    else:
        grade, status = "F", "FAIL"

    return {
        "total": round(total, 2),
        "maximum": maximum,
        "percentage": round(percentage, 2),
        "grade": grade,
        "status": status,
    }


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Student data must be a list.")
        students = []
        seen = set()
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                sid = int(item["id"])
                name = str(item["name"]).strip()
                class_name = str(item.get("class", "")).strip()
                marks = {s: float(item.get("marks", {}).get(s, 0)) for s in SUBJECTS}
                if sid <= 0 or not name or sid in seen:
                    continue
                if any(m < 0 or m > MAX_MARK for m in marks.values()):
                    continue
                seen.add(sid)
                students.append({
                    "id": sid,
                    "name": name,
                    "class": class_name or "Not specified",
                    "marks": marks,
                })
            except (KeyError, TypeError, ValueError):
                continue
        return students
    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showwarning(
            "Data warning",
            f"Could not read students.json. Starting with an empty list.\n\n{error}"
        )
        return []


def save_students(students):
    try:
        temp_file = DATA_FILE.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        temp_file.replace(DATA_FILE)
        return True
    except OSError as error:
        messagebox.showerror("Save error", f"Could not save student records:\n{error}")
        return False


class StudentDialog(tk.Toplevel):
    def __init__(self, parent, existing=None, existing_ids=None):
        super().__init__(parent)
        self.parent = parent
        self.existing = existing
        self.existing_ids = set(existing_ids or [])
        if existing:
            self.existing_ids.discard(existing["id"])
        self.result = None
        self.title("Edit Student" if existing else "Add Student")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        outer = ttk.Frame(self, padding=22, style="Dialog.TFrame")
        outer.pack(fill="both", expand=True)

        title = "Edit student record" if existing else "Add a new student"
        ttk.Label(outer, text=title, style="DialogTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 4)
        )
        ttk.Label(
            outer,
            text="Enter student details and marks for all five subjects.",
            style="Muted.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 18))

        self.id_var = tk.StringVar(value=str(existing["id"]) if existing else "")
        self.name_var = tk.StringVar(value=existing["name"] if existing else "")
        self.class_var = tk.StringVar(value=existing["class"] if existing else "")
        self.mark_vars = {
            subject: tk.StringVar(
                value=str(existing["marks"].get(subject, 0)) if existing else ""
            )
            for subject in SUBJECTS
        }

        self._field(outer, "Student ID", self.id_var, 2)
        self._field(outer, "Full name", self.name_var, 3)
        self._field(outer, "Class / Course", self.class_var, 4)

        ttk.Label(outer, text="SUBJECT MARKS", style="Section.TLabel").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(14, 7)
        )
        for row, subject in enumerate(SUBJECTS, start=6):
            ttk.Label(outer, text=subject, style="Body.TLabel").grid(
                row=row, column=0, sticky="w", pady=5, padx=(0, 20)
            )
            entry = ttk.Entry(outer, textvariable=self.mark_vars[subject], width=18)
            entry.grid(row=row, column=1, sticky="ew", pady=4)

        buttons = ttk.Frame(outer, style="Dialog.TFrame")
        buttons.grid(row=11, column=0, columnspan=2, sticky="e", pady=(20, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save student", style="Primary.TButton", command=self._save).pack(side="right")

        self.bind("<Escape>", lambda _event: self.destroy())
        self.bind("<Return>", lambda _event: self._save())
        self.update_idletasks()
        x = parent.winfo_rootx() + max(0, (parent.winfo_width() - self.winfo_width()) // 2)
        y = parent.winfo_rooty() + max(0, (parent.winfo_height() - self.winfo_height()) // 2)
        self.geometry(f"+{x}+{y}")
        self.wait_visibility()
        self.focus_set()

    def _field(self, parent, label, variable, row):
        ttk.Label(parent, text=label, style="Body.TLabel").grid(
            row=row, column=0, sticky="w", pady=5, padx=(0, 20)
        )
        ttk.Entry(parent, textvariable=variable, width=30).grid(
            row=row, column=1, sticky="ew", pady=4
        )

    def _save(self):
        try:
            student_id = int(self.id_var.get().strip())
            if student_id <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid ID", "Student ID must be a positive whole number.", parent=self)
            return

        name = self.name_var.get().strip()
        class_name = self.class_var.get().strip()
        if not name or not class_name:
            messagebox.showerror("Missing details", "Enter both the student's name and class/course.", parent=self)
            return
        if student_id in self.existing_ids:
            messagebox.showerror("Duplicate ID", "That student ID already exists.", parent=self)
            return

        marks = {}
        for subject, variable in self.mark_vars.items():
            try:
                mark = float(variable.get().strip())
                if not 0 <= mark <= MAX_MARK:
                    raise ValueError
                marks[subject] = mark
            except ValueError:
                messagebox.showerror(
                    "Invalid marks",
                    f"Enter a number from 0 to 100 for {subject}.",
                    parent=self,
                )
                return

        self.result = {
            "id": student_id,
            "name": name,
            "class": class_name,
            "marks": marks,
        }
        self.destroy()


class StudentManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Result & Grade Management System")
        self.geometry("1280x800")
        self.minsize(1050, 680)
        self.configure(bg=BG)
        self.students = load_students()
        self.search_var = tk.StringVar()
        self.current_page = "Dashboard"
        self._setup_styles()
        self._build_layout()
        self.show_page("Dashboard")

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=WHITE, relief="flat")
        style.configure("Dialog.TFrame", background=WHITE)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Body.TLabel", background=WHITE, foreground=TEXT)
        style.configure("Muted.TLabel", background=WHITE, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("DialogTitle.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 18, "bold"))
        style.configure("PageTitle.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 23, "bold"))
        style.configure("PageSubtitle.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=WHITE, foreground=MUTED, font=("Segoe UI", 9, "bold"))
        style.configure("Metric.TLabel", background=WHITE, foreground=TEXT, font=("Segoe UI", 24, "bold"))
        style.configure("MetricCaption.TLabel", background=WHITE, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("TButton", padding=(12, 8), font=("Segoe UI", 9, "bold"))
        style.configure("Primary.TButton", background=PRIMARY, foreground=WHITE, borderwidth=0)
        style.map("Primary.TButton", background=[("active", PRIMARY_DARK), ("pressed", PRIMARY_DARK)])
        style.configure("Secondary.TButton", background="#E8EFFD", foreground=PRIMARY, borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#D7E4FC")])
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT,
                        rowheight=36, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#F1F5F9", foreground="#475569",
                        font=("Segoe UI", 9, "bold"), relief="flat", padding=10)
        style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", TEXT)])
        style.configure("TEntry", padding=9, fieldbackground=WHITE)
        style.configure("Vertical.TScrollbar", background="#E2E8F0", troughcolor=WHITE, borderwidth=0)

    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(25, 30))
        tk.Label(brand, text="SR", bg=PRIMARY, fg=WHITE, font=("Segoe UI", 15, "bold"),
                 width=3, height=1).pack(side="left", padx=(0, 10))
        brand_text = tk.Frame(brand, bg=SIDEBAR)
        brand_text.pack(side="left")
        tk.Label(brand_text, text="STUDENT", bg=SIDEBAR, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="RESULT MANAGER", bg=SIDEBAR, fg="#A5B4FC",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(2, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=SIDEBAR, fg="#94A3B8",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=24, pady=(0, 10))

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "▦"),
            ("Students", "♙"),
            ("Performance", "▤"),
        ]
        for name, symbol in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"   {symbol}    {name}",
                anchor="w",
                bg=SIDEBAR,
                fg="#DCE5F7",
                activebackground=SIDEBAR_HOVER,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                padx=15,
                pady=13,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                command=lambda page=name: self.show_page(page),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[name] = btn

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=22, pady=22)
        tk.Frame(bottom, bg="#334155", height=1).pack(fill="x", pady=(0, 14))
        tk.Label(bottom, text="PYTHON DESKTOP PROJECT", bg=SIDEBAR, fg="#94A3B8",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(bottom, text="Local JSON storage", bg=SIDEBAR, fg="#CBD5E1",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.main_area, bg=WHITE, height=62)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        tk.Label(self.topbar, text="Student Administration", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=28)
        self.top_status = tk.Label(self.topbar, text="●  Local data ready", bg=WHITE,
                                   fg=GREEN, font=("Segoe UI", 9))
        self.top_status.pack(side="right", padx=28)

        self.content = tk.Frame(self.main_area, bg=BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=24)

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _page_heading(self, title, subtitle):
        header = tk.Frame(self.content, bg=BG)
        header.pack(fill="x", pady=(0, 22))
        left = tk.Frame(header, bg=BG)
        left.pack(side="left", fill="x", expand=True)
        ttk.Label(left, text=title, style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(left, text=subtitle, style="PageSubtitle.TLabel").pack(anchor="w", pady=(5, 0))
        return header

    def _card(self, parent, title, value, caption, accent):
        frame = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 12))
        top = tk.Frame(frame, bg=WHITE)
        top.pack(fill="x", padx=18, pady=(16, 0))
        tk.Frame(top, bg=accent, width=4, height=26).pack(side="left", padx=(0, 9))
        tk.Label(top, text=title.upper(), bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Label(frame, text=value, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 25, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        tk.Label(frame, text=caption, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 17))
        return frame

    def show_page(self, page):
        self.current_page = page
        for name, button in self.nav_buttons.items():
            button.configure(bg=PRIMARY if name == page else SIDEBAR)
        self._clear_content()
        if page == "Dashboard":
            self._dashboard_page()
        elif page == "Students":
            self._students_page()
        elif page == "Performance":
            self._performance_page()

    def _dashboard_page(self):
        self._page_heading(
            "Dashboard",
            "Overview of student records, academic results, and class performance."
        )
        results = [(s, calculate_result(s["marks"])) for s in self.students]
        count = len(results)
        passed = sum(1 for _, r in results if r["status"] == "PASS")
        failed = count - passed
        average = sum(r["percentage"] for _, r in results) / count if count else 0
        pass_rate = passed / count * 100 if count else 0

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x")
        self._card(cards, "Total students", str(count), "Records in your database", PRIMARY)
        self._card(cards, "Passed", str(passed), f"{pass_rate:.1f}% pass rate", GREEN)
        self._card(cards, "Failed", str(failed), "Needs academic attention", RED)
        self._card(cards, "Class average", f"{average:.1f}%", "Average percentage", ORANGE)

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True, pady=(22, 0))

        chart_card = tk.Frame(lower, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 14))
        tk.Label(chart_card, text="Grade distribution", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(18, 0))
        tk.Label(chart_card, text="Number of students by final grade", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(4, 0))
        canvas = tk.Canvas(chart_card, bg=WHITE, height=255, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=15, pady=12)
        self._draw_grade_chart(canvas)

        quick = tk.Frame(lower, bg=WHITE, width=270, highlightbackground=BORDER, highlightthickness=1)
        quick.pack(side="right", fill="y")
        quick.pack_propagate(False)
        tk.Label(quick, text="Quick actions", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(18, 5))
        tk.Label(quick, text="Manage your student records", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(0, 18))
        ttk.Button(quick, text="+  Add new student", style="Primary.TButton",
                   command=self.add_student).pack(fill="x", padx=18, pady=5)
        ttk.Button(quick, text="View student directory", style="Secondary.TButton",
                   command=lambda: self.show_page("Students")).pack(fill="x", padx=18, pady=5)
        ttk.Button(quick, text="Performance report", style="Secondary.TButton",
                   command=lambda: self.show_page("Performance")).pack(fill="x", padx=18, pady=5)
        ttk.Button(quick, text="Export results to CSV", style="Secondary.TButton",
                   command=self.export_csv).pack(fill="x", padx=18, pady=5)

        recent_card = tk.Frame(self.content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        recent_card.pack(fill="x", pady=(20, 0))
        row = tk.Frame(recent_card, bg=WHITE)
        row.pack(fill="x", padx=18, pady=15)
        tk.Label(row, text="Recently added students", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Button(row, text="View all", style="Secondary.TButton",
                   command=lambda: self.show_page("Students")).pack(side="right")
        recent = sorted(self.students, key=lambda s: s["id"], reverse=True)[:4]
        if not recent:
            tk.Label(recent_card, text="No student records yet. Add your first student to get started.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(0, 18))
        else:
            for student in recent:
                r = calculate_result(student["marks"])
                line = tk.Frame(recent_card, bg=WHITE)
                line.pack(fill="x", padx=18, pady=6)
                tk.Label(line, text=student["name"], bg=WHITE, fg=TEXT,
                         font=("Segoe UI", 9, "bold"), width=24, anchor="w").pack(side="left")
                tk.Label(line, text=student["class"], bg=WHITE, fg=MUTED,
                         font=("Segoe UI", 9), width=20, anchor="w").pack(side="left")
                tk.Label(line, text=f"{r['percentage']:.1f}%  ·  {r['grade']}",
                         bg=WHITE, fg=GREEN if r["status"] == "PASS" else RED,
                         font=("Segoe UI", 9, "bold")).pack(side="right")

    def _draw_grade_chart(self, canvas):
        canvas.delete("all")
        grades = ["A+", "A", "B", "C", "D", "E", "F"]
        counts = {g: 0 for g in grades}
        for student in self.students:
            grade = calculate_result(student["marks"])["grade"]
            counts[grade] = counts.get(grade, 0) + 1

        def draw(_event=None):
            canvas.delete("all")
            width = max(canvas.winfo_width(), 350)
            height = max(canvas.winfo_height(), 220)
            left, right, top, bottom = 35, width - 15, 20, height - 38
            chart_h = bottom - top
            max_count = max(counts.values()) if counts else 0
            max_count = max(max_count, 1)
            for i in range(4):
                y = bottom - chart_h * i / 3
                canvas.create_line(left, y, right, y, fill="#E9EEF5")
                canvas.create_text(left - 10, y, text=str(round(max_count * i / 3)),
                                   fill=MUTED, font=("Segoe UI", 8), anchor="e")
            slot = (right - left) / len(grades)
            colors = [PRIMARY, "#3B82F6", "#0D9488", "#16A34A", "#D97706", "#EA580C", "#DC2626"]
            for i, grade in enumerate(grades):
                x_center = left + slot * (i + 0.5)
                bar_h = chart_h * counts[grade] / max_count
                canvas.create_rectangle(
                    x_center - slot * 0.24, bottom - bar_h,
                    x_center + slot * 0.24, bottom,
                    fill=colors[i], outline=""
                )
                canvas.create_text(x_center, bottom - bar_h - 12, text=str(counts[grade]),
                                   fill=TEXT, font=("Segoe UI", 8, "bold"))
                canvas.create_text(x_center, bottom + 17, text=grade,
                                   fill=MUTED, font=("Segoe UI", 9))
        canvas.bind("<Configure>", draw)
        self.after(80, draw)

    def _students_page(self):
        header = self._page_heading(
            "Student directory",
            "Add, search, edit, and manage student records and results."
        )
        ttk.Button(header, text="+  Add student", style="Primary.TButton",
                   command=self.add_student).pack(side="right", anchor="n")

        toolbar = tk.Frame(self.content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        toolbar.pack(fill="x", pady=(0, 14))
        search_box = tk.Frame(toolbar, bg=WHITE)
        search_box.pack(side="left", fill="x", expand=True, padx=14, pady=12)
        tk.Label(search_box, text="⌕", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 16)).pack(side="left", padx=(0, 8))
        search_entry = ttk.Entry(search_box, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda _event: self._populate_tree())
        ttk.Button(toolbar, text="Clear search", style="Secondary.TButton",
                   command=self._clear_search).pack(side="right", padx=14, pady=12)
        ttk.Button(toolbar, text="Export CSV", style="Secondary.TButton",
                   command=self.export_csv).pack(side="right", pady=12)

        table_card = tk.Frame(self.content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        columns = ("id", "name", "class", "total", "percentage", "grade", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": ("ID", 65),
            "name": ("Student name", 200),
            "class": ("Class / Course", 145),
            "total": ("Total / 500", 105),
            "percentage": ("Percentage", 105),
            "grade": ("Grade", 75),
            "status": ("Status", 85),
        }
        for col, (label, width) in headings.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, minwidth=55, anchor="w" if col == "name" else "center")
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=10)
        self.tree.tag_configure("pass", foreground=GREEN)
        self.tree.tag_configure("fail", foreground=RED)
        self.tree.bind("<Double-1>", lambda _event: self.view_selected())

        footer = tk.Frame(self.content, bg=BG)
        footer.pack(fill="x", pady=(12, 0))
        ttk.Button(footer, text="View result", style="Secondary.TButton",
                   command=self.view_selected).pack(side="left", padx=(0, 8))
        ttk.Button(footer, text="Edit selected", style="Secondary.TButton",
                   command=self.edit_student).pack(side="left", padx=(0, 8))
        ttk.Button(footer, text="Delete selected", style="Secondary.TButton",
                   command=self.delete_student).pack(side="left")
        self.table_count = tk.Label(footer, text="", bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self.table_count.pack(side="right")
        self._populate_tree()
        search_entry.focus_set()

    def _clear_search(self):
        self.search_var.set()
        self._populate_tree()

    def _populate_tree(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        query = self.search_var.get().strip().casefold()
        filtered = [
            s for s in self.students
            if query in str(s["id"]).casefold()
            or query in s["name"].casefold()
            or query in s["class"].casefold()
        ]
        filtered.sort(key=lambda s: (s["name"].casefold(), s["id"]))
        for student in filtered:
            result = calculate_result(student["marks"])
            self.tree.insert(
                "", "end", iid=str(student["id"]),
                values=(
                    student["id"], student["name"], student["class"],
                    f"{result['total']:.1f}",
                    f"{result['percentage']:.2f}%",
                    result["grade"], result["status"]
                ),
                tags=("pass" if result["status"] == "PASS" else "fail",)
            )
        if hasattr(self, "table_count") and self.table_count.winfo_exists():
            self.table_count.configure(text=f"{len(filtered)} of {len(self.students)} students")

    def _selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select student", "Select a student from the table first.")
            return None
        sid = int(selected[0])
        return next((s for s in self.students if s["id"] == sid), None)

    def add_student(self):
        dialog = StudentDialog(self, existing_ids=[s["id"] for s in self.students])
        self.wait_window(dialog)
        if dialog.result:
            self.students.append(dialog.result)
            if save_students(self.students):
                self.show_page("Students")
                self.top_status.configure(text="●  Changes saved", fg=GREEN)
            else:
                self.students.pop()

    def edit_student(self):
        student = self._selected_student()
        if not student:
            return
        dialog = StudentDialog(
            self,
            existing=student,
            existing_ids=[s["id"] for s in self.students]
        )
        self.wait_window(dialog)
        if dialog.result:
            index = self.students.index(student)
            old = self.students[index]
            self.students[index] = dialog.result
            if save_students(self.students):
                self.show_page("Students")
                self.top_status.configure(text="●  Changes saved", fg=GREEN)
            else:
                self.students[index] = old

    def delete_student(self):
        student = self._selected_student()
        if not student:
            return
        if not messagebox.askyesno(
            "Confirm deletion",
            f"Delete {student['name']} (ID {student['id']})?\nThis cannot be undone."
        ):
            return
        index = self.students.index(student)
        removed = self.students.pop(index)
        if save_students(self.students):
            self.show_page("Students")
            self.top_status.configure(text="●  Changes saved", fg=GREEN)
        else:
            self.students.insert(index, removed)

    def view_selected(self):
        student = self._selected_student()
        if not student:
            return
        result = calculate_result(student["marks"])
        dialog = tk.Toplevel(self)
        dialog.title("Student result")
        dialog.configure(bg=WHITE)
        dialog.transient(self)
        dialog.resizable(False, False)
        frame = tk.Frame(dialog, bg=WHITE, padx=25, pady=22)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="STUDENT RESULT REPORT", bg=WHITE, fg=PRIMARY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(frame, text=student["name"], bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(6, 2))
        tk.Label(frame, text=f"ID {student['id']}   •   {student['class']}",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 15))
        for subject in SUBJECTS:
            line = tk.Frame(frame, bg=WHITE)
            line.pack(fill="x", pady=4)
            tk.Label(line, text=subject, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10), width=28, anchor="w").pack(side="left")
            tk.Label(line, text=f"{student['marks'][subject]:g} / 100", bg=WHITE,
                     fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="right")
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=12)
        for label, value in [
            ("Total", f"{result['total']:g} / {result['maximum']}"),
            ("Percentage", f"{result['percentage']:.2f}%"),
            ("Grade", result["grade"]),
            ("Result", result["status"]),
        ]:
            line = tk.Frame(frame, bg=WHITE)
            line.pack(fill="x", pady=3)
            tk.Label(line, text=label, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 10)).pack(side="left")
            tk.Label(line, text=value, bg=WHITE,
                     fg=GREEN if label == "Result" and value == "PASS" else
                        RED if label == "Result" else TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="right")
        ttk.Button(frame, text="Close", style="Primary.TButton",
                   command=dialog.destroy).pack(anchor="e", pady=(18, 0))
        dialog.update_idletasks()
        dialog.geometry(f"+{self.winfo_rootx() + 250}+{self.winfo_rooty() + 100}")

    def _performance_page(self):
        self._page_heading(
            "Performance analytics",
            "Class-wide statistics, grade distribution, and highest-performing students."
        )
        count = len(self.students)
        results = [(s, calculate_result(s["marks"])) for s in self.students]
        passed = sum(1 for _, r in results if r["status"] == "PASS")
        average = sum(r["percentage"] for _, r in results) / count if count else 0
        topper = max(results, key=lambda item: item[1]["percentage"]) if results else None

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x")
        self._card(cards, "Students assessed", str(count), "Total student records", PRIMARY)
        self._card(cards, "Pass rate", f"{passed / count * 100:.1f}%" if count else "0.0%",
                   f"{passed} students passed", GREEN)
        self._card(cards, "Average result", f"{average:.1f}%", "Mean student percentage", ORANGE)
        self._card(cards, "Highest score", f"{topper[1]['percentage']:.1f}%" if topper else "—",
                   topper[0]["name"] if topper else "No records yet", PRIMARY)

        chart_card = tk.Frame(self.content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        chart_card.pack(fill="both", expand=True, pady=(22, 0))
        tk.Label(chart_card, text="Grade distribution", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=22, pady=(18, 0))
        canvas = tk.Canvas(chart_card, bg=WHITE, height=270, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=15)
        self._draw_grade_chart(canvas)

        table_card = tk.Frame(self.content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        table_card.pack(fill="x", pady=(18, 0))
        tk.Label(table_card, text="Top performers", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(15, 8))
        ranked = sorted(results, key=lambda item: item[1]["percentage"], reverse=True)[:5]
        if not ranked:
            tk.Label(table_card, text="Add student records to see the ranking.",
                     bg=WHITE, fg=MUTED).pack(anchor="w", padx=20, pady=(0, 18))
        else:
            for rank, (student, result) in enumerate(ranked, start=1):
                line = tk.Frame(table_card, bg=WHITE)
                line.pack(fill="x", padx=20, pady=5)
                tk.Label(line, text=f"{rank:02d}", bg="#EFF6FF", fg=PRIMARY,
                         font=("Segoe UI", 9, "bold"), width=4, pady=4).pack(side="left", padx=(0, 12))
                tk.Label(line, text=student["name"], bg=WHITE, fg=TEXT,
                         font=("Segoe UI", 9, "bold"), width=24, anchor="w").pack(side="left")
                tk.Label(line, text=student["class"], bg=WHITE, fg=MUTED,
                         font=("Segoe UI", 9), width=18, anchor="w").pack(side="left")
                tk.Label(line, text=f"{result['percentage']:.2f}%   Grade {result['grade']}",
                         bg=WHITE, fg=GREEN if result["status"] == "PASS" else RED,
                         font=("Segoe UI", 9, "bold")).pack(side="right")
            tk.Frame(table_card, bg=WHITE, height=12).pack()

    def export_csv(self):
        if not self.students:
            messagebox.showinfo("No records", "Add at least one student before exporting.")
            return
        path = filedialog.asksaveasfilename(
            title="Export student results",
            defaultextension=".csv",
            initialfile="student_results.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        fields = ["id", "name", "class", *SUBJECTS, "total", "maximum", "percentage", "grade", "status"]
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                for student in self.students:
                    result = calculate_result(student["marks"])
                    writer.writerow({
                        "id": student["id"],
                        "name": student["name"],
                        "class": student["class"],
                        **student["marks"],
                        **result,
                    })
            messagebox.showinfo("Export complete", f"Results exported successfully:\n{path}")
            self.top_status.configure(text="●  CSV exported", fg=GREEN)
        except OSError as error:
            messagebox.showerror("Export error", f"Could not export CSV:\n{error}")


if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()
