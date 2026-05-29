from rest_framework import serializers
from .models import CloseApproach, NearEarthObject


class NearEarthObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearEarthObject
        fields = [
            "id",
            "nasa_jpl_id",
            "name",
            "absolute_magnitude_h",
            "estimated_diameter_min_km",
            "estimated_diameter_max_km",
            "is_potentially_hazardous",
            "created_at",
            "updated_at",
        ]

class CloseApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseApproach
        fields = [
            "id",
            "near_earth_object",
            "close_approach_date",
            "epoch_date_close_approach",
            "relative_velocity_kps",
            "miss_distance_km",
            "orbiting_body",
            "created_at",
            "updated_at",
        ]