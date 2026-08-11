import sqlite3
from datetime import datetime
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def ask_gemini(question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "contents": [
            {"parts": [{"text": question}]}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "candidates" not in data:
        print("Error response:", data)
        return None, 0, 0, 0, 0, 0

    answer_text = data["candidates"][0]["content"]["parts"][0]["text"]
    usage = data["usageMetadata"]
    total_tokens = usage["totalTokenCount"]
    prompt_tokens = usage.get("promptTokenCount", 0)
    visible_tokens = usage.get("candidatesTokenCount", 0)
    thinking_tokens = usage.get("thoughtsTokenCount", 0)

    cost_per_million_tokens = 0.15
    cost = (total_tokens / 1_000_000) * cost_per_million_tokens

    return answer_text, total_tokens, cost, prompt_tokens, visible_tokens, thinking_tokens


anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

def ask_claude(question):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": anthropic_api_key,
        "anthropic-version": "2023-06-01"
    }
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 200,
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "content" not in data:
        print("Error response:", data)
        return None, 0, 0

    answer_text = data["content"][0]["text"]
    input_tokens = data["usage"]["input_tokens"]
    output_tokens = data["usage"]["output_tokens"]
    total_tokens = input_tokens + output_tokens

    cost_per_million_input = 3.00
    cost_per_million_output = 15.00
    cost = (input_tokens / 1_000_000) * cost_per_million_input + (output_tokens / 1_000_000) * cost_per_million_output

    return answer_text, total_tokens, cost


def save_to_database(employee_name, question, provider, tokens_used, cost, prompt_tokens=None, visible_tokens=None, thinking_tokens=None):
    connection = sqlite3.connect("token_tracker.db")
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO usage_log (employee_name, question, provider, tokens_used, cost, timestamp, prompt_tokens, visible_tokens, thinking_tokens)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (employee_name, question, provider, tokens_used, cost, timestamp, prompt_tokens, visible_tokens, thinking_tokens))

    connection.commit()
    connection.close()


employees = [
    {"name": "Anil", "question": "Explain how a car engine works in 2 sentences."},
    {"name": "Priya", "question": "What is the capital of Japan?"},
    {"name": "Raj", "question": "Give me a fun fact about octopuses."},
    {"name": "Meera", "question": "What is 12 times 8?"},
    {"name": "Kabir", "question": "What is the capital of Italy?"},
    {"name": "Sana", "question": "Name one planet in our solar system."},
    {"name": "Vikram", "question": "Summarize photosynthesis in 2 sentences."},
    {"name": "Fatima", "question": "What year did World War 2 end?"},
    {"name": "Arjun", "question": "Explain gravity in one sentence."},
    {"name": "Neha", "question": "What is the boiling point of water in Celsius?"}
]

# ---- Gemini run (use this tomorrow once quota resets) ----
# total_org_cost = 0
# for employee in employees:
#     answer, tokens, cost, prompt_tokens, visible_tokens, thinking_tokens = ask_gemini(employee["question"])
#     total_org_cost = total_org_cost + cost
#     print(employee["name"], "| tokens:", tokens, "| cost: $" + str(round(cost, 6)))
#     save_to_database(employee["name"], employee["question"], "Gemini", tokens, cost, prompt_tokens, visible_tokens, thinking_tokens)
#     time.sleep(13)
# print("\nTotal org cost for this batch: $" + str(round(total_org_cost, 6)))

# ---- Claude run (working now) ----
total_org_cost = 0
for employee in employees:
    answer, tokens, cost = ask_claude(employee["question"])
    total_org_cost = total_org_cost + cost
    print(employee["name"], "| tokens:", tokens, "| cost: $" + str(round(cost, 6)))
    save_to_database(employee["name"], employee["question"], "Claude", tokens, cost)

print("\nTotal org cost for this batch: $" + str(round(total_org_cost, 6)))