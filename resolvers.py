from ariadne import QueryType, MutationType
from db import cursor, conn

query = QueryType()
mutation = MutationType()

# USERS 
@query.field("users")
def resolve_users(*_):
    cursor.execute("SELECT id, name, role FROM users WHERE active = TRUE")
    rows = cursor.fetchall()
    return [{"id": r[0], "name": r[1], "role": r[2]} for r in rows]

#  RECORDS (WITH FILTERING) 
@query.field("records")
def resolve_records(_, info, type=None, category=None):
    query_sql = "SELECT * FROM records WHERE 1=1"
    params = []

    if type:
        query_sql += " AND type=%s"
        params.append(type)

    if category:
        query_sql += " AND category=%s"
        params.append(category)

    cursor.execute(query_sql, tuple(params))
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "amount": r[1],
            "type": r[2],
            "category": r[3],
            "date": r[4],
            "note": r[5],
        }
        for r in rows
    ]

# SUMMARY 
@query.field("summary")
def resolve_summary(*_):
    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM records WHERE type='income'")
    income = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM records WHERE type='expense'")
    expense = cursor.fetchone()[0]

    return {
        "totalIncome": income,
        "totalExpense": expense,
        "balance": income - expense
    }

#  CATEGORY SUMMARY 
@query.field("summaryByCategory")
def resolve_summary_by_category(*_):
    cursor.execute("SELECT category, SUM(amount) FROM records GROUP BY category")
    rows = cursor.fetchall()   # ✅ FIXED TYPO

    return [
        {
            "category": r[0],
            "total": r[1]
        }
        for r in rows
    ]

# RECENT RECORDS 
@query.field("recentRecords")
def resolve_recent_records(_, info, limit=5):

    cursor.execute(
        "SELECT * FROM records ORDER BY id DESC LIMIT %s",
        (limit,)
    )

    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "amount": r[1],
            "type": r[2],
            "category": r[3],
            "date": r[4],
            "note": r[5],
        }
        for r in rows
    ]

#  ADD RECORD 
@mutation.field("addRecord")
def resolve_add_record(_, info, amount, type, category, date, note, user):

    if amount <= 0:
        raise Exception("Amount must be greater than 0")

    if type not in ["income", "expense"]:
        raise Exception("Invalid type")

    cursor.execute("SELECT role FROM users WHERE name=%s AND active=TRUE", (user,))
    result = cursor.fetchone()

    if not result:
        raise Exception("User not found or inactive")

    if result[0] != "admin":
        raise Exception("Only admin can add records")

    cursor.execute(
        "INSERT INTO records (amount, type, category, date, note) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (amount, type, category, date, note)
    )

    new_id = cursor.fetchone()[0]
    conn.commit()

    return {
        "id": new_id,
        "amount": amount,
        "type": type,
        "category": category,
        "date": date,
        "note": note,
    }