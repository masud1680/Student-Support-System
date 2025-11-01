from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Meeting, Ticket
from .forms import MeetingForm, TicketForm
from django.http import JsonResponse
from django.utils import timezone
import json

# ---------------- Teacher Views ----------------
@login_required
def teacher_dashboard(request):
    if not request.user.is_staff: return redirect('student_dashboard')
    meetings = Meeting.objects.filter(teacher=request.user).order_by('created_at')
    return render(request,'support/teacher_dashboard.html',{'meetings':meetings})

@login_required
def create_meeting(request):
    if not request.user.is_staff: return redirect('teacher_dashboard')
    form = MeetingForm(request.POST or None)
    if form.is_valid():
        meeting = form.save(commit=False)
        meeting.teacher = request.user
        meeting.save()
        messages.success(request,'Meeting created!')
        return redirect('teacher_dashboard')
    return render(request,'support/create_meeting.html',{'form':form})

@login_required
def update_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, teacher=request.user)
    form = MeetingForm(request.POST or None, instance=meeting)
    if form.is_valid():
        form.save()
        messages.success(request,'Meeting updated!')
        return redirect('teacher_dashboard')
    return render(request,'support/update_meeting.html',{'form':form,'meeting':meeting})

@login_required
def stop_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, teacher=request.user)
    meeting.status='stopped'
    meeting.save()
    Ticket.objects.filter(meeting=meeting,status__in=['waiting','joined']).update(status='completed')
    messages.success(request,'Meeting stopped.')
    return redirect('teacher_dashboard')

@login_required
def manage_tickets(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, teacher=request.user)
    return render(request,'support/teacher_manage_tickets.html',{'meeting':meeting})

@login_required
def update_ticket_status(request):
    if not request.user.is_staff: 
        return JsonResponse({'error':'Unauthorized'},status=403)
    
    if request.method=='POST':
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        action = data.get('action')
        ticket = Ticket.objects.get(id=ticket_id)
        if action=='start': ticket.status='joined'
        elif action=='complete': ticket.status='completed'
        ticket.save()
        return JsonResponse({'success':True,'ticket_status':ticket.status})
    return JsonResponse({'error':'Invalid request'},status=400)

@login_required
def live_queue(request, meeting_id):
    meeting = get_object_or_404(Meeting,id=meeting_id)

    if request.user.is_staff:
        tickets = Ticket.objects.filter(meeting=meeting).order_by('serial_number')
        ticket_list = []

        for t in tickets:
           
            ticket_list.append({
                'id': t.id,
                'student': f" {t.student.first_name} {t.student.last_name}",
                'problem_text': t.problem_text,
                'status': t.status,
                'serial_number': t.serial_number,
                
            })
            
        return JsonResponse({'tickets': ticket_list})
    else:
        ticket = Ticket.objects.filter(student=request.user, meeting=meeting, status__in=['waiting','joined']).first()
        position = None
        time_left = None
        if ticket:
            waiting_before = Ticket.objects.filter(meeting=meeting, status='waiting', serial_number__lt=ticket.serial_number).count()
            position = waiting_before + 1
            if ticket.status=='joined':
                end_time = ticket.meeting.end_time()
                time_left = max(0,int((end_time - timezone.now()).total_seconds()))
        return JsonResponse({'ticket': {'serial_number':ticket.serial_number,'status':ticket.status,'position':position,'time_left':time_left} if ticket else None})

# ---------------- Student Views ----------------
@login_required
def student_dashboard(request):
    if request.user.is_staff: 
        return redirect('teacher_dashboard')
    
    active_meetings = Meeting.objects.filter(status__in=['scheduled','active']).order_by('created_at')
    return render(request,'support/student_dashboard.html',{'active_meetings':active_meetings})

@login_required
def create_ticket(request, meeting_id):
    meeting = get_object_or_404(Meeting,id=meeting_id)
    active_ticket = Ticket.objects.filter(student=request.user,meeting=meeting,status__in=['waiting','joined']).first()
    if active_ticket:
        messages.error(request,'You already have an active ticket.')
        return redirect('student_dashboard')
    form = TicketForm(request.POST or None)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.student=request.user
        ticket.meeting=meeting
        ticket.save()
        messages.success(request,'Ticket submitted!')
        return redirect('student_dashboard')
    return render(request,'support/student_create_ticket.html',{'form':form,'meeting':meeting})
