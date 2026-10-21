# Student Result & Grade Management System

A desktop GUI application built with Python Tkinter for managing student records and academic results.

## Features
- Dashboard with total students, pass/fail counts, and class average
- Student add, edit, delete, view, and search
- Marks entry for five subjects
- Automatic total, percentage, grade, and pass/fail calculation
- Grade distribution chart and top performers
- JSON data persistence
- CSV export compatible with spreadsheet software
- Input validation and error messages

## Requirements
- Python 3.10 or later
- No third-party packages required (Tkinter is usually included with Python)

## Run
Open a terminal in this folder and run:

```bash
python main.py
```

On Windows, if `python` is not recognized, try:

```bash
py main.py
```

## Files
- `main.py` — application source code
- `students.json` — created automatically when student records are saved
- `student_results.csv` — created when you export results
- `screenshots/` — place screenshots of your running application here

## Grading rules
A student must score at least 33/100 in every subject to pass.
- A+: 90% and above
- A: 80% to below 90%
- B: 70% to below 80%
- C: 60% to below 70%
- D: 50% to below 60%
- E: 33% to below 50%
- F: Below 33% overall or failure in any subject

## Suggested testing
1. Add a student with valid marks.
2. Try a duplicate student ID.
3. Try invalid marks (negative or above 100).
4. Search by ID, name, and class.
5. Edit a student's marks and check the recalculated grade.
6. Delete a record after confirmation.
7. Check performance metrics and grade chart.
8. Export CSV and open it in Excel.
9. Close and reopen the app to verify JSON persistence.

## Notes
This is an educational local desktop application. For real school use, add user authentication, role-based permissions, backups, and stronger privacy controls.
