import time
import json
import os

import sys
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain import LLMChain, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

os.environ['OPENAI_API_KEY'] = "[insert your key here]"


def count_tokens(agent, query):
    with get_openai_callback() as cb:
        result = agent(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result



def ask_question(question_input):

    t0 = time.time()

    llm = OpenAI(
        temperature=0
    )


    question_template = """
You are a smart analyst who does analytics based on data and logic.

{question}

"""

    prompt = PromptTemplate.from_template(question_template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    result = llm_chain.run(question_input)


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

    




