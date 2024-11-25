from django import forms
from .models import Event, Participant


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "start_datetime",
            "end_datetime",
            "location",
            "status",
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ParticipantForm(forms.ModelForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(), empty_label="Выберите событие"
    )

    class Meta:
        model = Participant
        fields = ["name", "email", "event"]
