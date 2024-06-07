import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox

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
        self.add_employee_btn.clicked.connect(self.add_employee)
        layout.addWidget(self.add_employee_btn)

        self.add_machine_btn = QPushButton('Add Machine')
        self.add_machine_btn.clicked.connect(self.add_machine)
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

    def add_employee(self):
        # Implementation to add a new employee to the database
        pass

    def add_machine(self):
        # Implementation to add a new machine to the database
        pass

def main():
    app = QApplication(sys.argv)
    ex = AssignmentApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
