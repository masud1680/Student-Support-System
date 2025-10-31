from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


# --- Custom User Model ---
# It's best practice to use a custom User model from the start.
# Don't forget to add 'AUTH_USER_MODEL = "your_app_name.User"' to your settings.py
# (replace 'your_app_name' with the actual name of this app).

# class User(AbstractUser):
#     """
#     Custom User model inheriting from AbstractUser.
#     This model is used for both Students and Teachers.
#     """
#     ROLE_CHOICES = (
#         ('Student', 'Student'),
#         ('Teacher', 'Teacher'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')

#     def is_student(self):
#         return self.role == 'Student'

#     def is_teacher(self):
#         return self.role == 'Teacher'

# # --- Course Models ---

# class Course(models.Model):
#     """
#     Represents a course that students can enroll in and teachers can support.
#     """
#     course_name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     # You could add other fields like 'start_date', 'end_date', etc.

#     def __str__(self):
#         return self.course_name

# class Enrollment(models.Model):
#     """
#     Links a Student (User) to a Course they are enrolled in.
#     This is a many-to-many "through" table.
#     """
#     student = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='enrollments',
#         limit_choices_to={'role': 'Student'}  # Ensures only students can enroll
#     )
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='enrollments'
#     )
#     enrollment_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         # Ensures a student can't enroll in the same course twice
#         unique_together = ('student', 'course')

#     def __str__(self):
#         return f"{self.student.username} enrolled in {self.course.course_name}"

# class CourseAssignment(models.Model):
#     """
#     Assigns a Teacher (User) to a Course they are responsible for supporting.
#     This is also a many-to-many "through" table.
#     """
#     teacher = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='assignments',
#         limit_choices_to={'role': 'Teacher'}  # Ensures only teachers can be assigned
#     )
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='assignments'
#     )

#     class Meta:
#         # Prevents assigning the same teacher to the same course multiple times
#         unique_together = ('teacher', 'course')

#     def __str__(self):
#         return f"{self.teacher.username} supports {self.course.course_name}"

# # --- Support System Models ---

# class SupportTicket(models.Model):
#     """
#     Represents a single support request (ticket) from a student
#     for a specific course.
#     """
#     STATUS_CHOICES = (
#         ('Open', 'Open'),
#         ('In Progress', 'In Progress'),
#         ('Closed', 'Closed'),
#     )
#     PRIORITY_CHOICES = (
#         ('Low', 'Low'),
#         ('Medium', 'Medium'),
#         ('High', 'High'),
#     )

#     title = models.CharField(max_length=255)
#     student = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='created_tickets',
#         limit_choices_to={'role': 'Student'}
#     )
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='support_tickets'
#     )
#     assigned_teacher = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,  # If teacher is deleted, ticket remains
#         null=True,
#         blank=True,
#         related_name='assigned_tickets',
#         limit_choices_to={'role': 'Teacher'}
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"[{self.status}] {self.title} ({self.student.username})"

# class SupportMessage(models.Model):
#     """
#     Represents a single message (reply) within a support ticket.
#     This allows for a conversation thread.
#     """
#     ticket = models.ForeignKey(
#         SupportTicket,
#         on_delete=models.CASCADE,
#         related_name='messages'
#     )
#     sender = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='sent_messages'
#     )
#     message_text = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['sent_at']  # Show messages in chronological order

#     def __str__(self):
#         return f"Message by {self.sender.username} on ticket {self.ticket.id}"
