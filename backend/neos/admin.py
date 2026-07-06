from django.contrib import admin

from .models import ApiSyncRun, CloseApproach, NearEarthObject


@admin.register(NearEarthObject)
class NearEarthObjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nasa_jpl_id",
        "is_potentially_hazardous",
        "estimated_diameter_min_km",
        "estimated_diameter_max_km",
    )
    search_fields = ("name", "nasa_jpl_id")
    list_filter = ("is_potentially_hazardous",)


@admin.register(CloseApproach)
class CloseApproachAdmin(admin.ModelAdmin):
    list_display = (
        "near_earth_object",
        "close_approach_date",
        "miss_distance_km",
        "relative_velocity_kps",
        "orbiting_body",
    )
    search_fields = (
        "near_earth_object__name",
        "near_earth_object__nasa_jpl_id",
    )
    list_filter = ("orbiting_body", "close_approach_date")

@admin.register(ApiSyncRun)
class ApiSyncRunAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "status",
        "start_date",
        "end_date",
        "started_at",
        "finished_at",
        "records_created",
        "records_updated",
        "records_skipped",
    )
    list_filter = ("source", "status", "started_at")
    search_fields = ("source", "error_message")
    readonly_fields = ("started_at",)