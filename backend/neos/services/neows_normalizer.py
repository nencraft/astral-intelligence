from datetime import date
from decimal import Decimal

class NeoWsNormalizationError(ValueError):
      pass

def require_field(data, field_name):
    try:
        return data[field_name]
    except KeyError as exc:
        raise NeoWsNormalizationError(
            f"Missing required NeoWs field: {field_name}"
        ) from exc

def to_optional_decimal(value):
    if value is None:
        return None

    return Decimal(str(value))


def normalize_close_approach(raw_approach):
    return {
        "close_approach_date": date.fromisoformat(
            require_field(raw_approach, "close_approach_date")
        ),
        "epoch_date_close_approach": int(
            require_field(raw_approach, "epoch_date_close_approach")
        ),
        "relative_velocity_kps": to_optional_decimal(
            raw_approach.get("relative_velocity", {}).get(
                "kilometers_per_second"
            )
        ),
        "miss_distance_km": to_optional_decimal(
            raw_approach.get("miss_distance", {}).get("kilometers")
        ),
        "orbiting_body": require_field(raw_approach, "orbiting_body"),
    }


def normalize_neo(raw_neo):
    diameter_km = raw_neo.get("estimated_diameter", {}).get(
        "kilometers",
        {},
    )

    return {
        "neo": {
            "nasa_jpl_id": require_field(raw_neo, "id"),
            "name": require_field(raw_neo, "name"),
            "absolute_magnitude_h": to_optional_decimal(
                raw_neo.get("absolute_magnitude_h")
            ),
            "estimated_diameter_min_km": to_optional_decimal(
                diameter_km.get("estimated_diameter_min")
            ),
            "estimated_diameter_max_km": to_optional_decimal(
                diameter_km.get("estimated_diameter_max")
            ),
            "is_potentially_hazardous": require_field(
                raw_neo,
                "is_potentially_hazardous_asteroid",
            ),
        },
        "close_approaches": [
            normalize_close_approach(raw_approach)
            for raw_approach in raw_neo.get("close_approach_data", [])
        ],
    }


def normalize_feed(payload):
    normalized_objects = []

    for objects_for_date in payload.get("near_earth_objects", {}).values():
        for raw_neo in objects_for_date:
            normalized_objects.append(normalize_neo(raw_neo))

    return normalized_objects