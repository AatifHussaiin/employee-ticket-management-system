from database import get_connection
from utils.auth import verify_password, hash_password


class User:

    # ==========================================
    # CHECK EMPLOYEE ID
    # ==========================================

    @staticmethod
    def employee_exists(employee_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT employee_id FROM users WHERE employee_id=?",
            (employee_id,)
        )

        result = cursor.fetchone()

        conn.close()

        return result is not None

    # ==========================================
    # CHECK EMAIL
    # ==========================================

    @staticmethod
    def email_exists(email):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT email FROM users WHERE email=?",
            (email,)
        )

        result = cursor.fetchone()

        conn.close()

        return result is not None

    # ==========================================
    # REGISTER USER
    # ==========================================

    @staticmethod
    def register(user_data):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (
                employee_id,
                full_name,
                email,
                department,
                password
            )
            VALUES (?, ?, ?, ?, ?)
        """, user_data)

        conn.commit()
        conn.close()

    # ==========================================
    # LOGIN
    # ==========================================

    @staticmethod
    def login(employee_id, password):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                employee_id,
                full_name,
                email,
                department,
                password,
                role
            FROM users
            WHERE employee_id=?
        """, (employee_id,))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return None

        if verify_password(password, user[4]):

            return {
                "employee_id": user[0],
                "full_name": user[1],
                "email": user[2],
                "department": user[3],
                "role": user[5]
            }

        return None

    # ==========================================
    # UPDATE PROFILE
    # ==========================================

    @staticmethod
    def update_profile(
        employee_id,
        full_name,
        email,
        department
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET
                full_name=?,
                email=?,
                department=?
            WHERE employee_id=?
        """, (
            full_name,
            email,
            department,
            employee_id
        ))

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated

    # ==========================================
    # GET USER
    # ==========================================

    @staticmethod
    def get_user(employee_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                employee_id,
                full_name,
                email,
                department,
                role
            FROM users
            WHERE employee_id=?
        """, (employee_id,))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return None

        return {
            "employee_id": user[0],
            "full_name": user[1],
            "email": user[2],
            "department": user[3],
            "role": user[4]
        }

    # ==========================================
    # GET ALL EMPLOYEES
    # ==========================================

    @staticmethod
    def get_all_employees():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                employee_id,
                full_name
            FROM users
            WHERE role='Employee'
            ORDER BY full_name
        """)

        employees = cursor.fetchall()

        conn.close()

        return employees

    # ==========================================
    # VERIFY CURRENT PASSWORD
    # ==========================================

    @staticmethod
    def verify_current_password(
        employee_id,
        password
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT password
            FROM users
            WHERE employee_id=?
        """, (employee_id,))

        result = cursor.fetchone()

        conn.close()

        if result is None:
            return False

        return verify_password(
            password,
            result[0]
        )

    # ==========================================
    # CHANGE PASSWORD
    # ==========================================

    @staticmethod
    def change_password(
        employee_id,
        new_password
    ):

        hashed_password = hash_password(
            new_password
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password=?
            WHERE employee_id=?
        """, (
            hashed_password,
            employee_id
        ))

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated