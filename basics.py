employee = {
    "name": "Anil",
    "tokens_used": 7000000,
    "model": "gpt-4"
}

print(employee)
print(employee["name"])
print(employee["tokens_used"])

employees = [
    {"name": "Anil", "tokens_used": 7000000, "model": "gpt-4"},
    {"name": "Priya", "tokens_used": 150000, "model": "gpt-4"},
    {"name": "Raj", "tokens_used": 300000, "model": "gpt-3.5"},
    {"name": "Meera", "tokens_used": 5000, "model": "gpt-3.5"},
    {"name": "Kabir", "tokens_used": 8000, "model": "gpt-3.5"},
    {"name": "Sana", "tokens_used": 3000, "model": "gpt-3.5"},
    {"name": "Vikram", "tokens_used": 450000, "model": "gpt-4"},
    {"name": "Fatima", "tokens_used": 220000, "model": "gpt-4"},
    {"name": "Arjun", "tokens_used": 500000, "model": "gpt-4"},
    {"name": "Neha", "tokens_used": 180000, "model": "gpt-3.5"}
]

for employee in employees:
    print(employee["name"], "-", employee["tokens_used"], "tokens")

cost_per_million_tokens = 30  # example rate in dollars

for employee in employees:
    tokens_in_millions = employee["tokens_used"] / 1_000_000
    cost = tokens_in_millions * cost_per_million_tokens
    print(employee["name"], "cost: $" + str(round(cost, 2)))    

total_cost = 0

for employee in employees:
    tokens_in_millions = employee["tokens_used"] / 1_000_000
    cost = tokens_in_millions * cost_per_million_tokens
    total_cost = total_cost + cost

print("Total org cost: $" + str(round(total_cost, 2)))

anil_cost = (employees[0]["tokens_used"] / 1_000_000) * cost_per_million_tokens
percentage = (anil_cost / total_cost) * 100

print("Anil's share of total cost: " + str(round(percentage, 1)) + "%")