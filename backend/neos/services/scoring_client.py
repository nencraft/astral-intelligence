import httpx

from django.conf import settings


class ScoringClientError(RuntimeError):
    pass


def _send_score_request(payload, client):
    endpoint = f"{settings.SCORING_SERVICE_URL}/api/score"

    try:
        response = client.post(
            endpoint,
            json=payload,
        )
    except httpx.RequestError as exc:
        raise ScoringClientError("Scoring service request failed") from exc

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ScoringClientError(
            f"Scoring service request failed with status " f"{exc.response.status_code}"
        ) from exc

    try:
        return response.json()
    except ValueError as exc:
        raise ScoringClientError("Scoring service returned invalid JSON") from exc


def request_score(payload, client=None):
    if client is not None:
        return _send_score_request(payload, client)

    with httpx.Client(
        timeout=settings.SCORING_SERVICE_TIMEOUT_SECONDS,
    ) as default_client:
        return _send_score_request(payload, default_client)
