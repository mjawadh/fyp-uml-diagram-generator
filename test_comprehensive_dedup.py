"""Comprehensive deduplication test for deployment diagram entities"""

from scripts.normalize_components import (
    normalize_component_name,
    normalize_node_name, 
    normalize_device_name
)

print('=' * 80)
print('COMPREHENSIVE DEDUPLICATION TEST')
print('=' * 80)

# Test 1: PostgreSQL variations
print('\n1. POSTGRESQL DEDUPLICATION (as Component)')
print('-' * 80)
postgres_components = [
    'PostgreSQL',
    'Postgresql', 
    'postgres',
    'PostgreSQL Database',
    'Postgresql Database',
    'Postgres Database',
    'A PostgreSQL Database',
    'The PostgreSQL DB',
    'postgres db',
]
for test in postgres_components:
    result = normalize_component_name(test)
    print(f'  Component: {test:<35} -> {result}')

print('\n   POSTGRESQL DEDUPLICATION (as Node)')
print('-' * 80)
postgres_nodes = [
    'PostgreSQL',
    'Postgresql Database',
    'Postgres',
    'A Postgresql Database',
    'The Postgres Server',
]
for test in postgres_nodes:
    result = normalize_node_name(test)
    print(f'  Node:      {test:<35} -> {result}')

# Test 2: Docker variations
print('\n\n2. DOCKER CONTAINER DEDUPLICATION')
print('-' * 80)
docker_variations = [
    'Docker Container',
    'Docker Containers',
    'In Docker Container',
    'In Docker Containers', 
    'On Docker Container',
    'docker containers',
    'A Docker Container',
]
for test in docker_variations:
    result = normalize_node_name(test)
    print(f'  {test:<35} -> {result}')

# Test 3: Web Browser variations
print('\n\n3. WEB BROWSER DEDUPLICATION')
print('-' * 80)
browser_variations = [
    'Web Browser',
    'Web Browsers',
    'Via Web Browser',
    'Through Web Browser',
    'web browser',
    'Browser',
    'Browsers',
    'A Web Browser',
    'The Web Browser',
]
for test in browser_variations:
    result = normalize_device_name(test)
    print(f'  {test:<35} -> {result}')

# Test 4: Mobile Device variations
print('\n\n4. MOBILE DEVICE DEDUPLICATION')
print('-' * 80)
mobile_variations = [
    'Mobile Device',
    'Mobile Devices',
    'And Mobile Device',
    'And Mobile Devices',
    'Via Mobile Device',
    'mobile devices',
    'A Mobile Device',
    'The Mobile Device',
]
for test in mobile_variations:
    result = normalize_device_name(test)
    print(f'  {test:<35} -> {result}')

# Test 5: Linux Server variations
print('\n\n5. LINUX SERVER DEDUPLICATION')
print('-' * 80)
linux_variations = [
    'Linux Server',
    'Linux Servers',
    'linux server',
    'A Linux Server',
    'The Linux Server',
]
for test in linux_variations:
    result = normalize_node_name(test)
    print(f'  {test:<35} -> {result}')

# Test 6: Stripe variations
print('\n\n6. STRIPE DEDUPLICATION')
print('-' * 80)
stripe_variations = [
    'Stripe',
    'Stripe Payment',
    'Stripe Payment Gateway',
    'External Stripe',
    'External Stripe Payment Gateway',
    'stripe gateway',
]
for test in stripe_variations:
    result = normalize_component_name(test)
    print(f'  {test:<35} -> {result}')

print('\n' + '=' * 80)
print('SUMMARY: All variations within each category should normalize to ONE name')
print('=' * 80)
