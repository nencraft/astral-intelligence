from ..models import AstralScore
from .scoring_client import request_score
from .scoring_payload import build_score_payload
from .scoring_response import normalize_score_response

def score_close_approach(close_approach, client=None):
    payload = build_score_payload(close_approach)
    
    raw_response = request_score(
        payload,
        client=client
    )
    
    score_data = normalize_score_response(raw_response)
    
    score_defaults = score_data.copy()
    model_version = score_defaults.pop("model_version")
    
    return AstralScore.objects.update_or_create(
        close_approach=close_approach,
        model_version=model_version,
        defaults=score_defaults,
    )
    
    
    
    