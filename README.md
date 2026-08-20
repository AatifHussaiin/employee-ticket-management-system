# Employee Ticket Management System

A role-based employee ticket management system developed using Python and MySQL. The application allows employees to raise and track support tickets while administrators can manage users, monitor tickets, update ticket status, and generate reports.

## Features

- User registration and login
- Role-based access for employees and administrators
- Raise new support tickets
- View and track submitted tickets
- Update ticket status
- Admin dashboard
- User management
- Ticket management
- Profile management
- Ticket reports
- MySQL database integration
- Authentication and authorization

## Technology Stack

### Programming Language
- Python

### GUI / Application
- Tkinter

### Database
- MySQL

### Development Tools
- Git
- GitHub
- Visual Studio Code

### Concepts
- Object-Oriented Programming
- Database Management Systems
- Authentication and Authorization
- CRUD Operations
- Role-Based Access Control

## Project Structure

```text
EmployeeTicketManagementSystem/
│
├── assets/
│   └── Application assets
│
├── database/
│   └── Database-related files
│
├── gui/
│   ├── admin.py
│   ├── admin_users.py
│   ├── dashboard.py
│   ├── home.py
│   ├── login.py
│   ├── my_tickets.py
│   ├── profile.py
│   ├── raise_ticket.py
│   ├── register.py
│   ├── reports.py
│   └── sidebar.py
│
├── models/
│   ├── ticket.py
│   └── user.py
│
├── utils/
│   ├── auth.py
│   └── theme.py
│
├── create_admin.py
├── database.py
├── main.py
└── .gitignore