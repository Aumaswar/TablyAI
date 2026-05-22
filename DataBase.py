from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///FirstDB.db"

engine = create_engine(DATABASE_URL)

connection = engine.connect()

connection.execute(text("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary INTEGER,
    age INTEGER
)
"""))
connection.execute(text("DELETE FROM employees"))
connection.execute(text("""
INSERT INTO employees (name, salary, age)
VALUES
('Aum', 70000, 20),
('Raj', 30000, 21),
('Priya', 50000, 22)
"""))

user_query = "SELECT * FROM employees WHERE salary > 50000"

query = text(user_query)

result = connection.execute(query)

for row in result:
    print(row)

connection.commit()
