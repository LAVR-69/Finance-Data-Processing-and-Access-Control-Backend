import psycopg2

conn = psycopg2.connect(
    dbname="finance_db",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

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