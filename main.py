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

class EmployeeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Job Title", "Pointed", "Assigned"])
        
        layout.addWidget(self.table)
        
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.show_add_employee_dialog)
        
        self.modify_button = QPushButton("Modify Employee")
        self.modify_button.clicked.connect(self.modify_employee)
        
        self.delete_button = QPushButton("Delete Employee")
        self.delete_button.clicked.connect(self.delete_employee)
        
        self.assign_button = QPushButton("Assign to Machine")
        self.assign_button.clicked.connect(self.assign_employee)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.assign_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
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
                
    def show_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec_():
            self.load_data()
            
    def modify_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_id = int(self.table.item(selected_row, 0).text())
            # Open dialog to modify employee with given employee_id
    
    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_id = int(self.table.item(selected_row, 0).text())
            conn = sqlite3.connect('assignment.db')
            c = conn.cursor()
            c.execute("DELETE FROM Employees WHERE EmployeeID=?", (employee_id,))
            conn.commit()
            conn.close()
            self.load_data()
            
    def assign_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            pointed = self.table.item(selected_row, 4).text()
            if pointed == "Yes":
                # Open dialog to assign employee to machine
                window = MainWindow()
                window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Machine Assignment")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.employee_tab = EmployeeTab()
        self.machine_tab = QWidget()
        self.assignment_tab = QWidget()
        
        self.tabs.addTab(self.employee_tab, "Employees")
        self.tabs.addTab(self.machine_tab, "Machines")
        self.tabs.addTab(self.assignment_tab, "Assignments")
        
        self.employee_tab.load_data()

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

    # Create other tables (Machines, Assignments) similarly if needed

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
