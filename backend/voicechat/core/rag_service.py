import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"

def query_rag(user_question):

    response = client.responses.create(
        model="gpt-5.2",
        input=[
            {
                "role": "system",
                "content": "Answer ONLY using retrieved content from file_search. If not found, say you don't have that info."
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        tools=[{
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID]
        }]
    )

    return response.output_text
