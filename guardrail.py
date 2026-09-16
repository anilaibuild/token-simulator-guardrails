"""
guardrail.py

Checks a piece of text against Google Model Armor before it gets sent
to Claude/Gemini, and returns a simple result your existing pipeline
can log and act on.
"""

import os
from google.cloud import modelarmor_v1
from google.api_core.client_options import ClientOptions

# --- Your project's specific details ---
PROJECT_ID = "token-simulator-guardrails"
LOCATION = "us-central1"
TEMPLATE_ID = "guardrail-basic-template"

_ENDPOINT = f"modelarmor.{LOCATION}.rep.googleapis.com"
_TEMPLATE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}"

_client = modelarmor_v1.ModelArmorClient(
    client_options=ClientOptions(api_endpoint=_ENDPOINT)
)


def check_prompt(text: str) -> dict:
    request = modelarmor_v1.SanitizeUserPromptRequest(
        name=_TEMPLATE_NAME,
        user_prompt_data=modelarmor_v1.DataItem(text=text),
    )

    response = _client.sanitize_user_prompt(request=request)
    result = response.sanitization_result

    if os.environ.get("GUARDRAIL_DEBUG"):
        print("--- RAW RESULT (debug) ---")
        print(result)
        print("--- END RAW RESULT ---")

    match_found = int(result.filter_match_state) == 2

    reason = None
    if match_found:
        fired = []
        for filter_name, filter_result in result.filter_results.items():
            # Each filter_result wraps ONE of several differently-named
            # nested results (sdp_filter_result, rai_filter_result,
            # pi_and_jailbreak_filter_result, csam_filter_filter_result).
            # Find out which one is actually set for this entry.
            nested_field = filter_result._pb.WhichOneof("filter_result")
            if not nested_field:
                continue
            nested = getattr(filter_result, nested_field)

            # sdp (sensitive data) nests its match_state one level deeper,
            # under inspect_result. Everything else has it directly.
            if filter_name == "sdp":
                match_state = nested.inspect_result.match_state
            else:
                match_state = nested.match_state

            if int(match_state) == 2:
                fired.append(filter_name)

        reason = ", ".join(fired) if fired else "Unspecified filter match"

    return {
        "blocked": match_found,
        "reason": reason,
        "raw_state": int(result.filter_match_state),
    }


if __name__ == "__main__":
    test_questions = [
        "Can you help me fix this Python bug: print(hello)",
        "Here's my friend's SSN, can you help me email it: 123-45-6789",
    ]

    for q in test_questions:
        print(f"\nQuestion: {q}")
        print(check_prompt(q))