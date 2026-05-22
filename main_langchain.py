from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy import create_engine, text

from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

from pydantic import BaseModel

from schema_helper import build_compact_schema

from auth import (
    verify_password,
    create_access_token,
    verify_token,
)

import time

load_dotenv()

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:4200"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

CURRENT_DB_URL = ""

CURRENT_DB_TYPE = ""

SCHEMA_CACHE = {}

llm = ChatOpenAI(

    base_url="http://127.0.0.1:1234/v1",

    api_key="lm-studio",

    model="qwen2.5-coder-3b-instruct",

    temperature=0

)


class MetadataInput(BaseModel):

    table_name: str

    column_name: str

    description: str


class DatabaseConnection(BaseModel):

    db_type: str

    host: str

    username: str

    password: str

    database: str


class LoginRequest(BaseModel):

    username: str

    password: str


@app.get("/")
def home():

    return {
        "message": "AI SQL Database System Running"
    }


def authenticate_user(authorization):

    if authorization is None:

        return None

    if not authorization.startswith("Bearer "):

        return None

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    return payload


def get_cached_schema(db_url):

    global SCHEMA_CACHE

    if db_url not in SCHEMA_CACHE:

        SCHEMA_CACHE[db_url] = build_compact_schema(
            db_url
        )

    return SCHEMA_CACHE[db_url]


def validate_sql(generated_sql):

    upper_sql = generated_sql.upper()

    allowed_starts = [
        "SELECT",
        "WITH"
    ]

    if not any(
        upper_sql.startswith(x)
        for x in allowed_starts
    ):

        return False, "Only SELECT queries are allowed"

    blocked_keywords = [

        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "EXEC",
        "EXECUTE",
        "MERGE",
        "CALL",
        "GRANT",
        "REVOKE"

    ]

    for keyword in blocked_keywords:

        if keyword in upper_sql:

            return False, f"{keyword} queries are not allowed"

    return True, ""


@app.post("/login")
def login(data: LoginRequest):

    global CURRENT_DB_URL

    if CURRENT_DB_URL == "":

        return {
            "error": "No database connected"
        }

    try:

        engine = create_engine(CURRENT_DB_URL)

        with engine.connect() as connection:

            query = text("""

                SELECT
                    username,
                    password_hash,
                    role_name
                FROM app_users
                WHERE username = :username

            """)

            result = connection.execute(

                query,

                {
                    "username": data.username
                }

            ).fetchone()

        if not result:

            return {
                "error": "Invalid username"
            }

        stored_hash = result[1]

        if not verify_password(
            data.password,
            stored_hash
        ):

            return {
                "error": "Invalid password"
            }

        token = create_access_token({

            "username": result[0],

            "role": result[2]

        })

        return {

            "access_token": token,

            "role": result[2]

        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/save-metadata")
def save_metadata(
    data: MetadataInput
):

    global CURRENT_DB_URL
    global SCHEMA_CACHE

    if CURRENT_DB_URL == "":

        return {
            "error": "No database connected"
        }

    try:

        engine = create_engine(CURRENT_DB_URL)

        with engine.begin() as connection:

            query = text("""

                INSERT INTO metadata_definitions
                (
                    table_name,
                    column_name,
                    description
                )
                VALUES
                (
                    :table_name,
                    :column_name,
                    :description
                )

            """)

            connection.execute(

                query,

                {

                    "table_name": data.table_name,

                    "column_name": data.column_name,

                    "description": data.description

                }

            )

        SCHEMA_CACHE.clear()

        return {

            "message": "Metadata saved successfully"

        }

    except Exception as e:

        return {

            "error": str(e)

        }

        connection.commit()

        SCHEMA_CACHE.clear()

        return {

            "message": "Metadata saved successfully"

        }

    except Exception as e:

        return {

            "error": str(e)

        }


@app.get("/metadata")
def get_metadata():

    global CURRENT_DB_URL

    if CURRENT_DB_URL == "":

        return {
            "error": "No database connected"
        }

    try:

        engine = create_engine(CURRENT_DB_URL)
        print(CURRENT_DB_URL)
        with engine.connect() as connection:

            query = text("""

                SELECT
                    table_name,
                    column_name,
                    description
                FROM metadata_definitions
                ORDER BY table_name

            """)

            result = connection.execute(query)

            metadata = []

            for row in result:

                metadata.append({

                    "table_name": row[0],

                    "column_name": row[1],

                    "description": row[2]

                })

        return {
            "metadata": metadata
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/connect-db")
def connect_db(data: DatabaseConnection):

    global CURRENT_DB_URL
    global CURRENT_DB_TYPE
    global SCHEMA_CACHE

    host = data.host
    username = data.username
    password = data.password
    database = data.database

    if data.db_type == "mysql":

        db_url = (
            f"mysql+pymysql://{username}:{password}"
            f"@{host}/{database}"
        )

    elif data.db_type == "mssql":

        db_url = (
            f"mssql+pyodbc://@{host}/{database}"
            "?driver=ODBC+Driver+18+for+SQL+Server"
            "&trusted_connection=yes"
            "&TrustServerCertificate=yes"
            "&Encrypt=no"
        )

    else:

        return {
            "error": "Unsupported database type"
        }

    try:

        engine = create_engine(db_url)

        with engine.connect():
            pass

        CURRENT_DB_URL = db_url

        CURRENT_DB_TYPE = data.db_type

        SCHEMA_CACHE.clear()

        return {

            "message": "Database connected successfully"

        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.get("/schemas")
def get_schema():

    global CURRENT_DB_URL

    if CURRENT_DB_URL == "":

        return {
            "error": "No database connected"
        }

    try:

        schema = get_cached_schema(
            CURRENT_DB_URL
        )

        return {
            "schema": schema
        }

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/tables")
def get_tables():
    global CURRENT_DB_URL

    if CURRENT_DB_URL == "":
        return []
    engine = create_engine(CURRENT_DB_URL)
    inspector = inspect(engine)
    return inspector.get_table_names()

@app.get("/columns/{table_name}")
def get_columns(table_name:str):

    global CURRENT_DB_URL

    if CURRENT_DB_URL == "":
        return []
    
    engine = create_engine(CURRENT_DB_URL)

    inspector = inpect(engine)

    columns = inspector.get_columns(table_name)

    return[
        column["name"]
        for column in columns
    ]



@app.get("/query")
def query(question: str):

    global CURRENT_DB_URL
    global CURRENT_DB_TYPE

    if CURRENT_DB_URL == "":

        return {
            "error": "No database connected"
        }

    try:

        start_time = time.time()

        engine = create_engine(CURRENT_DB_URL)

        compact_schema = get_cached_schema(
            CURRENT_DB_URL
        )

        base_prompt = f"""

        You are an expert SQL assistant.

        Database Schema:
        {compact_schema}

        Rules:
        - Return ONLY SQL
        - No markdown
        - No explanation
        - No comments
        - One query only
        - Use ONLY schema tables
        - Use ONLY schema columns
        - Never invent tables
        - Never invent columns

        """

        if CURRENT_DB_TYPE == "mysql":

            base_prompt += """

            - Use ONLY MySQL syntax
            - Use LIMIT instead of TOP
            - NEVER use TOP

            """

        elif CURRENT_DB_TYPE == "mssql":

            base_prompt += """

            - Use ONLY Microsoft SQL Server syntax
            - Use TOP instead of LIMIT
            - NEVER use LIMIT

            CORRECT:
            SELECT TOP 1 name
            FROM employees
            ORDER BY salary DESC

            WRONG:
            ORDER BY salary DESC TOP 1

            """

        prompt = base_prompt + f"""

        User Question:
        {question}

        """

        generated_sql = ""

        for attempt in range(2):

            response = llm.invoke(prompt)

            generated_sql = response.content.strip()

            generated_sql = generated_sql.replace(
                "```sql",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            generated_sql = generated_sql.split(";")[0].strip()

            generated_sql = generated_sql.replace(
                "\n",
                " "
            )

            upper_sql = generated_sql.upper()

            if CURRENT_DB_TYPE == "mssql":

                if "TOP 1" not in upper_sql and "ORDER BY" in upper_sql:

                    generated_sql = generated_sql.replace(
                        "SELECT",
                        "SELECT TOP 1",
                        1
                    )

                generated_sql = generated_sql.replace(
                    "LIMIT 1",
                    ""
                )

            if CURRENT_DB_TYPE == "mysql":

                generated_sql = generated_sql.replace(
                    "TOP 1",
                    ""
                )

                if "LIMIT" not in upper_sql:

                    generated_sql += " LIMIT 1"

            print("\nQUESTION:")
            print(question)

            print("\nGENERATED SQL:")
            print(generated_sql)

            is_valid, validation_message = validate_sql(
                generated_sql
            )

            if not is_valid:

                return {
                    "error": validation_message
                }

            try:

                with engine.connect() as connection:

                    sql_query = text(generated_sql)

                    result = connection.execute(
                        sql_query
                    )

                    columns = result.keys()

                    data = []

                    for row in result:

                        row_dict = {}

                        for index, column in enumerate(columns):

                            row_dict[column] = row[index]

                        data.append(row_dict)

                execution_time = round(
                    time.time() - start_time,
                    2
                )

                return {

                    "question": question,

                    "generated_sql": generated_sql,

                    "result": data,

                    "human_response": f"{len(data)} record(s) found.",

                    "execution_time_seconds": execution_time

                }

            except Exception as sql_error:

                print("\nSQL ERROR:")
                print(sql_error)

                prompt = base_prompt + f"""

                Previous SQL failed.

                SQL:
                {generated_sql}

                Error:
                {str(sql_error)}

                Fix the SQL.

                User Question:
                {question}

                """

        return {

            "error": "AI failed after retry",

            "generated_sql": generated_sql

        }

    except Exception as e:

        return {
            "error": str(e)
        }