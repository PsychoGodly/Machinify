import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QLabel, QLineEdit, QMessageBox

def initialize_db():
    conn = sqlite3.connect('assignment.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        IsAssigned BOOLEAN DEFAULT FALSE
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Machines (
        MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        MaxEmployees INTEGER NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Assignments (
        AssignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER,
        MachineID INTEGER,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
        FOREIGN KEY (MachineID) REFERENCES Machines(MachineID),
        UNIQUE (EmployeeID)
    )
    ''')

    conn.commit()
    conn.close()

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Employee Name:")
        self.name_input = QLineEdit()

        self.submit_button = QPushButton("Add")
        self.submit_button.clicked.connect(self.add_employee)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def add_employee(self):
        name = self.name_input.text()
        if name:
            conn = sqlite3.connect('assignment.db')
            c = conn.cursor()
            c.execute("INSERT INTO Employees (Name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            self.accept()  # Close the dialog

class AddMachineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Machine")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Machine Name:")
        self.name_input = QLineEdit()

        self.max_employees_label = QLabel("Max Employees:")
        self.max_employees_input = QLineEdit()

        self.submit_button = QPushButton("Add")
        self.submit_button.clicked.connect(self.add_machine)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.max_employees_label)
        self.layout.addWidget(self.max_employees_input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def add_machine(self):
        name = self.name_input.text()
        max_employees = self.max_employees_input.text()
        if name and max_employees.isdigit():
            conn = sqlite3.connect('assignment.db')
            c = conn.cursor()
            c.execute("INSERT INTO Machines (Name, MaxEmployees) VALUES (?, ?)", (name, int(max_employees)))
            conn.commit()
            conn.close()
            self.accept()  # Close the dialog

class AssignmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Employee Machine Assignment')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_data()

        self.add_employee_btn = QPushButton('Add Employee')
        self.add_employee_btn.clicked.connect(self.show_add_employee_dialog)
        layout.addWidget(self.add_employee_btn)

        self.add_machine_btn = QPushButton('Add Machine')
        self.add_machine_btn.clicked.connect(self.show_add_machine_dialog)
        layout.addWidget(self.add_machine_btn)

        self.setLayout(layout)

    def load_data(self):
        conn = sqlite3.connect('assignment.db')
        c = conn.cursor()

        c.execute('SELECT * FROM Employees')
        employees = c.fetchall()

        c.execute('SELECT * FROM Machines')
        machines = c.fetchall()

        c.execute('SELECT * FROM Assignments')
        assignments = c.fetchall()

        conn.close()

        self.table.setRowCount(len(employees))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Employee', 'Assigned Machine', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, employee in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(employee[1]))
            assigned_machine = next((m[1] for m in machines if any(a[2] == m[0] and a[1] == employee[0] for a in assignments)), 'None')
            self.table.setItem(row, 1, QTableWidgetItem(assigned_machine))
            self.table.setCellWidget(row, 2, QPushButton('Assign'))

    def show_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_():
            self.load_data()  # Reload data to reflect new entry

    def show_add_machine_dialog(self):
        dialog = AddMachineDialog(self)
        if dialog.exec_():
            self.load_data()  # Reload data to reflect new entry

def main():
    initialize_db()  # Ensure the database is initialized
    app = QApplication(sys.argv)
    ex = AssignmentApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
