from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("event/<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("event/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path(
        "register/", views.event_register_participant, name="event_register_participant"
    ),
    path(
        "event/<int:event_id>/participant/add/",
        views.add_participant,
        name="add_participant",
    ),
    path(
        "event/<int:event_id>/participant/<int:participant_id>/delete/",
        views.delete_participant,
        name="delete_participant",
    ),
    path(
        "event/<int:event_id>/participants/",
        views.event_participants,
        name="event_participants",
    ),
]
