from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Root endpoint - API info
    path('', views.home, name='home'),  # Keep this with JsonResponse version
    
    # ==================== USER ENDPOINTS ====================
    # Original chat endpoints (backward compatible)
    path('speak/', views.speak_text, name='speak_text'),
    path('api/chat/', views.chat_api, name='chat_api'),
    
    # Utility endpoints
    path('api/check-role/', views.check_role, name='check_role'),
    path('api/chat-history/', views.chat_history, name='chat_history'),
    
    # ==================== ADMIN ENDPOINTS ====================
    # Admin document management
    path('api/admin/upload-document/', views.admin_upload_document, name='admin_upload_document'),
    path('api/admin/upload-text/', views.admin_upload_text, name='admin_upload_text'),
    path('api/admin/upload-voice/', views.admin_upload_voice, name='admin_upload_voice'),
    
    # Admin feedback management
    path('api/admin/feedback/', views.admin_submit_feedback, name='admin_submit_feedback'),
    path('api/admin/feedback-summary/', views.admin_feedback_summary, name='admin_feedback_summary'),
    
    # Admin file management
    path('api/admin/list-files/', views.admin_list_files, name='admin_list_files'),
]
