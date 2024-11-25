from django.contrib import admin
from .models import Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "end_datetime", "status", "updated_at")
    list_filter = ("status", "start_datetime")
    search_fields = ("title", "location")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "event", "registered_at")
    search_fields = ("name", "email")
