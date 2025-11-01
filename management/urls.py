# from django.urls import path
# from management.views import Home

# urlpatterns = [
#     path('', Home, name='home'),
    
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/create/', views.create_meeting, name='create_meeting'),
    path('teacher/update/<int:meeting_id>/', views.update_meeting, name='update_meeting'),
    path('teacher/stop/<int:meeting_id>/', views.stop_meeting, name='stop_meeting'),
    path('teacher/tickets/<int:meeting_id>/', views.manage_tickets, name='manage_tickets'),
    path('teacher/update-ticket/', views.update_ticket_status, name='update_ticket_status'),
    path('teacher/live-queue/<int:meeting_id>/', views.live_queue, name='live_queue'),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/create-ticket/<int:meeting_id>/', views.create_ticket, name='create_ticket'),
    path('student/live-queue/<int:meeting_id>/', views.live_queue, name='student_live_queue'),
]
