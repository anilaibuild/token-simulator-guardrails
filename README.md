# Token Simulator + Guardrail

A working pipeline that tracks real Claude vs. Gemini token costs, and extends that with a Google Model Armor guardrail layer that blocks risky prompts (PII, jailbreak attempts) before they ever reach an external AI provider.

Full writeup: *[What Almost Leaked: Building a Guardrail for Shadow AI](#)* ← add your published post link here

## What this does

1. **Token/cost tracking** (`gemini_test.py`, `database.py`) — sends the same questions to both Claude and Gemini, logs real token usage and cost to SQLite, and charts the results (`visualize.py`).
2. **Guardrail layer** (`guardrail.py`) — checks every prompt against Google Model Armor before it's allowed to reach Claude or Gemini. Blocks PII (via a custom Cloud DLP inspection template for phone numbers and emails) and prompt injection / jailbreak attempts.
3. **Live interactive demo** (`live_demo.py`) — type any prompt and see the guardrail's real, live verdict.

## Real findings

- Claude's reasoning tokens are almost entirely invisible in billing — 94% never show up as visible output.
- Claude costs roughly 20x more than Gemini for equivalent tasks.
- Model Armor's default ("Basic") sensitive-data detection misses phone numbers and emails entirely — catches only high-severity IDs like SSNs by default. Fixed by configuring Advanced detection with a custom DLP inspection template.
- The guardrail correctly distinguishes between a question *about* PII (allowed) and a prompt *containing* real PII (blocked) — it's not a blunt keyword filter.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```
GEMINI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

```


You'll also need:
- A GCP project with the Model Armor API enabled
- A Model Armor template configured (see the full writeup for exact steps)
- `gcloud auth application-default login` run locally for authentication

## Usage

Run the full cost + guardrail pipeline:
```bash
python gemini_test.py
```

Try the interactive guardrail demo:
```bash
python live_demo.py
```

Generate the charts:
```bash
python visualize.py
python guardrail_chart.py
```

## Notes on scope

This is a personal proof-of-concept, not production infrastructure. A few things worth knowing:
- "Logs" means the local SQLite database, not GCP Cloud Logging.
- Latency was not profiled — no round-trip timing claims are made.
- Fail-closed behavior on a Model Armor API error is a side effect of unhandled exceptions in this version, not deliberate error-handling design.

## License

MIT