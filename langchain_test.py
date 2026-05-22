from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from sqlalchemy import create_engine, text
import os

llm = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

db = SQLDatabase.from_uri("sqlite:///FirstDB.db")

chain = create_sql_query_chain(llm, db)

question = "show employees with salary above 50000"

response = chain.invoke({
    "question": question
})

generated_sql = response.split("SQLQuery:")[-1].strip()

print("Generated SQL:")
print(generated_sql)

engine = create_engine("sqlite:///FirstDB.db")

connection = engine.connect()

query = text(generated_sql)

result = connection.execute(query)

print("\nResults:")

for row in result:
    print(row)