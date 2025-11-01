from django import forms
from .models import Meeting, Ticket

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'meeting_link', 'duration_minutes']
        widgets = {
            'title': forms.TextInput(attrs={'class':'border p-2 w-full rounded','placeholder':'Meeting Title'}),
            # 'date': forms.DateInput(attrs={'type':'date','class':'border p-2 w-full rounded'}),
            # 'start_time': forms.TimeInput(attrs={'type':'time','class':'border p-2 w-full rounded'}),
            'duration_minutes': forms.NumberInput(attrs={'class':'border p-2 w-full rounded','min':1}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['problem_text']
        widgets = {'problem_text': forms.Textarea(attrs={'class':'border p-2 w-full rounded','rows':4,'placeholder':'Describe your problem'})}
