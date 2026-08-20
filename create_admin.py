from database import get_connection
from utils.auth import hash_password


def create_admin():

    employee_id = input("Enter Admin Employee ID: ").strip()
    full_name = input("Enter Admin Name: ").strip()
    email = input("Enter Admin Email: ").strip()
    department = input("Enter Department: ").strip()
    password = input("Enter Admin Password: ").strip()

    if not employee_id or not full_name or not email or not department or not password:
        print("\nAll fields are required.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check if employee ID already exists
    cursor.execute(
        "SELECT employee_id FROM users WHERE employee_id=?",
        (employee_id,)
    )

    if cursor.fetchone():

        print("\nEmployee ID already exists.")
        conn.close()
        return

    # Check if email already exists
    cursor.execute(
        "SELECT email FROM users WHERE email=?",
        (email,)
    )

    if cursor.fetchone():

        print("\nEmail already exists.")
        conn.close()
        return

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users
        (
            employee_id,
            full_name,
            email,
            department,
            password,
            role
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        employee_id,
        full_name,
        email,
        department,
        password_hash,
        "Admin"
    ))

    conn.commit()
    conn.close()

    print("\n================================")
    print("Admin account created successfully!")
    print("================================")
    print(f"Employee ID : {employee_id}")
    print(f"Name        : {full_name}")
    print(f"Department  : {department}")
    print("Role        : Admin")


if __name__ == "__main__":
    create_admin()