from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ("planned", "Запланировано"),
        ("in_progress", "В процессе"),
        ("completed", "Завершено"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def participant_count(self):
        return self.participants.count()


class Participant(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="Событие",
    )
    registered_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
