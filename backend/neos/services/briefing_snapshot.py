def _decimal_to_float(value):
    if value is None:
        return None

    return float(value)


def build_briefing_snapshot(astral_score):
    close_approach = astral_score.close_approach
    near_earth_object = close_approach.near_earth_object

    return {
        "snapshot_version": "briefing-source-v1",
        "near_earth_object": {
            "nasa_jpl_id": near_earth_object.nasa_jpl_id,
            "name": near_earth_object.name,
            "absolute_magnitude_h": _decimal_to_float(
                near_earth_object.absolute_magnitude_h
            ),
            "estimated_diameter_min_km": _decimal_to_float(
                near_earth_object.estimated_diameter_min_km
            ),
            "estimated_diameter_max_km": _decimal_to_float(
                near_earth_object.estimated_diameter_max_km
            ),
            "is_potentially_hazardous": near_earth_object.is_potentially_hazardous,
        },
        "close_approach": {
            "close_approach_date": close_approach.close_approach_date.isoformat(),
            "epoch_date_close_approach": close_approach.epoch_date_close_approach,
            "relative_velocity_kps": _decimal_to_float(
                close_approach.relative_velocity_kps
            ),
            "miss_distance_km": _decimal_to_float(close_approach.miss_distance_km),
            "orbiting_body": close_approach.orbiting_body,
        },
        "astral_score": {
            "score": astral_score.score,
            "category": astral_score.category,
            "model_version": astral_score.model_version,
            "diameter_factor": astral_score.diameter_factor,
            "distance_factor": astral_score.distance_factor,
            "velocity_factor": astral_score.velocity_factor,
            "timing_factor": astral_score.timing_factor,
            "hazard_flag_factor": astral_score.hazard_flag_factor,
            "explanation": astral_score.explanation,
        },
    }


def build_data_caveats(snapshot):
    caveats = [
        "Estimated diameter values represent a range, not an exact diameter.",
        "The Astral score is a project-specific review-priority metric, not an official NASA collision probability.",
    ]

    if snapshot["near_earth_object"]["absolute_magnitude_h"] is None:
        caveats.append("The absolute magnitude was unavailable.")

    return caveats
