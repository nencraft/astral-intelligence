import json

PROMPT_VERSION = "briefing-v1"


def build_briefing_prompt(snapshot, caveats):
    snapshot_json = json.dumps(snapshot, indent=2, sort_keys=True)
    caveats_json = json.dumps(caveats, indent=2)

    return f"""
    ROLE
    
    You are writing a factual technical briefing about a near-Earth object's
    close approach.

    RULES
    
    Use only the supplied source data and required caveats.
    Do not invent measurements, probabilities, classifications, or other facts.
    Do not claim that an Earth impact will occur.
    Do not describe the Astral score as a collision or impact probability.
    Clearly distinguish NASA's potentially hazardous designation from an
    impact prediction.
    Preserve the supplied measurements and units.
    Write clearly and avoid sensational language.
    
    REQUIRED OUTPUT
    
    Return valid JSON using exactly this structure:
    {{
        "plain_english_summary": "A concise explanation for a general audience.",
        "technical_summary": "A technical summary using the supplied measurements and units.",
        "risk_context": "A careful explanation of what the hazard designation and Astral score do and do not mean."
    }}

    Return only the JSON object.
    Do not include Markdown code fences.
    Do not add any other fields.
    Every field must contain a non-empty string.
    
    SOURCE DATA
    {snapshot_json}
    
    REQUIRED CAVEATS
    {caveats_json}
    """.strip()
