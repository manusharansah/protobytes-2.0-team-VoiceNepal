import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found")

client = OpenAI(api_key=api_key)

# -------------------------------------------------
# 1️⃣ Create Vector Store
# -------------------------------------------------
print("Creating vector store...")
vs = client.vector_stores.create(name="passport-kb")

print("Vector Store Created!")
print("Vector Store ID:", vs.id)

# -------------------------------------------------
# 2️⃣ Upload File
# -------------------------------------------------
print("Uploading file...")

file = client.files.create(
    file=open("passport records.docx", "rb"),
    purpose="assistants",
)

# -------------------------------------------------
# 3️⃣ Add File to Vector Store
# -------------------------------------------------
print("Adding file to vector store...")

batch = client.vector_stores.file_batches.create(
    vector_store_id=vs.id,
    file_ids=[file.id],
)

# -------------------------------------------------
# 4️⃣ Wait for Processing
# -------------------------------------------------
print("Waiting for ingestion to complete...")

while True:
    status = client.vector_stores.file_batches.retrieve(
        vector_store_id=vs.id,
        batch_id=batch.id,
    )

    if status.status in ("completed", "failed", "cancelled"):
        print("Batch status:", status.status)
        break

    time.sleep(1)

if status.status != "completed":
    raise RuntimeError("Ingestion failed")

print("\n✅ VECTOR STORE READY!")
print("Copy this ID and paste into rag_service.py:")
print("👉", vs.id)
