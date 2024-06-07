import sqlite3

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

initialize_db()
