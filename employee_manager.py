import mysql.connector
import json

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            with open('dbconfig.json', 'r') as f:
                config = json.load(f)
            
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

class EmployeeManager:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_employee(self):
        if not self.db.connect():
            return
        
        name = input("Enter name: ")
        email = input("Enter email: ")
        department = input("Enter department: ")
        age = int(input("Enter age: "))
        designation = input("Enter designation: ")
        
        query = "INSERT INTO employees (name, email, department, age, designation) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.db.cursor.execute(query, (name, email, department, age, designation))
            self.db.connection.commit()
            print("Employee created successfully!")
        except Exception as e:
            print(f"Error creating employee: {e}")
        finally:
            self.db.close()
    
    def list_employees(self):
        if not self.db.connect():
            return
        
        query = "SELECT * FROM employees"
        try:
            self.db.cursor.execute(query)
            employees = self.db.cursor.fetchall()
            
            print("\n--- All Employees ---")
            for emp in employees:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Email: {emp[2]}, Department: {emp[3]}, Age: {emp[4]}, Designation: {emp[5]}")
        except Exception as e:
            print(f"Error fetching employees: {e}")
        finally:
            self.db.close()
    
    def update_employee(self):
        if not self.db.connect():
            return
        
        emp_id = int(input("Enter employee ID to update: "))
        
        # Fetch current details
        query = "SELECT * FROM employees WHERE id = %s"
        try:
            self.db.cursor.execute(query, (emp_id,))
            employee = self.db.cursor.fetchone()
            
            if not employee:
                print("Employee not found!")
                return
            
            print(f"\nCurrent details:")
            print(f"Name: {employee[1]}, Email: {employee[2]}, Department: {employee[3]}, Age: {employee[4]}, Designation: {employee[5]}")
            
            confirm = input("\nDo you want to update this employee? (y/n): ")
            if confirm.lower() != 'y':
                return
            
            name = input(f"Enter new name ({employee[1]}): ") or employee[1]
            email = input(f"Enter new email ({employee[2]}): ") or employee[2]
            department = input(f"Enter new department ({employee[3]}): ") or employee[3]
            age = input(f"Enter new age ({employee[4]}): ")
            age = int(age) if age else employee[4]
            designation = input(f"Enter new designation ({employee[5]}): ") or employee[5]
            
            update_query = "UPDATE employees SET name=%s, email=%s, department=%s, age=%s, designation=%s WHERE id=%s"
            self.db.cursor.execute(update_query, (name, email, department, age, designation, emp_id))
            self.db.connection.commit()
            print("Employee updated successfully!")
            
        except Exception as e:
            print(f"Error updating employee: {e}")
        finally:
            self.db.close()
    
    def delete_employee(self):
        if not self.db.connect():
            return
        
        emp_id = int(input("Enter employee ID to delete: "))
        
        query = "DELETE FROM employees WHERE id = %s"
        try:
            self.db.cursor.execute(query, (emp_id,))
            if self.db.cursor.rowcount > 0:
                self.db.connection.commit()
                print("Employee deleted successfully!")
            else:
                print("Employee not found!")
        except Exception as e:
            print(f"Error deleting employee: {e}")
        finally:
            self.db.close()
    
    def run(self):
        while True:
            print("\n--- Employee Management System ---")
            print("1. Create new employee")
            print("2. List all employees")
            print("3. Update employee")
            print("4. Delete employee")
            print("5. Quit")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                self.create_employee()
            elif choice == '2':
                self.list_employees()
            elif choice == '3':
                self.update_employee()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    manager = EmployeeManager()
    manager.run()
