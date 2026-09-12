REQUIRED_FIELDS = (
    "plain_english_summary",
    "technical_summary",
    "risk_context",
)


class BriefingResponseError(ValueError):
    pass


def _require_mapping(value):
    if not isinstance(value, dict):
        raise BriefingResponseError("Briefing response must be a JSON object.")

    return value


def _require_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise BriefingResponseError(f"{field_name} must be non-empty text.")

    return value.strip()


def normalize_briefing_response(response):
    response = _require_mapping(response)

    required_fields = set(REQUIRED_FIELDS)
    received_fields = set(response)

    missing_fields = required_fields - received_fields
    unexpected_fields = received_fields - required_fields

    if missing_fields:
        names = ", ".join(sorted(missing_fields))
        raise BriefingResponseError(
            f"Briefing response is missing required fields: {names}"
        )

    if unexpected_fields:
        names = ", ".join(sorted(unexpected_fields))
        raise BriefingResponseError(
            f"Briefing response contains unexpected fields: {names}"
        )

    return {
        field_name: _require_text(
            response[field_name],
            field_name,
        )
        for field_name in REQUIRED_FIELDS
    }
