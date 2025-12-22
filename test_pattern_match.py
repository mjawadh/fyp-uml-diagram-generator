import re

patterns = ['web browser', 'browser', 'mobile', 'mobile device', 'postgresql', 'mysql', 'mongodb', 'database']
test = 'PostgreSQL'

print(f"Testing: '{test}'")
print("-" * 40)

for p in patterns:
    match = re.search(p, test, re.IGNORECASE)
    result = "MATCH" if match else "no match"
    print(f'{p:20} -> {result}')
