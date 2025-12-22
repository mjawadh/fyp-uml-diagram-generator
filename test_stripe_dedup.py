"""Test Stripe deduplication with various input formats"""

from scripts.normalize_components import normalize_component_name

test_cases = [
    'Stripe',
    'stripe', 
    'Stripe Payment',
    'Stripe Payment Gateway',
    'External Stripe',
    'External Stripe Payment Gateway',
    'stripe gateway',
    'The Stripe Payment Gateway',
    'A Stripe',
    'external stripe payment',
]

print('=' * 70)
print('STRIPE DEDUPLICATION TEST')
print('=' * 70)
print()
print(f'{"Input":<40} -> {"Output":<25}')
print('-' * 70)

for test in test_cases:
    result = normalize_component_name(test)
    print(f'{test:<40} -> {result:<25}')

print()
print('=' * 70)
print('EXPECTED: All should normalize to "Stripe Gateway"')
print('=' * 70)
