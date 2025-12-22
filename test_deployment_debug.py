"""Debug script to test deployment diagram extraction."""
import sys
import logging

# Setup logging to see debug messages
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Load models
print("Loading models...")
import spacy
from uml_extractors import DeploymentDiagramExtractor

nlp = spacy.load("en_core_web_lg")

try:
    ner_model = spacy.load("./architecture_uml_model/model-best")
    print("✓ Loaded custom NER model")
except:
    ner_model = None
    print("⚠ Using base model only")

# Test narration
narration = """The client-facing web application sends requests to an order management service. The order management service reads and writes data to a MongoDB database and leverages a Redis cache for session storage. The service is deployed inside Docker containers hosted on Ubuntu servers. The system communicates with an external PayPal payment service. Customers interact with the system using desktop browsers and mobile applications. The order service provides RESTful APIs for client communication."""

print("\n" + "="*80)
print("TESTING DEPLOYMENT EXTRACTION")
print("="*80)

extractor = DeploymentDiagramExtractor(nlp, ner_model)
elements = extractor.extract(narration)

print(f"\n✓ Extracted {len(elements)} elements")

# Group by type
nodes = [e for e in elements if e['type'] == 'Node']
devices = [e for e in elements if e['type'] == 'Device']
relationships = [e for e in elements if e['type'] == 'DeploymentRelationship']

print(f"\nNodes ({len(nodes)}):")
for node in nodes:
    children = node['data'].get('children', [])
    if children:
        print(f"  • {node['data']['name']} {node['data']['stereotype']} - CONTAINS: {children}")
    else:
        print(f"  • {node['data']['name']} {node['data']['stereotype']}")

print(f"\nDevices ({len(devices)}):")
for device in devices:
    print(f"  • {device['data']['name']}")

print(f"\nRelationships ({len(relationships)}):")
for rel in relationships:
    print(f"  • {rel['data']['source']} --> {rel['data']['target']} : {rel['data']['type']}")

print("\n" + "="*80)
