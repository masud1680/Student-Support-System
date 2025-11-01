from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Meeting(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    title = models.CharField(max_length=255)
    meeting_link = models.CharField(max_length=300, default="google.com")
   
    duration_minutes = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=20, choices=[('scheduled','Scheduled'),('active','Active'),('stopped','Stopped')], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.title} "

class Ticket(models.Model):
    STATUS_CHOICES = [('waiting','Waiting'),('joined','Joined'),('completed','Completed')]
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='tickets')
    problem_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    serial_number = models.PositiveIntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = Ticket.objects.filter(meeting=self.meeting).count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - #{self.serial_number} ({self.status})"
