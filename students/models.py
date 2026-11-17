from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200, verbose_name="фио студента")
    group = models.CharField(max_length=50, verbose_name="группа")

    class Meta:
        ordering = ["name"]
        verbose_name = "студент"
        verbose_name_plural = "студенты"

    def __str__(self):
        return f"{self.name} ({self.group})"
