from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="название")
    slug = models.SlugField(
        max_length=180,
        blank=True,
        null=True,
        unique=True,
        verbose_name="URL-идентификатор",
    )
    max_duration = models.PositiveIntegerField(verbose_name="лимит выступления")
    is_long = models.GeneratedField(
        expression=models.Case(
            models.When(max_duration__gte=15, then=models.Value(True)),
            default=models.Value(False),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="длительное мероприятие",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"

    def __str__(self):
        return f"{self.name} (лимит: {self.max_duration} мин)"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name))
            slug = base_slug or "event"
            unique_slug = slug
            counter = 1
            while Event.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.slug:
            return reverse("events:detail_by_slug", kwargs={"slug": self.slug})
        return reverse("events:detail", kwargs={"event_id": self.id})
