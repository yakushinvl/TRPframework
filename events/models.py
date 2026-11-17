from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="название")
    max_duration = models.PositiveIntegerField(verbose_name="лимит выступления")

    class Meta:
        ordering = ["name"]
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"

    def __str__(self):
        return f"{self.name} (лимит: {self.max_duration} мин)"
