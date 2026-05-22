from sqlalchemy import create_engine, text
from auth import hash_password

DB_URL = (
    "mssql+pyodbc://@localhost/company_db"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
    "&Encrypt=no"
)

engine = create_engine(DB_URL)

connection = engine.connect()

print("CONNECTED SUCCESSFULLY")

username = "admin"

password = "admin123"

hashed_password = hash_password(password)

query = text("""

    INSERT INTO app_users
    (
        username,
        password_hash,
        role_name
    )

    VALUES
    (
        :username,
        :password_hash,
        :role_name
    )

""")

connection.execute(

    query,

    {
        "username": username,
        "password_hash": hashed_password,
        "role_name": "admin"
    }

)

connection.commit()

connection.close()

print("ADMIN USER CREATED")