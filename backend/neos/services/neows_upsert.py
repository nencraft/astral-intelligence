from dataclasses import dataclass

from django.utils import timezone

from neos.models import CloseApproach, NearEarthObject


@dataclass
class UpsertResult:
    objects_created: int = 0
    objects_updated: int = 0
    approaches_created: int = 0
    approaches_updated: int = 0


def upsert_normalized_object(normalized_object, synced_at=None):
    synced_at = synced_at or timezone.now()
    result = UpsertResult()

    neo_data = normalized_object["neo"]
    close_approaches = normalized_object.get("close_approaches", [])

    nasa_jpl_id = neo_data["nasa_jpl_id"]
    neo_defaults = {
        "name": neo_data["name"],
        "absolute_magnitude_h": neo_data.get("absolute_magnitude_h"),
        "estimated_diameter_min_km": neo_data.get(
            "estimated_diameter_min_km"
        ),
        "estimated_diameter_max_km": neo_data.get(
            "estimated_diameter_max_km"
        ),
        "is_potentially_hazardous": neo_data.get(
            "is_potentially_hazardous",
            False,
        ),
        "last_synced_at": synced_at,
    }

    neo, created = NearEarthObject.objects.update_or_create(
        nasa_jpl_id=nasa_jpl_id,
        defaults=neo_defaults,
    )

    if created:
        result.objects_created += 1
    else:
        result.objects_updated += 1

    for approach_data in close_approaches:
        approach_defaults = {
            "close_approach_date": approach_data["close_approach_date"],
            "relative_velocity_kps": approach_data.get(
                "relative_velocity_kps"
            ),
            "miss_distance_km": approach_data.get("miss_distance_km"),
        }

        _, approach_created = CloseApproach.objects.update_or_create(
            near_earth_object=neo,
            epoch_date_close_approach=approach_data[
                "epoch_date_close_approach"
            ],
            orbiting_body=approach_data["orbiting_body"],
            defaults=approach_defaults,
        )

        if approach_created:
            result.approaches_created += 1
        else:
            result.approaches_updated += 1

    return result

def upsert_normalized_feed(normalized_objects, synced_at=None):
    result = UpsertResult()

    for normalized_object in normalized_objects:
        object_result = upsert_normalized_object(
            normalized_object,
            synced_at=synced_at,
        )
        result.objects_created += object_result.objects_created
        result.objects_updated += object_result.objects_updated
        result.approaches_created += object_result.approaches_created
        result.approaches_updated += object_result.approaches_updated

    return result