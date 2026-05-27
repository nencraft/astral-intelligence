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
    is_potentially_hazardous = models.BooleanField(default=False)
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
    epoch_date_close_approach = models.BigIntegerField(
        null=True,
        blank=True,
    )
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

    def __str__(self):
        return f"{self.near_earth_object.name} - {self.close_approach_date}"