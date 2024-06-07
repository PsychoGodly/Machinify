import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QMessageBox
import sqlite3

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Employee Name:")
        self.name_input = QLineEdit()

        self.job_label = QLabel("Job Title:")
        self.job_input = QLineEdit()

        self.submit_button = QPushButton("Add")
        self.submit_button.clicked.connect(self.add_employee)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.job_label)
        self.layout.addWidget(self.job_input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def add_employee(self):
        name = self.name_input.text()
        job = self.job_input.text()
        if name:
            conn = sqlite3.connect('assignment.db')
            c = conn.cursor()
            c.execute("INSERT INTO Employees (Name, JobTitle) VALUES (?, ?)", (name, job))
            conn.commit()
            conn.close()
            self.accept()  # Close the dialog

class EmployeeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Job Title", "Pointed", "Assigned", "Modify", "Delete"])
        
        layout.addWidget(self.table)
        
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.show_add_employee_dialog)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.load_data()
    
    def load_data(self):
        conn = sqlite3.connect('assignment.db')
        c = conn.cursor()

        c.execute('SELECT * FROM Employees')
        employees = c.fetchall()

        conn.close()

        self.table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            for col, value in enumerate(employee):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
                
            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(self.modify_employee)
            self.table.setCellWidget(row, 6, modify_button)
            
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete_employee)
            self.table.setCellWidget(row, 7, delete_button)

    def show_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_():
            self.load_data()
            
    def modify_employee(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            employee_id = int(self.table.item(row, 0).text())
            # Open dialog to modify employee with given employee_id
    
    def delete_employee(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            employee_id = int(self.table.item(row, 0).text())
            conn = sqlite3.connect('assignment.db')
            c = conn.cursor()
            c.execute("DELETE FROM Employees WHERE EmployeeID=?", (employee_id,))
            conn.commit()
            conn.close()
            self.load_data()

class MachineTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Add your machine tab layout here
        
        self.setLayout(layout)
    
    # Implement functionality for machine tab

class AssignmentTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Add your assignment tab layout here
        
        self.setLayout(layout)
    
    # Implement functionality for assignment tab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Machine Assignment")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.employee_tab = EmployeeTab()
        self.machine_tab = MachineTab()
        self.assignment_tab = AssignmentTab()
        
        self.tabs.addTab(self.employee_tab, "Employees")
        self.tabs.addTab(self.machine_tab, "Machines")
        self.tabs.addTab(self.assignment_tab, "Assignments")

def initialize_db():
    conn = sqlite3.connect('assignment.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        JobTitle TEXT NOT NULL,
        IsAssigned BOOLEAN DEFAULT FALSE
    )
    ''')

    # Add other table creation queries if needed

    conn.commit()
    conn.close()

def main():
    initialize_db()  # Initialize the database before running the application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
