from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:2810@localhost/company_db"
)

connection = engine.connect()

print("MySQL Connected")