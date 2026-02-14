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