"""Debug generic component detection."""
import spacy
from uml_extractors import ComponentDiagramExtractor

# Load models
nlp_standard = spacy.load("en_core_web_lg")
try:
    nlp_architecture = spacy.load("./architecture_uml_model/model-best")
except:
    nlp_architecture = None

test_narration = """The ecommerce frontend communicates with the payment service API. The payment service API accesses a PostgreSQL database and uses Redis cache. The backend services run in Docker containers on Linux servers. The system integrates with an external Stripe payment gateway. Users access the system via web browsers and mobile devices. The payment API exposes REST endpoints."""

extractor = ComponentDiagramExtractor(nlp_standard, nlp_architecture)

# Let's manually call the extraction without building elements
# and see what's in self.components
doc = extractor._process_text(test_narration)

# Mock the extraction to see what gets added
print("="*60)
print("COMPONENTS FOUND (before deduplication):")
print("="*60)

extractor._extract_components_pattern(test_narration)
for name, data in extractor.components.items():
    print(f"  {name:35s} {data.get('stereotype', '')}")

print(f"\nTotal: {len(extractor.components)} components")

print("\n" + "="*60)
print("GENERIC PATTERN ANALYSIS:")
print("="*60)

generic_component_patterns = {
    'api service': ['payment', 'order', 'user', 'auth', 'product', 'inventory', 'shipping'],
    'backend service': ['payment', 'order', 'user', 'auth', 'product', 'inventory', 'shipping'],
}

for comp_name in list(extractor.components.keys()):
    comp_lower = comp_name.lower()
    print(f"\nChecking: '{comp_name}'")
    
    for generic_pattern, specific_keywords in generic_component_patterns.items():
        if comp_lower == generic_pattern or comp_lower.strip() == generic_pattern.strip():
            print(f"  → Matches generic pattern '{generic_pattern}'")
            
            # Check if we have a more specific component
            for other_name in list(extractor.components.keys()) + list(extractor.external_systems):
                other_lower = other_name.lower()
                if other_lower != comp_lower:
                    for keyword in specific_keywords:
                        if keyword in other_lower:
                            check1 = generic_pattern.split()[0] in other_lower
                            check2 = 'service' in other_lower
                            check3 = 'gateway' in other_lower
                            if check1 or check2 or check3:
                                print(f"    → Found specific '{other_name}' with keyword '{keyword}'")
                                print(f"       Should skip '{comp_name}'")
                                break
