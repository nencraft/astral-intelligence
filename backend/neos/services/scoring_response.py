FACTOR_FIELDS = (
    ("diameter", "diameter_factor", 25),
    ("distance", "distance_factor", 25),
    ("velocity", "velocity_factor", 20),
    ("timing", "timing_factor", 15),
    ("hazardFlag", "hazard_flag_factor", 15),
)


class ScoringResponseError(ValueError):
    pass


def _require_mapping(value, field_name):
    if not isinstance(value, dict):
        raise ScoringResponseError(
            f"{field_name} must be a JSON object"
        )

    return value


def _require_key(mapping, key):
    if key not in mapping:
        raise ScoringResponseError(
            f"Scoring response is missing required field: {key}"
        )

    return mapping[key]


def _require_integer(value, field_name, maximum):
    if type(value) is not int:
        raise ScoringResponseError(
            f"{field_name} must be an integer"
        )

    if value < 0 or value > maximum:
        raise ScoringResponseError(
            f"{field_name} must be between 0 and {maximum}"
        )

    return value


def _require_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ScoringResponseError(
            f"{field_name} must be nonempty text"
        )

    return value


def _category_for_score(score):
    if score < 25:
        return "Low Interest"

    if score < 50:
        return "Moderate Interest"

    if score < 75:
        return "High Interest"

    return "Critical Review"


def normalize_score_response(response):
    response = _require_mapping(response, "response")

    score = _require_integer(
        _require_key(response, "score"),
        "score",
        100,
    )
    category = _require_text(
        _require_key(response, "category"),
        "category",
    )
    model_version = _require_text(
        _require_key(response, "modelVersion"),
        "modelVersion",
    )
    explanation = _require_text(
        _require_key(response, "explanation"),
        "explanation",
    )
    factors = _require_mapping(
        _require_key(response, "factors"),
        "factors",
    )

    normalized_factors = {}

    for external_name, internal_name, maximum in FACTOR_FIELDS:
        normalized_factors[internal_name] = _require_integer(
            _require_key(factors, external_name),
            external_name,
            maximum,
        )

    factor_total = sum(normalized_factors.values())

    if score != factor_total:
        raise ScoringResponseError(
            "score must equal the factor total"
        )

    expected_category = _category_for_score(score)

    if category != expected_category:
        raise ScoringResponseError(
            f"category must be {expected_category} for score {score}"
        )

    return {
        "score": score,
        "category": category,
        "model_version": model_version,
        **normalized_factors,
        "explanation": explanation,
    }