# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"

# def query_rag(user_question):

#     response = client.responses.create(
#         model="gpt-5.2",
#         input=[
#             {
#                 "role": "system",
#                 "content": "Answer ONLY using retrieved content from file_search. If not found, say you don't have that info."
#             },
#             {
#                 "role": "user",
#                 "content": user_question
#             }
#         ],
#         tools=[{
#             "type": "file_search",
#             "vector_store_ids": [VECTOR_STORE_ID]
#         }]
#     )

#     return response.output_text


import os
import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# Initialize Gemini Model
# -----------------------------
llm = genai.GenerativeModel("gemini-1.5-pro")

# -----------------------------
# Load Embedding Model
# -----------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Sample Documents (Replace with your governance docs)
# -----------------------------
documents = [
    "Passport requires citizenship certificate and national ID.",
    "Driving license application requires medical certificate.",
    "Voter ID requires age above 18 and citizenship proof."
]

# -----------------------------
# Create FAISS Index
# -----------------------------
dimension = 384  # embedding size of MiniLM
index = faiss.IndexFlatL2(dimension)

doc_embeddings = embedder.encode(documents)
index.add(np.array(doc_embeddings))

# -----------------------------
# Retrieval Function
# -----------------------------
def retrieve(query, k=2):
    query_vector = embedder.encode([query])
    distances, indices = index.search(np.array(query_vector), k)

    retrieved_docs = [documents[i] for i in indices[0]]
    return "\n".join(retrieved_docs)

# -----------------------------
# RAG Query Function
# -----------------------------
def query_rag(user_question):

    # Step 1: Retrieve relevant documents
    context = retrieve(user_question)

    # Step 2: Strict prompt (NO hallucination allowed)
    prompt = f"""
You are an official government information assistant.

Answer ONLY using the context below.
If the answer is not clearly present in the context,
reply exactly: "I don't have that information."

Context:
{context}

Question:
{user_question}

Answer:
"""

    response = llm.generate_content(prompt)

    return response.text


