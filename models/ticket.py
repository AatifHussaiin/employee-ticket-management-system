from database import get_connection
import random
import string


class Ticket:

    # ==========================================
    # GENERATE TICKET ID
    # ==========================================

    @staticmethod
    def generate_ticket_id():

        while True:

            code = "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )

            ticket_id = f"TKT-{code}"

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM tickets WHERE ticket_id=?",
                (ticket_id,)
            )

            result = cursor.fetchone()

            conn.close()

            if result is None:

                return ticket_id

    # ==========================================
    # CREATE TICKET
    # ==========================================

    @staticmethod
    def create_ticket(
        employee_id,
        category,
        subject,
        description,
        priority
    ):

        ticket_id = Ticket.generate_ticket_id()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tickets
            (
                ticket_id,
                employee_id,
                category,
                subject,
                description,
                priority,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, 'Open')
        """, (
            ticket_id,
            employee_id,
            category,
            subject,
            description,
            priority
        ))

        conn.commit()
        conn.close()

        return ticket_id

    # ==========================================
    # GET EMPLOYEE TICKETS
    # ==========================================

    @staticmethod
    def get_employee_tickets(employee_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.ticket_id,
                t.category,
                t.subject,
                t.priority,
                t.status,
                COALESCE(u.full_name, 'Unassigned'),
                t.created_at
            FROM tickets t
            LEFT JOIN users u
                ON t.assigned_to = u.employee_id
            WHERE t.employee_id=?
            ORDER BY t.created_at DESC
        """, (employee_id,))

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # GET SINGLE TICKET
    # ==========================================

    @staticmethod
    def get_ticket(ticket_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                ticket_id,
                employee_id,
                category,
                subject,
                description,
                priority,
                status,
                created_at,
                updated_at,
                assigned_to
            FROM tickets
            WHERE ticket_id=?
        """, (ticket_id,))

        ticket = cursor.fetchone()

        conn.close()

        return ticket

    # ==========================================
    # GET EMPLOYEE COUNTS
    # ==========================================

    @staticmethod
    def get_employee_counts(employee_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE employee_id=?
        """, (employee_id,))

        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE employee_id=?
            AND status='Open'
        """, (employee_id,))

        open_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE employee_id=?
            AND status='Pending'
        """, (employee_id,))

        pending = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE employee_id=?
            AND status='Resolved'
        """, (employee_id,))

        resolved = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE employee_id=?
            AND priority='High'
        """, (employee_id,))

        high_priority = cursor.fetchone()[0]

        conn.close()

        return {
            "total": total,
            "open": open_count,
            "pending": pending,
            "resolved": resolved,
            "high_priority": high_priority
        }

    # ==========================================
    # GET RECENT EMPLOYEE TICKETS
    # ==========================================

    @staticmethod
    def get_recent_tickets(
        employee_id,
        limit=5
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ticket_id,
                subject,
                priority,
                status,
                created_at
            FROM tickets
            WHERE employee_id=?
            ORDER BY created_at DESC
            LIMIT ?
        """, (
            employee_id,
            limit
        ))

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # GET ALL TICKETS - ADMIN
    # ==========================================

    @staticmethod
    def get_all_tickets():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.ticket_id,
                t.employee_id,
                t.category,
                t.subject,
                t.priority,
                t.status,
                COALESCE(u.full_name, 'Unassigned'),
                t.created_at
            FROM tickets t
            LEFT JOIN users u
                ON t.assigned_to = u.employee_id
            ORDER BY t.created_at DESC
        """)

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # ADMIN COUNTS
    # ==========================================

    @staticmethod
    def get_admin_counts():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
        """)

        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status='Open'
        """)

        open_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status='Pending'
        """)

        pending = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status='Resolved'
        """)

        resolved = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE priority='High'
        """)

        high_priority = cursor.fetchone()[0]

        conn.close()

        return {
            "total": total,
            "open": open_count,
            "pending": pending,
            "resolved": resolved,
            "high_priority": high_priority
        }

    # ==========================================
    # SEARCH ALL TICKETS - ADMIN
    # ==========================================

    @staticmethod
    def search_all_tickets(
        search_text="",
        status="All",
        priority="All"
    ):

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                t.ticket_id,
                t.employee_id,
                t.category,
                t.subject,
                t.priority,
                t.status,
                COALESCE(u.full_name, 'Unassigned'),
                t.created_at
            FROM tickets t
            LEFT JOIN users u
                ON t.assigned_to = u.employee_id
            WHERE 1=1
        """

        params = []

        # ======================================
        # SEARCH
        # ======================================

        if search_text:

            query += """
                AND (
                    t.ticket_id LIKE ?
                    OR t.employee_id LIKE ?
                    OR t.category LIKE ?
                    OR t.subject LIKE ?
                    OR t.priority LIKE ?
                    OR t.status LIKE ?
                    OR COALESCE(u.full_name, '') LIKE ?
                )
            """

            search_pattern = f"%{search_text}%"

            params.extend([
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern
            ])

        # ======================================
        # STATUS FILTER
        # ======================================

        if status and status != "All":

            query += """
                AND t.status=?
            """

            params.append(status)

        # ======================================
        # PRIORITY FILTER
        # ======================================

        if priority and priority != "All":

            query += """
                AND t.priority=?
            """

            params.append(priority)

        query += """
            ORDER BY t.created_at DESC
        """

        cursor.execute(
            query,
            params
        )

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # UPDATE STATUS
    # ==========================================

    @staticmethod
    def update_status(
        ticket_id,
        new_status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets
            SET
                status=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE ticket_id=?
        """, (
            new_status,
            ticket_id
        ))

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated

    # ==========================================
    # GET ASSIGNABLE EMPLOYEES
    # ==========================================

    @staticmethod
    def get_assignable_employees():

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
    # ASSIGN TICKET
    # ==========================================

    @staticmethod
    def assign_ticket(
        ticket_id,
        employee_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets
            SET
                assigned_to=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE ticket_id=?
        """, (
            employee_id,
            ticket_id
        ))

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated

    # ==========================================
    # GET ASSIGNED EMPLOYEE
    # ==========================================

    @staticmethod
    def get_assigned_employee(
        ticket_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.assigned_to,
                u.full_name
            FROM tickets t
            LEFT JOIN users u
                ON t.assigned_to = u.employee_id
            WHERE t.ticket_id=?
        """, (ticket_id,))

        result = cursor.fetchone()

        conn.close()

        if result is None:

            return None

        return {
            "employee_id": result[0],
            "full_name": result[1]
        }

    # ==========================================
    # GET TICKETS BY STATUS
    # ==========================================

    @staticmethod
    def get_tickets_by_status(
        employee_id,
        status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ticket_id,
                category,
                subject,
                priority,
                status,
                created_at
            FROM tickets
            WHERE employee_id=?
            AND status=?
            ORDER BY created_at DESC
        """, (
            employee_id,
            status
        ))

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # GET TICKETS BY PRIORITY
    # ==========================================

    @staticmethod
    def get_tickets_by_priority(
        employee_id,
        priority
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ticket_id,
                category,
                subject,
                priority,
                status,
                created_at
            FROM tickets
            WHERE employee_id=?
            AND priority=?
            ORDER BY created_at DESC
        """, (
            employee_id,
            priority
        ))

        tickets = cursor.fetchall()

        conn.close()

        return tickets

    # ==========================================
    # REPORT - STATUS COUNTS
    # ==========================================

    @staticmethod
    def get_status_counts(
        employee_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM tickets
            WHERE employee_id=?
            GROUP BY status
        """, (employee_id,))

        rows = cursor.fetchall()

        conn.close()

        result = {
            "Open": 0,
            "Pending": 0,
            "Resolved": 0
        }

        for status, count in rows:

            if status in result:

                result[status] = count

        return result

    # ==========================================
    # REPORT - PRIORITY COUNTS
    # ==========================================

    @staticmethod
    def get_priority_counts(
        employee_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                priority,
                COUNT(*)
            FROM tickets
            WHERE employee_id=?
            GROUP BY priority
        """, (employee_id,))

        rows = cursor.fetchall()

        conn.close()

        result = {
            "Low": 0,
            "Medium": 0,
            "High": 0
        }

        for priority, count in rows:

            if priority in result:

                result[priority] = count

        return result

    # ==========================================
    # REPORT - CATEGORY COUNTS
    # ==========================================

    @staticmethod
    def get_category_counts(
        employee_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                category,
                COUNT(*)
            FROM tickets
            WHERE employee_id=?
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """, (employee_id,))

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ==========================================
    # REPORT - MONTHLY TREND
    # ==========================================

    @staticmethod
    def get_monthly_ticket_trend(
        employee_id
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                strftime('%Y-%m', created_at) AS month,
                COUNT(*)
            FROM tickets
            WHERE employee_id=?
            GROUP BY strftime('%Y-%m', created_at)
            ORDER BY month
        """, (employee_id,))

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ==========================================
    # REPORT - ADMIN STATUS COUNTS
    # ==========================================

    @staticmethod
    def get_admin_status_counts():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM tickets
            GROUP BY status
        """)

        rows = cursor.fetchall()

        conn.close()

        result = {
            "Open": 0,
            "Pending": 0,
            "Resolved": 0
        }

        for status, count in rows:

            if status in result:

                result[status] = count

        return result

    # ==========================================
    # REPORT - ADMIN PRIORITY COUNTS
    # ==========================================

    @staticmethod
    def get_admin_priority_counts():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                priority,
                COUNT(*)
            FROM tickets
            GROUP BY priority
        """)

        rows = cursor.fetchall()

        conn.close()

        result = {
            "Low": 0,
            "Medium": 0,
            "High": 0
        }

        for priority, count in rows:

            if priority in result:

                result[priority] = count

        return result

    # ==========================================
    # REPORT - ADMIN CATEGORY COUNTS
    # ==========================================

    @staticmethod
    def get_admin_category_counts():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                category,
                COUNT(*)
            FROM tickets
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ==========================================
    # REPORT - ADMIN MONTHLY TREND
    # ==========================================

    @staticmethod
    def get_admin_monthly_ticket_trend():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                strftime('%Y-%m', created_at) AS month,
                COUNT(*)
            FROM tickets
            GROUP BY strftime('%Y-%m', created_at)
            ORDER BY month
        """)

        rows = cursor.fetchall()

        conn.close()

        return rows