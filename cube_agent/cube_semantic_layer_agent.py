import time
import json
import os
import sys

from sqlalchemy import create_engine
from langchain import LLMChain, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import (AgentExecutor, Tool, ZeroShotAgent,
                              initialize_agent, load_tools)

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

from sqlalchemy import URL
from sqlalchemy import create_engine

# Pull this key from your openAI account
os.environ['OPENAI_API_KEY'] = "[your openAI key here]"

### Pull this info from your Cube Console ###
cube_db_name="[your cube db name from console]"
cube_pw="[your cube pw from console]" 
host_cube="[your cube host from console]"
### Pull this info from your Cube Console ###


port= '5432'

cube_uri_object = URL.create(
    "postgresql", # postgresql+pg8000
    username="cube",
    password=cube_pw,  # plain (unescaped) text
    host=host_cube,
    database=cube_db_name
)

def ask_question(question_input):

    t0 = time.time()
    llm = OpenAI(temperature=0)

    engine = create_engine(cube_uri_object)

    db = SQLDatabase.from_uri(cube_uri_object)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    sql_cube_agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )

    test_query = sys.argv[ 1 ]
    result = sql_cube_agent.run( question_input )

    print("---------------------------------------------")
    print("Question: " + question_input)
    print("Answer: " + result)
    print("---------------------------------------------")

    t1 = time.time()
    total = t1-t0

    print("Seconds: " + str(total))
    print("Finished")
    return result



if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Need 1 arguments!")

    else:

        test_query = sys.argv[1]

        ask_question(test_query)

        print("completed...")

    




