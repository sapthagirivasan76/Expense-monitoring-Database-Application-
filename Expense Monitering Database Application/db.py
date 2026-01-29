import mysql.connector
try:
    
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="accord",   # change if needed
            database="expense_db"
        )

    def insert_expense(date, category, amount, description):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO expenses (date, category, amount, description) VALUES (%s,%s,%s,%s)",
            (date, category, amount, description)
        )
        con.commit()
        con.close()

    def fetch_expenses():
        con= get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM expenses")
        rows =cur.fetchall()
        con.close()
        return rows

    def delete_expense(expense_id):
        con =get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
        con.commit()
        con.close()

    def monthly_total(month, year):
        con = get_connection()
        cur= con.cursor()
        cur.execute("""
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE MONTH(date)=%s AND YEAR(date)=%s
        """, (month, year))
        total= cur.fetchone()[0]
        con.close()
        return total

except Exception as e:
    print("error to rectify", e)