from django.db import models


class NearEarthObject(models.Model):
    nasa_jpl_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    absolute_magnitude_h = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
    )
    estimated_diameter_min_km = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=True,
        blank=True,
    )
    estimated_diameter_max_km = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=True,
        blank=True,
    )
    is_potentially_hazardous = models.BooleanField()
    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class CloseApproach(models.Model):
    near_earth_object = models.ForeignKey(
        NearEarthObject,
        on_delete=models.CASCADE,
        related_name="close_approaches",
    )
    close_approach_date = models.DateField()
    epoch_date_close_approach = models.BigIntegerField()
    relative_velocity_kps = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=True,
        blank=True,
    )
    miss_distance_km = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        blank=True,
    )
    orbiting_body = models.CharField(max_length=64, default="Earth")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["close_approach_date"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "near_earth_object",
                    "epoch_date_close_approach",
                    "orbiting_body",
                ],
                name="unique_close_approach_per_object_epoch_body",
            )
        ]

    def __str__(self):
        return f"{self.near_earth_object.name} - {self.close_approach_date}"
    
class ApiSyncRun(models.Model):
    class Status(models.TextChoices):
        STARTED = "started", "Started"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        PARTIAL_SUCCESS = "partial_success", "Partial success"

    source = models.CharField(max_length=64)
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.STARTED,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    records_requested = models.PositiveIntegerField(default=0)
    records_created = models.PositiveIntegerField(default=0)
    records_updated = models.PositiveIntegerField(default=0)
    records_skipped = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.source} sync - {self.status} - {self.started_at}"