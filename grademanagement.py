test_results = [
    {
        "reg-number": "TEST-001",
        "name": "Test Student",
        "Cat 1": 12,
        "cat2": 15,
        "exam": 56,
    }
]


class GradeManager:
    def __init__(self):
        self.students = []

    def _results_to_use(self):
        return self.students if self.students else test_results

    def add_student(self, reg_number, name, cat1, cat2, exam):
        self.students.append(
            {
                "reg-number": reg_number,
                "name": name,
                "Cat 1": cat1,
                "cat2": cat2,
                "exam": exam,
            }
        )

    def calculate_total(self):
        for student in self._results_to_use():
            student["total"] = (student["Cat 1"] + student["cat2"] )/2+ student["exam"]

    def grading(self):
        for student in self._results_to_use():
            score = student["total"]
            if score >= 70:
                student["grade"] = "A"
            elif score >= 60:
                student["grade"] = "B"
            elif score >= 50:
                student["grade"] = "C"
            elif score >= 40:
                student["grade"] = "D"
            elif score >= 0:
                student["grade"] = "E"
            else:
                student["grade"] = "Invalid"

    def display(self):
        self.calculate_total()
        self.grading()

        for student in self._results_to_use():
            print("-" * 30)
            print(f"Registration Number: {student['reg-number']}")
            print(f"Name: {student['name']}")
            print(f"CAT 1: {student['Cat 1']}")
            print(f"CAT 2: {student['cat2']}")
            print(f"Exam: {student['exam']}")
            print(f"Total: {student['total']}/100")
            print(f"Grade: {student['grade']}")
    def HighestStudent(self):
        self.calculate_total()
        self.grading()
        highest_student = max(
            self._results_to_use(), key=lambda student: student["total"]
        )
        print("Highest Student:")
        print(f"Registration Number: {highest_student['reg-number']}")
        print(f"Name: {highest_student['name']}")
        print(f"Total: {highest_student['total']}/100")
        print(f"Grade: {highest_student['grade']}")


if __name__ == "__main__":
    grade_manager = GradeManager()

    choice=int(input("Choose an option: \n1 1.Enter student.\n2.Display student results." 
    "\n3.Average of the sudjects.\n4.Find the highest student.\n5.Exit.\n choice: "))
    match choice:
        case 1:
            grade_manager.add_student(
                input("Enter the registration number: "),
                input("Enter the student name: "),
                int(input("Enter CAT 1 score: ")),
                int(input("Enter CAT 2 score: ")),
                int(input("Enter exam score: ")),
            )
        case 2:
            grade_manager.display()
        case 3:
            grade_manager.calculate_total()
        case 4:
            grade_manager.HighestStudent()
        case 5:
            exit()
        case _:
            print("Invalid choice. Please try again.")

   
