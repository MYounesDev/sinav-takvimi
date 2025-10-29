# Coordinator Accounts

This document lists all coordinator accounts available in the system.

## Default Credentials

All coordinator accounts use the same default password: **admin123**

It is recommended to change passwords after first login.

## Department Coordinators

### 1. Bilgisayar Mühendisliği (Computer Engineering)
- **Email:** bilgisayar@gmail.com
- **Password:** admin123
- **Role:** Coordinator

### 2. Yazılım Mühendisliği (Software Engineering)
- **Email:** yazilim@gmail.com
- **Password:** admin123
- **Role:** Coordinator

### 3. Elektrik Mühendisliği (Electrical Engineering)
- **Email:** elektrik@gmail.com
- **Password:** admin123
- **Role:** Coordinator

### 4. Elektronik Mühendisliği (Electronics Engineering)
- **Email:** elektronik@gmail.com
- **Password:** admin123
- **Role:** Coordinator

### 5. İnşaat Mühendisliği (Civil Engineering)
- **Email:** insaat@gmail.com
- **Password:** admin123
- **Role:** Coordinator

## Admin Account

- **Email:** admin@gmail.com
- **Password:** admin123
- **Role:** Administrator

## Adding/Updating Coordinators

If you need to add or update coordinator accounts, run:

```bash
python add_coordinators.py
```

This script will:
- Check existing departments
- Create missing departments if needed
- Add new coordinator accounts
- Update existing coordinator accounts
- Display all coordinator credentials

## Features by Role

### Administrator (Admin)
- Full access to all departments
- Can manage all courses, students, and exams
- Can view and manage all classrooms
- Access to all reports and exports

### Coordinator
- Access limited to their specific department
- Can manage courses for their department
- Can manage students enrolled in their department
- Can schedule exams for their department courses
- Can generate seating plans and export PDFs
- Can view and manage classrooms

## Login Instructions

1. Launch the application
2. Enter the coordinator email (e.g., bilgisayar@gmail.com)
3. Enter the password: admin123
4. Click Login

## Security Recommendations

1. Change default passwords after first login
2. Use strong passwords (minimum 8 characters with mix of letters, numbers, and symbols)
3. Do not share credentials between users
4. Regularly review user accounts and remove unused ones

## Troubleshooting

### Cannot Login
- Verify the email is correct (check for typos)
- Ensure password is exactly: admin123 (case-sensitive)
- Check that the database is properly initialized

### Coordinator Not Found
- Run `python add_coordinators.py` to add missing coordinators
- Check the database file exists at `database/exam_scheduler.db`

### Department Not Showing
- Verify the department exists in the database
- Run `python add_coordinators.py` to create missing departments

## Technical Details

Coordinator accounts are stored in the `users` table with:
- `role = 'coordinator'`
- `department_id` linking to their respective department
- Passwords are hashed using bcrypt for security

Each coordinator has full access to their department's data but cannot access other departments' information.

