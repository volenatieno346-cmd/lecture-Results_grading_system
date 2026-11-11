import tkinter as tk
from tkinter import messagebox, ttk

from grademanagement import GradeManager
from db import Database

grade_manager = GradeManager()
db = Database()

PLACEHOLDERS = {
    "reg_number": "Enter registration number",
    "name": "Enter student name",
    "cat1": "Enter CAT 1 score",
    "cat2": "Enter CAT 2 score",
    "exam": "Enter exam score",
}

create_table_query = """
CREATE TABLE IF NOT EXISTS students (
    reg_number TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    cat1 INTEGER NOT NULL,
    cat2 INTEGER NOT NULL,
    exam INTEGER NOT NULL,
    total INTEGER NOT NULL,
    grade TEXT NOT NULL
)
"""
db.execute_query(create_table_query)


def show_message(message):
    messagebox.showinfo("Student Results", message)


def add_student():
    reg_number = entry_reg_number.get().strip()
    name = entry_name.get().strip()
    cat1_score = entry_cat1.get().strip()
    cat2_score = entry_cat2.get().strip()
    exam_score = entry_exam.get().strip()

    if (
        not reg_number
        or reg_number == PLACEHOLDERS["reg_number"]
        or not name
        or name == PLACEHOLDERS["name"]
        or not cat1_score
        or cat1_score == PLACEHOLDERS["cat1"]
        or not cat2_score
        or cat2_score == PLACEHOLDERS["cat2"]
        or not exam_score
        or exam_score == PLACEHOLDERS["exam"]
    ):
        show_message("Please fill in all fields.")
        return
    if not cat1_score.isdigit() or not cat2_score.isdigit() or not exam_score.isdigit():
        show_message("Scores must be numeric.")
        return
    if not (int(cat1_score) >= 0 and int(cat1_score) <= 40) or not (int(cat2_score) >= 0 and int(cat2_score) <= 40) or not (int(exam_score) >= 0 and int(exam_score) <= 60):
        show_message("Scores must be between 0 and their respective maximum values.")
        return

    grade_manager.add_student(
        reg_number,
        name,
        int(cat1_score),
        int(cat2_score),
        int(exam_score),
    )
    grade_manager.calculate_total()
    grade_manager.grading()
    grade = grade_manager.students[-1]["grade"]
    
    addingQuery = "INSERT INTO students (reg_number, name, cat1, cat2, exam, total, grade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (reg_number, name, int(cat1_score), int(cat2_score), int(exam_score), grade_manager.students[-1]["total"], grade)
    db.execute_query(addingQuery, params)
    display_students()
    show_message(f"Student added: {reg_number}, {name}, CAT1: {cat1_score}, CAT2: {cat2_score}, Exam: {exam_score}")
    show_message(f"Total: {grade_manager.students[-1]['total']}/100, Grade: {grade}")


def display_students():
    query = """
    SELECT reg_number, name, cat1, cat2, exam, total, grade
    FROM students
    ORDER BY total DESC
    """
    students = db.fetch_results(query)

    for item in results_table.get_children():
        results_table.delete(item)

    if not students:
        results_table.insert(
            "",
            tk.END,
            values=("No student records found.", "", "", "", "", "", ""),
        )
        return

    for student in students:
        results_table.insert(
            "",
            tk.END,
            values=student,
        )


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(_event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(_event):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


root = tk.Tk()
root.title("Marks entry and grading system")
root.geometry("950x600")

tk.Label(root, text="Student Result Handler").pack(pady=5)

entry_reg_number = tk.Entry(root, width=30)
entry_reg_number.pack()
add_placeholder(entry_reg_number, PLACEHOLDERS["reg_number"])

entry_name = tk.Entry(root, width=30)
entry_name.pack()
add_placeholder(entry_name, PLACEHOLDERS["name"])

entry_cat1 = tk.Entry(root, width=30)
entry_cat1.pack()
add_placeholder(entry_cat1, PLACEHOLDERS["cat1"])

entry_cat2 = tk.Entry(root, width=30)
entry_cat2.pack()
add_placeholder(entry_cat2, PLACEHOLDERS["cat2"])

entry_exam = tk.Entry(root, width=30)
entry_exam.pack()
add_placeholder(entry_exam, PLACEHOLDERS["exam"])

table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("reg_number", "name", "cat1", "cat2", "exam", "total", "grade")
results_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
)

headings = {
    "reg_number": "Registration Number",
    "name": "Student Name",
    "cat1": "CAT 1",
    "cat2": "CAT 2",
    "exam": "Exam",
    "total": "Total",
    "grade": "Grade",
}
column_widths = {
    "reg_number": 180,
    "name": 160,
    "cat1": 80,
    "cat2": 80,
    "exam": 80,
    "total": 90,
    "grade": 80,
}
for column in columns:
    results_table.heading(column, text=headings[column])
    results_table.column(column, width=column_widths[column], anchor=tk.CENTER)

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=results_table.yview,
)
horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.HORIZONTAL,
    command=results_table.xview,
)
results_table.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set,
)

results_table.grid(row=0, column=0, sticky="nsew")
vertical_scrollbar.grid(row=0, column=1, sticky="ns")
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)


button_add_student = tk.Button(root, text="Add Student", command=lambda: add_student())
button_add_student.pack(pady=5)

button_display_students = tk.Button(
    root, text="Display saved students", command=display_students
)
button_display_students.pack(pady=5)

button_high_student = tk.Button(root, text="SEE POS ONE", command=lambda: grade_manager.HighestStudent())
button_high_student.pack(pady=5)

root.mainloop()
