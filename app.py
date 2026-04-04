import psycopg2
from flask import Flask, request, jsonify
from ariadne import QueryType, MutationType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphiQL

# DB CONNECTION 
conn = psycopg2.connect(
    dbname="finance_db",
    user="admin",
    password="****",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ROLE FUNCTION 
def check_role(user, allowed_roles):
    cursor.execute("SELECT role FROM users WHERE name=%s AND active=TRUE", (user,))
    result = cursor.fetchone()

    if not result:
        raise Exception("User not found or inactive")

    role = result[0]

    if role not in allowed_roles:
        raise Exception("Access denied")

    return role

# CREATE TABLES 
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    role TEXT,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    amount INT,
    type TEXT,
    category TEXT,
    date TEXT,
    note TEXT
);
""")
conn.commit()

# INSERT USERS 
cursor.execute("INSERT INTO users (name, role) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", ("Aviral", "admin"))
cursor.execute("INSERT INTO users (name, role) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", ("Yash", "viewer"))
cursor.execute("INSERT INTO users (name, role) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", ("Yana", "analyst"))
conn.commit()

# APP 
app = Flask(__name__)

# SCHEMA 
type_defs = """
    type User {
        id: Int
        name: String
        role: String
    }

    type Record {
        id: Int
        amount: Int
        type: String
        category: String
        date: String
        note: String
    }

    type Summary {
        totalIncome: Int
        totalExpense: Int
        balance: Int
    }

    type CategorySummary {
        category: String
        total: Int
    }

    type Query {
        users: [User]
        records(type: String, category: String, date: String): [Record]
        summary: Summary
        summaryByCategory: [CategorySummary]
        recentRecords(limit: Int): [Record]
    }

    type Mutation {
        addRecord(
            amount: Int,
            type: String,
            category: String,
            date: String,
            note: String,
            user: String
        ): Record
        
        updateRecord(
            id: Int,
            amount: Int,
            category: String,
            note: String,
            user: String
        ): Record

        deleteRecord(id: Int, user: String): Boolean
    }
"""

# RESOLVERS 
query = QueryType()
mutation = MutationType()

@query.field("users")
def resolve_users(*_):
    cursor.execute("SELECT id, name, role FROM users WHERE active = TRUE")
    rows = cursor.fetchall()
    return [{"id": r[0], "name": r[1], "role": r[2]} for r in rows]

@query.field("records")
def resolve_records(_, info, type=None, category=None, date=None):
    query_sql = "SELECT * FROM records WHERE 1=1"
    params = []

    if type:
        query_sql += " AND type=%s"
        params.append(type)

    if category:
        query_sql += " AND category=%s"
        params.append(category)

    if date:
        query_sql += " AND date=%s"
        params.append(date)

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

@query.field("summaryByCategory")
def resolve_summary_by_category(*_):
    cursor.execute("SELECT category, SUM(amount) FROM records GROUP BY category")
    rows = cursor.fetchall()

    return [{"category": r[0], "total": r[1]} for r in rows]

# 🔥 FIXED RECENT RECORDS (IMPORTANT)
@query.field("recentRecords")
def resolve_recent_records(_, info, limit=5):

    if not limit:
        limit = 5

    query_sql = f"SELECT * FROM records ORDER BY id DESC LIMIT {limit}"
    cursor.execute(query_sql)
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

# MUTATIONS 
@mutation.field("addRecord")
def resolve_add_record(_, info, amount, type, category, date, note, user):

    if amount <= 0:
        raise Exception("Amount must be greater than 0")

    if type not in ["income", "expense"]:
        raise Exception("Invalid type")

    check_role(user, ["admin"])

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

@mutation.field("updateRecord")
def resolve_update_record(_, info, id, amount=None, category=None, note=None, user=None):

    check_role(user, ["admin"])

    query_sql = "UPDATE records SET "
    updates = []
    params = []

    if amount:
        updates.append("amount=%s")
        params.append(amount)

    if category:
        updates.append("category=%s")
        params.append(category)

    if note:
        updates.append("note=%s")
        params.append(note)

    if not updates:
        raise Exception("No fields to update")

    query_sql += ", ".join(updates)
    query_sql += " WHERE id=%s RETURNING id, amount, type, category, date, note"

    params.append(id)

    cursor.execute(query_sql, tuple(params))
    row = cursor.fetchone()
    conn.commit()

    if not row:
        raise Exception("Record not found")

    return {
        "id": row[0],
        "amount": row[1],
        "type": row[2],
        "category": row[3],
        "date": row[4],
        "note": row[5],
    }

@mutation.field("deleteRecord")
def resolve_delete_record(_, info, id, user):

    check_role(user, ["admin"])

    cursor.execute("DELETE FROM records WHERE id=%s RETURNING id", (id,))
    result = cursor.fetchone()
    conn.commit()

    if not result:
        raise Exception("Record not found")

    return True

# SCHEMA INIT 
schema = make_executable_schema(type_defs, query, mutation)

# ROUTE 
@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    if request.method == "GET":
        return ExplorerGraphiQL().html(None), 200

    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    return jsonify(result), 200

# RUN 
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        ssl_context=("cert.pem", "key.pem")
    )