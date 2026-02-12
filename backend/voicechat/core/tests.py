import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found")

client = OpenAI(api_key=api_key)

# 🔥 VERY IMPORTANT:
# Put your ALREADY CREATED vector_store_id here
VECTOR_STORE_ID = "PASTE_YOUR_VECTOR_STORE_ID_HERE"


def query_rag(user_question: str) -> str:
    """
    Sends user question to OpenAI RAG system
    and returns model output text.
    """

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
