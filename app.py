import customtkinter as ctk
import csv
from datetime import datetime
import os

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Attendance Tracker")
        self.geometry("800x600")
        
        # Set the theme and color scheme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize data structures
        self.students = self.load_csv("students.csv")
        self.classrooms = self.load_csv("classrooms.csv")
        self.attendance = self.load_csv("attendance.csv")

        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_students = self.tabview.add("Students")
        self.tab_classrooms = self.tabview.add("Classrooms")
        self.tab_attendance = self.tabview.add("Mark Attendance")
        self.tab_report = self.tabview.add("Attendance Report")

        self.setup_students_tab()
        self.setup_classrooms_tab()
        self.setup_attendance_tab()
        self.setup_report_tab()

    def setup_students_tab(self):
        frame = ctk.CTkFrame(self.tab_students)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Add New Student", font=("Arial", 16, "bold")).pack(pady=10)

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="First Name")
        self.name_entry.pack(pady=5)

        self.surname_entry = ctk.CTkEntry(frame, placeholder_text="Last Name")
        self.surname_entry.pack(pady=5)

        add_button = ctk.CTkButton(frame, text="Add Student", command=self.add_student)
        add_button.pack(pady=10)

        self.students_list = ctk.CTkTextbox(frame, height=200)
        self.students_list.pack(pady=10, fill="both", expand=True)

        self.update_students_list()

    def setup_classrooms_tab(self):
        frame = ctk.CTkFrame(self.tab_classrooms)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Add New Module", font=("Arial", 16, "bold")).pack(pady=10)

        self.module_entry = ctk.CTkEntry(frame, placeholder_text="Module Name")
        self.module_entry.pack(pady=5)

        add_button = ctk.CTkButton(frame, text="Add Module", command=self.add_module)
        add_button.pack(pady=10)

        self.modules_list = ctk.CTkTextbox(frame, height=200)
        self.modules_list.pack(pady=10, fill="both", expand=True)

        self.update_modules_list()

    def setup_attendance_tab(self):
        frame = ctk.CTkFrame(self.tab_attendance)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Mark Attendance", font=("Arial", 16, "bold")).pack(pady=10)

        self.module_select = ctk.CTkOptionMenu(frame, values=self.get_modules())
        self.module_select.pack(pady=5)

        self.student_select = ctk.CTkOptionMenu(frame, values=self.get_students())
        self.student_select.pack(pady=5)

        mark_button = ctk.CTkButton(frame, text="Mark Present", command=self.mark_attendance)
        mark_button.pack(pady=10)

        self.attendance_list = ctk.CTkTextbox(frame, height=200)
        self.attendance_list.pack(pady=10, fill="both", expand=True)

        self.update_attendance_list()

    def setup_report_tab(self):
        frame = ctk.CTkFrame(self.tab_report)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Attendance Report", font=("Arial", 16, "bold")).pack(pady=10)

        self.report_student_select = ctk.CTkOptionMenu(frame, values=self.get_students())
        self.report_student_select.pack(pady=5)

        report_button = ctk.CTkButton(frame, text="Generate Report", command=self.generate_report)
        report_button.pack(pady=10)

        self.report_text = ctk.CTkTextbox(frame, height=300)
        self.report_text.pack(pady=10, fill="both", expand=True)

    def add_student(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        if name and surname:
            student_id = f"S{len(self.students) + 1:03d}"
            self.students.append([student_id, name, surname])
            self.save_csv("students.csv", self.students)
            self.update_students_list()
            self.name_entry.delete(0, 'end')
            self.surname_entry.delete(0, 'end')
            self.update_student_select()

    def add_module(self):
        module = self.module_entry.get()
        if module:
            module_id = f"M{len(self.classrooms) + 1:03d}"
            self.classrooms.append([module_id, module])
            self.save_csv("classrooms.csv", self.classrooms)
            self.update_modules_list()
            self.module_entry.delete(0, 'end')
            self.update_module_select()

    def mark_attendance(self):
        module = self.module_select.get()
        student = self.student_select.get()
        if module and student:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.attendance.append([module, student, timestamp])
            self.save_csv("attendance.csv", self.attendance)
            self.update_attendance_list()

    def generate_report(self):
        student = self.report_student_select.get()
        report = f"Attendance Report for {student}:\n\n"
        for record in self.attendance:
            if record[1] == student:
                report += f"Module: {record[0]}, Time: {record[2]}\n"
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", report)

    def update_students_list(self):
        self.students_list.delete("1.0", "end")
        for student in self.students:
            self.students_list.insert("end", f"{student[0]}: {student[1]} {student[2]}\n")

    def update_modules_list(self):
        self.modules_list.delete("1.0", "end")
        for module in self.classrooms:
            self.modules_list.insert("end", f"{module[0]}: {module[1]}\n")

    def update_attendance_list(self):
        self.attendance_list.delete("1.0", "end")
        for record in self.attendance:
            self.attendance_list.insert("end", f"{record[1]} - {record[0]} at {record[2]}\n")

    def update_student_select(self):
        self.student_select.configure(values=self.get_students())
        self.report_student_select.configure(values=self.get_students())

    def update_module_select(self):
        self.module_select.configure(values=self.get_modules())

    def get_students(self):
        return [f"{student[1]} {student[2]}" for student in self.students]

    def get_modules(self):
        return [module[1] for module in self.classrooms]

    def load_csv(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', newline='') as file:
            return list(csv.reader(file))

    def save_csv(self, filename, data):
        with open(filename, 'w', newline='') as file:
            csv.writer(file).writerows(data)

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()