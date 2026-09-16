"""
live_demo.py

Interactive demo: type any prompt and see Model Armor's real,
live verdict immediately. Built for live demos / interviews / a
screen-recorded GIF for the blog post.

Run:  python live_demo.py
Exit: type 'quit' or press Ctrl+C
"""

from guardrail import check_prompt

BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

BANNER = f"""
{BOLD}Guardrail Live Check{RESET}
Model Armor \u00b7 template: guardrail-basic-template \u00b7 region: us-central1

Type any prompt and see whether it would be blocked before
reaching Claude or Gemini. Type 'quit' to exit.
"""

def main():
    print(BANNER)
    while True:
        try:
            prompt = input(f"{BOLD}Prompt> {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not prompt:
            continue
        if prompt.lower() in ("quit", "exit"):
            print("Exiting.")
            break

        result = check_prompt(prompt)

        if result["blocked"]:
            print(f"\033[91m\033[1m\u2717 BLOCKED\033[0m  reason: {result['reason']}\n")
        else:
            print(f"\033[92m\033[1m\u2713 ALLOWED\033[0m  would be sent to Claude/Gemini\n")


if __name__ == "__main__":
    main()