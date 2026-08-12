
class ScoringPayloadError(ValueError):
    pass

def _require_value(value, field_name):
    if value is None:
        raise ScoringPayloadError(f"{field_name} is required for scoring.")
    return value

def build_score_payload(close_approach):
    neo = close_approach.near_earth_object
    
    return {
        "estimatedDiameterMinKm": float(
            _require_value(
                neo.estimated_diameter_min_km, 
                "estimated_diameter_min_km",
            )
        ),
        "estimatedDiameterMaxKm": float(
            _require_value(
                neo.estimated_diameter_max_km,
                "estimated_diameter_max_km",
            )
        ),
        "missDistanceKm": float(
            _require_value(
                close_approach.miss_distance_km,
                "miss_distance_km",
            )
        ),
        "relativeVelocityKps": float(
            _require_value(
                close_approach.relative_velocity_kps,
                "relative_velocity_kps",
            )
        ),
        "isPotentiallyHazardous": neo.is_potentially_hazardous,
        "closeApproachDate": close_approach.close_approach_date.isoformat(),
    }