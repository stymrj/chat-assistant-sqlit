import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create Employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    )
''')

# Create Departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    )
''')

# Insert sample data
cursor.executemany('''
    INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date)
    VALUES (?, ?, ?, ?, ?)
''', [
    (1, "Alice", "Sales", 50000, "2021-01-15"),
    (2, "Bob", "Engineering", 70000, "2020-06-10"),
    (3, "Charlie", "Marketing", 60000, "2022-03-20")
])

cursor.executemany('''
    INSERT INTO Departments (ID, Name, Manager)
    VALUES (?, ?, ?)
''', [
    (1, "Sales", "Alice"),
    (2, "Engineering", "Bob"),
    (3, "Marketing", "Charlie")
])

# Commit and close
conn.commit()
conn.close()

print("Database setup completed!")
