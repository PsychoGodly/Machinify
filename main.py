import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem

class EmployeeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Job Title", "Pointed", "Assigned"])
        
        layout.addWidget(self.table)
        
        self.add_button = QPushButton("Add Employee")
        self.modify_button = QPushButton("Modify Employee")
        self.delete_button = QPushButton("Delete Employee")
        self.assign_button = QPushButton("Assign to Machine")
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.assign_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class MachineTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Max Employees"])
        
        layout.addWidget(self.table)
        
        self.add_button = QPushButton("Add Machine")
        self.modify_button = QPushButton("Modify Machine")
        self.delete_button = QPushButton("Delete Machine")
        self.assign_button = QPushButton("Assign Employee")
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.assign_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class AssignmentTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Machine ID", "Name", "Max Employees"])
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)

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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
