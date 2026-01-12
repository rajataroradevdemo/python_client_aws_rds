CREATE DATABASE IF NOT EXISTS employee_db;
USE employee_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    designation VARCHAR(100) NOT NULL
);

-- Sample data
INSERT INTO employees (name, email, department, age, designation) VALUES
('John Doe', 'john.doe@company.com', 'Engineering', 30, 'Software Engineer'),
('Jane Smith', 'jane.smith@company.com', 'HR', 28, 'HR Manager'),
('Mike Johnson', 'mike.johnson@company.com', 'Sales', 35, 'Sales Director');
