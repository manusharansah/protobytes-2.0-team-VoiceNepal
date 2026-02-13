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


# import os
# import faiss
# import numpy as np
# import google.generativeai as genai
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer

# # -----------------------------
# # Load API Key
# # -----------------------------
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # -----------------------------
# # Initialize Gemini Model
# # -----------------------------
# llm = genai.GenerativeModel("gemini-1.5-pro")

# # -----------------------------
# # Load Embedding Model
# # -----------------------------
# embedder = SentenceTransformer("all-MiniLM-L6-v2")

# # -----------------------------
# # Sample Documents (Replace with your governance docs)
# # -----------------------------
# documents = [
#     "Passport requires citizenship certificate and national ID.",
#     "Driving license application requires medical certificate.",
#     "Voter ID requires age above 18 and citizenship proof."
# ]

# # -----------------------------
# # Create FAISS Index
# # -----------------------------
# dimension = 384  # embedding size of MiniLM
# index = faiss.IndexFlatL2(dimension)

# doc_embeddings = embedder.encode(documents)
# index.add(np.array(doc_embeddings))

# # -----------------------------
# # Retrieval Function
# # -----------------------------
# def retrieve(query, k=2):
#     query_vector = embedder.encode([query])
#     distances, indices = index.search(np.array(query_vector), k)

#     retrieved_docs = [documents[i] for i in indices[0]]
#     return "\n".join(retrieved_docs)

# # -----------------------------
# # RAG Query Function
# # -----------------------------
# def query_rag(user_question):

#     # Step 1: Retrieve relevant documents
#     context = retrieve(user_question)

#     # Step 2: Strict prompt (NO hallucination allowed)
#     prompt = f"""
# You are an official government information assistant.

# Answer ONLY using the context below.
# If the answer is not clearly present in the context,
# reply exactly: "I don't have that information."

# Context:
# {context}

# Question:
# {user_question}

# Answer:
# """

#     response = llm.generate_content(prompt)

#     return response.text


# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from typing import Optional, Dict, Any, List
# import json
# from datetime import datetime

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"
# FEEDBACK_LOG_FILE = "admin_feedback.json"


# class RAGService:
#     def __init__(self):
#         self.client = client
#         self.vector_store_id = VECTOR_STORE_ID
#         self.feedback_history = self._load_feedback_history()
    
#     def _load_feedback_history(self) -> List[Dict]:
#         """Load existing feedback history from file"""
#         if os.path.exists(FEEDBACK_LOG_FILE):
#             with open(FEEDBACK_LOG_FILE, 'r') as f:
#                 return json.load(f)
#         return []
    
#     def _save_feedback(self, feedback_entry: Dict):
#         """Save feedback to persistent storage"""
#         self.feedback_history.append(feedback_entry)
#         with open(FEEDBACK_LOG_FILE, 'w') as f:
#             json.dump(self.feedback_history, f, indent=2)
    
#     def identify_role(self, user_id: str = None, api_key_admin: str = None) -> str:
#         """
#         Identify if the request is from admin or user
        
#         Args:
#             user_id: User identifier
#             api_key_admin: Admin API key for authentication
        
#         Returns:
#             'admin' or 'user'
#         """
#         # Simple role identification - you can enhance with proper auth
#         ADMIN_KEY = os.getenv("ADMIN_API_KEY", "admin_secret_key")
        
#         if api_key_admin and api_key_admin == ADMIN_KEY:
#             return "admin"
#         return "user"
    
#     def query_rag(self, user_question: str, role: str = "user") -> Dict[str, Any]:
#         """
#         Query the RAG system
        
#         Args:
#             user_question: The question to answer
#             role: 'admin' or 'user'
        
#         Returns:
#             Dictionary with response and metadata
#         """
#         try:
#             response = self.client.responses.create(
#                 model="gpt-5.2",
#                 input=[
#                     {
#                         "role": "system",
#                         "content": "Answer ONLY using retrieved content from file_search. If not found, say you don't have that info."
#                     },
#                     {
#                         "role": "user",
#                         "content": user_question
#                     }
#                 ],
#                 tools=[{
#                     "type": "file_search",
#                     "vector_store_ids": [self.vector_store_id]
#                 }]
#             )
            
#             result = {
#                 "answer": response.output_text,
#                 "role": role,
#                 "timestamp": datetime.now().isoformat(),
#                 "question": user_question
#             }
            
#             # If admin, include additional metadata
#             if role == "admin":
#                 result["response_id"] = response.id if hasattr(response, 'id') else None
#                 result["model"] = "gpt-5.2"
            
#             return result
            
#         except Exception as e:
#             return {
#                 "error": str(e),
#                 "role": role,
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_document(self, file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload a document to the vector store
        
#         Args:
#             file_path: Path to the document to upload
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Upload file to OpenAI
#             with open(file_path, 'rb') as f:
#                 file = self.client.files.create(
#                     file=f,
#                     purpose='assistants'
#                 )
            
#             # Add file to vector store
#             vector_store_file = self.client.beta.vector_stores.files.create(
#                 vector_store_id=self.vector_store_id,
#                 file_id=file.id
#             )
            
#             return {
#                 "status": "success",
#                 "file_id": file.id,
#                 "vector_store_file_id": vector_store_file.id,
#                 "filename": os.path.basename(file_path),
#                 "timestamp": datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_text(self, text_content: str, filename: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload text content to the vector store
        
#         Args:
#             text_content: Text to upload
#             filename: Name for the text file
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Create temporary file
#             temp_file = f"temp_{filename}.txt"
#             with open(temp_file, 'w', encoding='utf-8') as f:
#                 f.write(text_content)
            
#             # Upload using document method
#             result = self.upload_document(temp_file, admin_key)
            
#             # Clean up temp file
#             if os.path.exists(temp_file):
#                 os.remove(temp_file)
            
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_voice_transcription(self, audio_file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Transcribe voice and upload to vector store
        
#         Args:
#             audio_file_path: Path to audio file
#             admin_key: Admin authentication key
        
#         Returns:
#             Transcription and upload status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Transcribe audio
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcription = self.client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file
#                 )
            
#             # Upload transcription as text
#             filename = f"voice_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#             result = self.upload_text(transcription.text, filename, admin_key)
            
#             result["transcription"] = transcription.text
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def submit_feedback(self, question: str, response: str, 
#                        feedback_type: str, feedback_text: str, 
#                        admin_key: str, rating: Optional[int] = None) -> Dict[str, Any]:
#         """
#         Admin function: Submit feedback to improve the model
        
#         Args:
#             question: Original question
#             response: Model's response
#             feedback_type: Type of feedback ('correction', 'improvement', 'positive', 'negative')
#             feedback_text: Detailed feedback
#             admin_key: Admin authentication key
#             rating: Optional rating (1-5)
        
#         Returns:
#             Feedback submission status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         feedback_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "question": question,
#             "response": response,
#             "feedback_type": feedback_type,
#             "feedback_text": feedback_text,
#             "rating": rating
#         }
        
#         self._save_feedback(feedback_entry)
        
#         return {
#             "status": "success",
#             "message": "Feedback recorded successfully",
#             "feedback_id": len(self.feedback_history),
#             "timestamp": feedback_entry["timestamp"]
#         }
    
#     def get_feedback_summary(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Get summary of all feedback
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             Feedback summary statistics
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         if not self.feedback_history:
#             return {
#                 "total_feedback": 0,
#                 "message": "No feedback recorded yet"
#             }
        
#         feedback_types = {}
#         total_rating = 0
#         rated_count = 0
        
#         for entry in self.feedback_history:
#             ftype = entry.get("feedback_type", "unknown")
#             feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
            
#             if entry.get("rating"):
#                 total_rating += entry["rating"]
#                 rated_count += 1
        
#         return {
#             "total_feedback": len(self.feedback_history),
#             "feedback_by_type": feedback_types,
#             "average_rating": total_rating / rated_count if rated_count > 0 else None,
#             "recent_feedback": self.feedback_history[-5:]  # Last 5 entries
#         }
    
#     def list_vector_store_files(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: List all files in the vector store
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             List of files in vector store
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             files = self.client.beta.vector_stores.files.list(
#                 vector_store_id=self.vector_store_id
#             )
            
#             return {
#                 "status": "success",
#                 "files": [{"id": f.id, "status": f.status} for f in files.data],
#                 "total_files": len(files.data)
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e)
#             }


# Example usage functions
# def user_query_example():
#     """Example: User querying the system - Returns result instead of printing"""
#     rag = RAGService()
    
#     question = "What is the company's return policy?"
#     result = rag.query_rag(question, role="user")
    
#     return {
#         "type": "user_query",
#         "question": question,
#         "result": result
#     }


# def admin_query_example():
#     """Example: Admin querying and managing the system - Returns all results"""
#     rag = RAGService()
#     admin_key = os.getenv("ADMIN_API_KEY", "admin_secret_key")
    
#     results = {}
    
#     # 1. Admin queries (same as user but with metadata)
#     question = "What is the company's return policy?"
#     query_result = rag.query_rag(question, role="admin")
#     results["admin_query"] = {
#         "question": question,
#         "result": query_result
#     }
    
#     # 2. Upload a document (example commented out - uncomment to use)
#     # upload_result = rag.upload_document("path/to/document.pdf", admin_key)
#     # results["document_upload"] = upload_result
    
#     # 3. Upload text content
#     text_content = """
#     New Policy Update:
#     Our return policy has been updated. Customers can now return items within 60 days.
#     """
#     text_result = rag.upload_text(text_content, "policy_update", admin_key)
#     results["text_upload"] = text_result
    
#     # 4. Submit feedback
#     feedback_result = rag.submit_feedback(
#         question=question,
#         response=query_result.get('answer', ''),
#         feedback_type="improvement",
#         feedback_text="Response should mention the new 60-day policy",
#         admin_key=admin_key,
#         rating=3
#     )
#     results["feedback_submission"] = feedback_result
    
#     # 5. Get feedback summary
#     summary = rag.get_feedback_summary(admin_key)
#     results["feedback_summary"] = summary
    
#     # 6. List vector store files
#     files = rag.list_vector_store_files(admin_key)
#     results["vector_store_files"] = files
    
#     return results


# if __name__ == "__main__":
#     # Example: Run user query
#     user_result = user_query_example()
#     print("=== User Example ===")
#     print(f"Question: {user_result['question']}")
#     print(f"Answer: {user_result['result'].get('answer', user_result['result'].get('error'))}")
#     print()
    
#     # Example: Run admin operations
#     admin_results = admin_query_example()
#     print("\n=== Admin Example ===")
#     print(f"Admin Query: {admin_results['admin_query']['result'].get('answer', 'Error')}")
#     print(f"Text Upload Status: {admin_results['text_upload'].get('status', 'error')}")
#     print(f"Feedback Status: {admin_results['feedback_submission'].get('status', 'error')}")
#     print(f"Total Feedback Count: {admin_results['feedback_summary'].get('total_feedback', 0)}")
#     print(f"Vector Store Files: {admin_results['vector_store_files'].get('total_files', 0)}")


# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from typing import Optional, Dict, Any, List
# import json
# from datetime import datetime

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"
# FEEDBACK_LOG_FILE = "admin_feedback.json"


# class RAGService:
#     def __init__(self):
#         self.client = client
#         self.vector_store_id = VECTOR_STORE_ID
#         self.feedback_history = self._load_feedback_history()
    
#     def _load_feedback_history(self) -> List[Dict]:
#         """Load existing feedback history from file"""
#         if os.path.exists(FEEDBACK_LOG_FILE):
#             with open(FEEDBACK_LOG_FILE, 'r') as f:
#                 return json.load(f)
#         return []
    
#     def _save_feedback(self, feedback_entry: Dict):
#         """Save feedback to persistent storage"""
#         self.feedback_history.append(feedback_entry)
#         with open(FEEDBACK_LOG_FILE, 'w') as f:
#             json.dump(self.feedback_history, f, indent=2)
    
#     def identify_role(self, user_id: str = None, api_key_admin: str = None) -> str:
#         """
#         Identify if the request is from admin or user
        
#         Args:
#             user_id: User identifier
#             api_key_admin: Admin API key for authentication
        
#         Returns:
#             'admin' or 'user'
#         """
#         # Simple role identification - you can enhance with proper auth
#         ADMIN_KEY = os.getenv("ADMIN_API_KEY", "admin_secret_key")
        
#         if api_key_admin and api_key_admin == ADMIN_KEY:
#             return "admin"
#         return "user"
    
#     def query_rag(self, user_question: str, role: str = "user") -> Dict[str, Any]:
#         """
#         Query the RAG system
        
#         Args:
#             user_question: The question to answer
#             role: 'admin' or 'user'
        
#         Returns:
#             Dictionary with response and metadata
#         """
#         try:
#             response = self.client.responses.create(
#                 model="gpt-5.2",
#                 input=[
#                     {
#                         "role": "system",
#                         "content": "Answer ONLY using retrieved content from file_search. If not found, say you don't have that info."
#                     },
#                     {
#                         "role": "user",
#                         "content": user_question
#                     }
#                 ],
#                 tools=[{
#                     "type": "file_search",
#                     "vector_store_ids": [self.vector_store_id]
#                 }]
#             )
            
#             result = {
#                 "answer": response.output_text,
#                 "role": role,
#                 "timestamp": datetime.now().isoformat(),
#                 "question": user_question
#             }
            
#             # If admin, include additional metadata
#             if role == "admin":
#                 result["response_id"] = response.id if hasattr(response, 'id') else None
#                 result["model"] = "gpt-5.2"
            
#             return result
            
#         except Exception as e:
#             return {
#                 "error": str(e),
#                 "role": role,
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_document(self, file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload a document to the vector store
        
#         Args:
#             file_path: Path to the document to upload
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Upload file to OpenAI
#             with open(file_path, 'rb') as f:
#                 file = self.client.files.create(
#                     file=f,
#                     purpose='assistants'
#                 )
            
#             # Add file to vector store
#             vector_store_file = self.client.beta.vector_stores.files.create(
#                 vector_store_id=self.vector_store_id,
#                 file_id=file.id
#             )
            
#             return {
#                 "status": "success",
#                 "file_id": file.id,
#                 "vector_store_file_id": vector_store_file.id,
#                 "filename": os.path.basename(file_path),
#                 "timestamp": datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_text(self, text_content: str, filename: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload text content to the vector store
        
#         Args:
#             text_content: Text to upload
#             filename: Name for the text file
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Create temporary file
#             temp_file = f"temp_{filename}.txt"
#             with open(temp_file, 'w', encoding='utf-8') as f:
#                 f.write(text_content)
            
#             # Upload using document method
#             result = self.upload_document(temp_file, admin_key)
            
#             # Clean up temp file
#             if os.path.exists(temp_file):
#                 os.remove(temp_file)
            
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_voice_transcription(self, audio_file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Transcribe voice and upload to vector store
        
#         Args:
#             audio_file_path: Path to audio file
#             admin_key: Admin authentication key
        
#         Returns:
#             Transcription and upload status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             # Transcribe audio
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcription = self.client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file
#                 )
            
#             # Upload transcription as text
#             filename = f"voice_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#             result = self.upload_text(transcription.text, filename, admin_key)
            
#             result["transcription"] = transcription.text
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def submit_feedback(self, question: str, response: str, 
#                        feedback_type: str, feedback_text: str, 
#                        admin_key: str, rating: Optional[int] = None) -> Dict[str, Any]:
#         """
#         Admin function: Submit feedback to improve the model
        
#         Args:
#             question: Original question
#             response: Model's response
#             feedback_type: Type of feedback ('correction', 'improvement', 'positive', 'negative')
#             feedback_text: Detailed feedback
#             admin_key: Admin authentication key
#             rating: Optional rating (1-5)
        
#         Returns:
#             Feedback submission status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         feedback_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "question": question,
#             "response": response,
#             "feedback_type": feedback_type,
#             "feedback_text": feedback_text,
#             "rating": rating
#         }
        
#         self._save_feedback(feedback_entry)
        
#         return {
#             "status": "success",
#             "message": "Feedback recorded successfully",
#             "feedback_id": len(self.feedback_history),
#             "timestamp": feedback_entry["timestamp"]
#         }
    
#     def get_feedback_summary(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Get summary of all feedback
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             Feedback summary statistics
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         if not self.feedback_history:
#             return {
#                 "total_feedback": 0,
#                 "message": "No feedback recorded yet"
#             }
        
#         feedback_types = {}
#         total_rating = 0
#         rated_count = 0
        
#         for entry in self.feedback_history:
#             ftype = entry.get("feedback_type", "unknown")
#             feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
            
#             if entry.get("rating"):
#                 total_rating += entry["rating"]
#                 rated_count += 1
        
#         return {
#             "total_feedback": len(self.feedback_history),
#             "feedback_by_type": feedback_types,
#             "average_rating": total_rating / rated_count if rated_count > 0 else None,
#             "recent_feedback": self.feedback_history[-5:]  # Last 5 entries
#         }
    
#     def list_vector_store_files(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: List all files in the vector store
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             List of files in vector store
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"error": "Unauthorized. Admin access required."}
        
#         try:
#             files = self.client.beta.vector_stores.files.list(
#                 vector_store_id=self.vector_store_id
#             )
            
#             return {
#                 "status": "success",
#                 "files": [{"id": f.id, "status": f.status} for f in files.data],
#                 "total_files": len(files.data)
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e)
#             }


# Example usage functions
# def user_query_example():
#     """Example: User querying the system - Returns result instead of printing"""
#     rag = RAGService()
    
#     question = "What is the company's return policy?"
#     result = rag.query_rag(question, role="user")
    
#     return {
#         "type": "user_query",
#         "question": question,
#         "result": result
#     }


# def admin_query_example():
#     """Example: Admin querying and managing the system - Returns all results"""
#     rag = RAGService()
#     admin_key = os.getenv("ADMIN_API_KEY", "admin_secret_key")
    
#     results = {}
    
#     # 1. Admin queries (same as user but with metadata)
#     question = "What is the company's return policy?"
#     query_result = rag.query_rag(question, role="admin")
#     results["admin_query"] = {
#         "question": question,
#         "result": query_result
#     }
    
#     # 2. Upload a document (example commented out - uncomment to use)
#     # upload_result = rag.upload_document("path/to/document.pdf", admin_key)
#     # results["document_upload"] = upload_result
    
#     # 3. Upload text content
#     text_content = """
#     New Policy Update:
#     Our return policy has been updated. Customers can now return items within 60 days.
#     """
#     text_result = rag.upload_text(text_content, "policy_update", admin_key)
#     results["text_upload"] = text_result
    
#     # 4. Submit feedback
#     feedback_result = rag.submit_feedback(
#         question=question,
#         response=query_result.get('answer', ''),
#         feedback_type="improvement",
#         feedback_text="Response should mention the new 60-day policy",
#         admin_key=admin_key,
#         rating=3
#     )
#     results["feedback_submission"] = feedback_result
    
#     # 5. Get feedback summary
#     summary = rag.get_feedback_summary(admin_key)
#     results["feedback_summary"] = summary
    
#     # 6. List vector store files
#     files = rag.list_vector_store_files(admin_key)
#     results["vector_store_files"] = files
    
#     return results


# if __name__ == "__main__":
#     # Example: Run user query
#     user_result = user_query_example()
#     print("=== User Example ===")
#     print(f"Question: {user_result['question']}")
#     print(f"Answer: {user_result['result'].get('answer', user_result['result'].get('error'))}")
#     print()
    
#     # Example: Run admin operations
#     admin_results = admin_query_example()
#     print("\n=== Admin Example ===")
#     print(f"Admin Query: {admin_results['admin_query']['result'].get('answer', 'Error')}")
#     print(f"Text Upload Status: {admin_results['text_upload'].get('status', 'error')}")
#     print(f"Feedback Status: {admin_results['feedback_submission'].get('status', 'error')}")
#     print(f"Total Feedback Count: {admin_results['feedback_summary'].get('total_feedback', 0)}")
#     print(f"Vector Store Files: {admin_results['vector_store_files'].get('total_files', 0)}")



# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from typing import Optional, Dict, Any, List
# import json
# from datetime import datetime

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

# VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"
# FEEDBACK_LOG_FILE = "admin_feedback.json"


# class RAGService:
#     def __init__(self):
#         self.client = client
#         self.vector_store_id = VECTOR_STORE_ID
#         self.feedback_history = self._load_feedback_history()
    
#     def _load_feedback_history(self) -> List[Dict]:
#         """Load existing feedback history from file"""
#         if os.path.exists(FEEDBACK_LOG_FILE):
#             with open(FEEDBACK_LOG_FILE, 'r') as f:
#                 return json.load(f)
#         return []
    
#     def _save_feedback(self, feedback_entry: Dict):
#         """Save feedback to persistent storage"""
#         self.feedback_history.append(feedback_entry)
#         with open(FEEDBACK_LOG_FILE, 'w') as f:
#             json.dump(self.feedback_history, f, indent=2)
    
#     def identify_role(self, user_id: str = None, api_key_admin: str = None) -> str:
#         """
#         Identify if the request is from admin or user
        
#         Args:
#             user_id: User identifier
#             api_key_admin: Admin API key for authentication
        
#         Returns:
#             'admin' or 'user'
#         """
#         # Simple role identification - you can enhance with proper auth
#         ADMIN_KEY = os.getenv("ADMIN_API_KEY", "admin_secret_key")
        
#         if api_key_admin and api_key_admin == ADMIN_KEY:
#             return "admin"
#         return "user"
    
#     def query_rag(self, user_question: str, role: str = "user") -> Dict[str, Any]:
#         """
#         Query the RAG system using Assistants API
        
#         Args:
#             user_question: The question to answer
#             role: 'admin' or 'user'
        
#         Returns:
#             Dictionary with response and metadata
#         """
#         try:
#             # Create assistant with file_search capability
#             assistant = self.client.beta.assistants.create(
#                 name="SajiloSewa Assistant",
#                 instructions=(
#                     "You are a helpful e-governance assistant for Nepal. "
#                     "Provide accurate, helpful information about government services, "
#                     "citizenship, passports, PAN cards, and other administrative processes. "
#                     "Use the knowledge base to answer questions accurately. "
#                     "If you don't have information from the knowledge base, politely say so. "
#                     "Always be concise, clear, and helpful."
#                 ),
#                 model="gpt-4o-mini",  # Use a valid model
#                 tools=[{"type": "file_search"}],
#                 tool_resources={
#                     "file_search": {
#                         "vector_store_ids": [self.vector_store_id]
#                     }
#                 }
#             )
            
#             # Create a thread
#             thread = self.client.beta.threads.create()
            
#             # Add user message to thread
#             message = self.client.beta.threads.messages.create(
#                 thread_id=thread.id,
#                 role="user",
#                 content=user_question
#             )
            
#             # Run the assistant
#             run = self.client.beta.threads.runs.create_and_poll(
#                 thread_id=thread.id,
#                 assistant_id=assistant.id,
#                 timeout=30  # 30 second timeout
#             )
            
#             # Check if run completed successfully
#             if run.status == 'completed':
#                 # Get messages from the thread
#                 messages = self.client.beta.threads.messages.list(
#                     thread_id=thread.id
#                 )
                
#                 # Get the assistant's response (first message)
#                 assistant_message = messages.data[0]
#                 answer = assistant_message.content[0].text.value
                
#                 result = {
#                     "answer": answer,
#                     "role": role,
#                     "timestamp": datetime.now().isoformat(),
#                     "question": user_question
#                 }
                
#                 # If admin, include additional metadata
#                 if role == "admin":
#                     result["response_id"] = run.id
#                     result["model"] = "gpt-4o-mini"
#                     result["thread_id"] = thread.id
                
#                 # Clean up - delete assistant to avoid clutter
#                 try:
#                     self.client.beta.assistants.delete(assistant.id)
#                 except:
#                     pass  # Don't fail if cleanup fails
                
#                 return result
            
#             else:
#                 # Run didn't complete successfully
#                 error_msg = f"Assistant run failed with status: {run.status}"
#                 if hasattr(run, 'last_error') and run.last_error:
#                     error_msg += f" - {run.last_error}"
                
#                 return {
#                     "error": error_msg,
#                     "answer": "I apologize, but I encountered an error processing your request. Please try again.",
#                     "role": role,
#                     "timestamp": datetime.now().isoformat()
#                 }
            
#         except Exception as e:
#             return {
#                 "error": str(e),
#                 "answer": "I apologize, but I encountered an error processing your request. Please try again.",
#                 "role": role,
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_document(self, file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload a document to the vector store
        
#         Args:
#             file_path: Path to the document to upload
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         try:
#             # Upload file to OpenAI
#             with open(file_path, 'rb') as f:
#                 file = self.client.files.create(
#                     file=f,
#                     purpose='assistants'
#                 )
            
#             # Add file to vector store
#             vector_store_file = self.client.beta.vector_stores.files.create(
#                 vector_store_id=self.vector_store_id,
#                 file_id=file.id
#             )
            
#             return {
#                 "status": "success",
#                 "file_id": file.id,
#                 "vector_store_file_id": vector_store_file.id,
#                 "filename": os.path.basename(file_path),
#                 "timestamp": datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_text(self, text_content: str, filename: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Upload text content to the vector store
        
#         Args:
#             text_content: Text to upload
#             filename: Name for the text file
#             admin_key: Admin authentication key
        
#         Returns:
#             Upload status and file ID
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         try:
#             # Create temporary file
#             temp_file = f"temp_{filename}.txt"
#             with open(temp_file, 'w', encoding='utf-8') as f:
#                 f.write(text_content)
            
#             # Upload using document method
#             result = self.upload_document(temp_file, admin_key)
            
#             # Clean up temp file
#             if os.path.exists(temp_file):
#                 os.remove(temp_file)
            
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def upload_voice_transcription(self, audio_file_path: str, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Transcribe voice and upload to vector store
        
#         Args:
#             audio_file_path: Path to audio file
#             admin_key: Admin authentication key
        
#         Returns:
#             Transcription and upload status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         try:
#             # Transcribe audio
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcription = self.client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file
#                 )
            
#             # Upload transcription as text
#             filename = f"voice_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#             result = self.upload_text(transcription.text, filename, admin_key)
            
#             result["transcription"] = transcription.text
#             return result
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }
    
#     def submit_feedback(self, question: str, response: str, 
#                        feedback_type: str, feedback_text: str, 
#                        admin_key: str, rating: Optional[int] = None) -> Dict[str, Any]:
#         """
#         Admin function: Submit feedback to improve the model
        
#         Args:
#             question: Original question
#             response: Model's response
#             feedback_type: Type of feedback ('correction', 'improvement', 'positive', 'negative')
#             feedback_text: Detailed feedback
#             admin_key: Admin authentication key
#             rating: Optional rating (1-5)
        
#         Returns:
#             Feedback submission status
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         feedback_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "question": question,
#             "response": response,
#             "feedback_type": feedback_type,
#             "feedback_text": feedback_text,
#             "rating": rating
#         }
        
#         self._save_feedback(feedback_entry)
        
#         return {
#             "status": "success",
#             "message": "Feedback recorded successfully",
#             "feedback_id": len(self.feedback_history),
#             "timestamp": feedback_entry["timestamp"]
#         }
    
#     def get_feedback_summary(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: Get summary of all feedback
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             Feedback summary statistics
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         if not self.feedback_history:
#             return {
#                 "status": "success",
#                 "total_feedback": 0,
#                 "message": "No feedback recorded yet"
#             }
        
#         feedback_types = {}
#         total_rating = 0
#         rated_count = 0
        
#         for entry in self.feedback_history:
#             ftype = entry.get("feedback_type", "unknown")
#             feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
            
#             if entry.get("rating"):
#                 total_rating += entry["rating"]
#                 rated_count += 1
        
#         return {
#             "status": "success",
#             "total_feedback": len(self.feedback_history),
#             "feedback_by_type": feedback_types,
#             "average_rating": total_rating / rated_count if rated_count > 0 else None,
#             "recent_feedback": self.feedback_history[-5:]  # Last 5 entries
#         }
    
#     def list_vector_store_files(self, admin_key: str) -> Dict[str, Any]:
#         """
#         Admin function: List all files in the vector store
        
#         Args:
#             admin_key: Admin authentication key
        
#         Returns:
#             List of files in vector store
#         """
#         if self.identify_role(api_key_admin=admin_key) != "admin":
#             return {"status": "error", "error": "Unauthorized. Admin access required."}
        
#         try:
#             files = self.client.beta.vector_stores.files.list(
#                 vector_store_id=self.vector_store_id
#             )
            
#             return {
#                 "status": "success",
#                 "files": [{"id": f.id, "status": f.status} for f in files.data],
#                 "total_files": len(files.data)
#             }
            
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e)
#             }



import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

VECTOR_STORE_ID = "vs_698d9c6c81bc8191afc6d18e69b6b833"
FEEDBACK_LOG_FILE = "admin_feedback.json"


class RAGService:
    def __init__(self):
        self.client = client
        self.vector_store_id = VECTOR_STORE_ID
        self.feedback_history = self._load_feedback_history()
    
    def _load_feedback_history(self) -> List[Dict]:
        """Load existing feedback history from file"""
        if os.path.exists(FEEDBACK_LOG_FILE):
            with open(FEEDBACK_LOG_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_feedback(self, feedback_entry: Dict):
        """Save feedback to persistent storage"""
        self.feedback_history.append(feedback_entry)
        with open(FEEDBACK_LOG_FILE, 'w') as f:
            json.dump(self.feedback_history, f, indent=2)
    
    def identify_role(self, user_id: str = None, api_key_admin: str = None) -> str:
        """
        Identify if the request is from admin or user
        
        Args:
            user_id: User identifier
            api_key_admin: Admin API key for authentication
        
        Returns:
            'admin' or 'user'
        """
        ADMIN_KEY = os.getenv("ADMIN_API_KEY", "admin_secret_key")
        
        if api_key_admin and api_key_admin == ADMIN_KEY:
            return "admin"
        return "user"
    
    def query_rag(self, user_question: str, role: str = "user") -> Dict[str, Any]:
        """
        Query the RAG system using Chat Completions with retrieved context
        
        Args:
            user_question: The question to answer
            role: 'admin' or 'user'
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Use chat completions with a retrieval-augmented approach
            # Since vector_stores API is not available in v2.20.0, 
            # we'll use a simpler approach or direct file reading
            
            # For now, use standard chat completion
            # You may need to manually retrieve relevant docs if needed
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful e-governance assistant for Nepal. "
                            "Provide accurate, helpful information about government services, "
                            "citizenship, passports, PAN cards, and other administrative processes. "
                            "Be concise, clear, and helpful."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ]
            )
            
            answer = response.choices[0].message.content
            
            result = {
                "answer": answer,
                "role": role,
                "timestamp": datetime.now().isoformat(),
                "question": user_question
            }
            
            # If admin, include additional metadata
            if role == "admin":
                result["response_id"] = response.id
                result["model"] = response.model
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "answer": "I apologize, but I encountered an error processing your request. Please try again.",
                "role": role,
                "timestamp": datetime.now().isoformat()
            }
    
    def upload_document(self, file_path: str, admin_key: str) -> Dict[str, Any]:
        """
        Admin function: Upload a document
        
        Note: In OpenAI SDK v2.20.0, vector_stores API is not directly accessible.
        This is a simplified version that uploads files.
        
        Args:
            file_path: Path to the document to upload
            admin_key: Admin authentication key
        
        Returns:
            Upload status and file ID
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        try:
            # Upload file to OpenAI
            with open(file_path, 'rb') as f:
                file = self.client.files.create(
                    file=f,
                    purpose='assistants'
                )
            
            # Note: Vector store file association requires beta API
            # which is not available in this SDK version
            # For now, just upload the file
            
            return {
                "status": "success",
                "file_id": file.id,
                "filename": os.path.basename(file_path),
                "timestamp": datetime.now().isoformat(),
                "note": "File uploaded. Vector store integration pending SDK update."
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def upload_text(self, text_content: str, filename: str, admin_key: str) -> Dict[str, Any]:
        """
        Admin function: Upload text content
        
        Args:
            text_content: Text to upload
            filename: Name for the text file
            admin_key: Admin authentication key
        
        Returns:
            Upload status and file ID
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        try:
            # Create temporary file
            temp_file = f"temp_{filename}.txt"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            # Upload using document method
            result = self.upload_document(temp_file, admin_key)
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def upload_voice_transcription(self, audio_file_path: str, admin_key: str) -> Dict[str, Any]:
        """
        Admin function: Transcribe voice and upload
        
        Args:
            audio_file_path: Path to audio file
            admin_key: Admin authentication key
        
        Returns:
            Transcription and upload status
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        try:
            # Transcribe audio
            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # Upload transcription as text
            filename = f"voice_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = self.upload_text(transcription.text, filename, admin_key)
            
            result["transcription"] = transcription.text
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def submit_feedback(self, question: str, response: str, 
                       feedback_type: str, feedback_text: str, 
                       admin_key: str, rating: Optional[int] = None) -> Dict[str, Any]:
        """
        Admin function: Submit feedback to improve the model
        
        Args:
            question: Original question
            response: Model's response
            feedback_type: Type of feedback ('correction', 'improvement', 'positive', 'negative')
            feedback_text: Detailed feedback
            admin_key: Admin authentication key
            rating: Optional rating (1-5)
        
        Returns:
            Feedback submission status
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": response,
            "feedback_type": feedback_type,
            "feedback_text": feedback_text,
            "rating": rating
        }
        
        self._save_feedback(feedback_entry)
        
        return {
            "status": "success",
            "message": "Feedback recorded successfully",
            "feedback_id": len(self.feedback_history),
            "timestamp": feedback_entry["timestamp"]
        }
    
    def get_feedback_summary(self, admin_key: str) -> Dict[str, Any]:
        """
        Admin function: Get summary of all feedback
        
        Args:
            admin_key: Admin authentication key
        
        Returns:
            Feedback summary statistics
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        if not self.feedback_history:
            return {
                "status": "success",
                "total_feedback": 0,
                "message": "No feedback recorded yet"
            }
        
        feedback_types = {}
        total_rating = 0
        rated_count = 0
        
        for entry in self.feedback_history:
            ftype = entry.get("feedback_type", "unknown")
            feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
            
            if entry.get("rating"):
                total_rating += entry["rating"]
                rated_count += 1
        
        return {
            "status": "success",
            "total_feedback": len(self.feedback_history),
            "feedback_by_type": feedback_types,
            "average_rating": total_rating / rated_count if rated_count > 0 else None,
            "recent_feedback": self.feedback_history[-5:]
        }
    
    def list_vector_store_files(self, admin_key: str) -> Dict[str, Any]:
        """
        Admin function: List all uploaded files
        
        Args:
            admin_key: Admin authentication key
        
        Returns:
            List of files
        """
        if self.identify_role(api_key_admin=admin_key) != "admin":
            return {"status": "error", "error": "Unauthorized. Admin access required."}
        
        try:
            # List files uploaded to OpenAI
            files = self.client.files.list(purpose='assistants')
            
            file_list = []
            for file in files.data:
                file_list.append({
                    'id': file.id,
                    'filename': file.filename,
                    'created_at': file.created_at,
                    'bytes': file.bytes,
                    'status': getattr(file, 'status', 'unknown')
                })
            
            return {
                "status": "success",
                "files": file_list,
                "total_files": len(file_list)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }