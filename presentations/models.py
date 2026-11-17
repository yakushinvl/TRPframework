from django.db import models
from events.models import Event
from students.models import Student


class Presentation(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="presentations",
        verbose_name="мероприятие",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="presentations",
        verbose_name="студент",
    )
    title = models.CharField(max_length=250, verbose_name="тема доклада")
    duration = models.PositiveIntegerField(verbose_name="время доклада")
    score_1 = models.FloatField(verbose_name="балл за доклад")
    score_2 = models.FloatField(verbose_name="балл за ответы")

    class Meta:
        ordering = ["id"]
        verbose_name = "выступление"
        verbose_name_plural = "выступления"

    @property
    def total_score(self):
        return round(self.score_1 + self.score_2, 2)

    @property
    def result(self):
        score = self.total_score
        if score >= 9.0:
            return "1 место"
        elif score >= 8.0:
            return "2 место"
        elif score >= 7.0:
            return "3 место"
        return "участник"

    def check_duration(self):
        if self.duration <= self.event.max_duration:
            return "в регламенте"
        return "превышен"

    def __str__(self):
        return f"{self.student.name} — «{self.title}»"
