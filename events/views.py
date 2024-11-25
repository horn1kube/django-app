from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Event, Participant
from .forms import EventForm, ParticipantForm


def event_list(request):
    status_translation = {
        "planned": "Запланировано",
        "in_progress": "В процессе",
        "completed": "Завершено",
    }

    status_counts = (
        Event.objects.values("status").annotate(count=Count("id")).order_by("status")
    )

    title = request.GET.get("title", "")
    location = request.GET.get("location", "")
    status = request.GET.get("status", "")
    start_datetime = request.GET.get("start_datetime", "")

    sort_field = request.GET.get("sort_field", "start_datetime")
    sort_order = request.GET.get("sort_order", "asc")

    if sort_order == "desc":
        sort_field = "-" + sort_field

    events = Event.objects.all()

    if title:
        events = events.filter(title__icontains=title)
    if location:
        events = events.filter(location__icontains=location)
    if status:
        events = events.filter(status=status)
    if start_datetime:
        events = events.filter(start_datetime__gte=start_datetime)

    paginator = Paginator(events.order_by(sort_field), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    translated_status_counts = [
        {
            "status": status_translation.get(
                status_stat["status"], status_stat["status"]
            ),
            "count": status_stat["count"],
            "status_internal": status_stat["status"],
        }
        for status_stat in status_counts
    ]

    return render(
        request,
        "events/event_list.html",
        {
            "page_obj": page_obj,
            "status_counts": translated_status_counts,
            "current_status": status,
            "title": title,
            "location": location,
            "start_datetime": start_datetime,
            "sort_field": sort_field,
            "sort_order": sort_order,
        },
    )


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all()

    return render(
        request,
        "events/event_participants.html",
        {"event": event, "participants": participants},
    )


def event_register_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = ParticipantForm()

    return render(request, "events/event_register_participant.html", {"form": form})


def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_edit.html", {"form": form, "event": event})


def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")

    return render(request, "events/event_delete_confirm.html", {"event": event})


def add_participant(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.event = event
            participant.save()
            return redirect("event_participants", event_id=event.id)
    else:
        form = ParticipantForm()

    return render(
        request, "events/add_participant.html", {"form": form, "event": event}
    )


def delete_participant(request, event_id, participant_id):
    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(Participant, id=participant_id)

    if request.method == "POST":
        participant.delete()
        return redirect("event_participants", event_id=event.id)

    return render(
        request,
        "events/delete_participant.html",
        {"participant": participant, "event": event},
    )
