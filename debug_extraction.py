"""Debug what the NER model actually extracts vs what the extractors use."""
import spacy
from uml_extractors import ComponentDiagramExtractor, DeploymentDiagramExtractor

# Test input
test_text = """The user interface service sends requests to an inventory service. 
The inventory service stores data in a MySQL database and uses a Redis cache. 
The inventory service is deployed inside Docker containers running on a Linux server. 
The system integrates with an external Amazon S3 storage service. 
Users access the system through desktop browsers."""

print("=" * 80)
print("STEP 1: LOAD MODELS")
print("=" * 80)

nlp_standard = spacy.load("en_core_web_lg")
nlp_architecture = spacy.load("./architecture_uml_model/model-best")
print(f"Standard model: {nlp_standard.meta['name']}")
print(f"Architecture model labels: {nlp_architecture.get_pipe('ner').labels}")

print("\n" + "=" * 80)
print("STEP 2: RAW NER EXTRACTION (architecture model directly)")
print("=" * 80)

doc_ner = nlp_architecture(test_text)
print(f"\nEntities extracted by architecture_uml_model:")
for ent in doc_ner.ents:
    print(f"  - '{ent.text}' -> {ent.label_}")

print("\n" + "=" * 80)
print("STEP 3: COMPONENT EXTRACTOR OUTPUT")
print("=" * 80)

extractor = ComponentDiagramExtractor(nlp_standard, nlp_architecture)

# Add debug to see what's happening inside
print("\nCalling extract()...")
elements = extractor.extract(test_text)

print(f"\nComponents in extractor.components dict:")
for name, data in extractor.components.items():
    print(f"  - {name}: {data}")

print(f"\nExternal systems in extractor.external_systems:")
for sys in extractor.external_systems:
    print(f"  - {sys}")

print(f"\nRelationships in extractor.relationships:")
for rel in extractor.relationships:
    print(f"  - {rel}")

print(f"\n\nFINAL MODEL ELEMENTS ({len(elements)}):")
for i, elem in enumerate(elements, 1):
    print(f"  {i}. {elem}")

print("\n" + "=" * 80)
print("STEP 4: WHAT ENTITIES WERE MISSING FROM FINAL OUTPUT?")
print("=" * 80)

# What NER found
ner_components = []
ner_external = []
for ent in doc_ner.ents:
    if ent.label_ == 'COMPONENT':
        ner_components.append(ent.text)
    elif ent.label_ == 'EXTERNAL_SYSTEM':
        ner_external.append(ent.text)

print(f"\nNER found COMPONENT: {ner_components}")
print(f"NER found EXTERNAL_SYSTEM: {ner_external}")

# What extractor has
extractor_components = list(extractor.components.keys())
extractor_external = list(extractor.external_systems)

print(f"\nExtractor components: {extractor_components}")
print(f"Extractor external: {extractor_external}")

# Missing
missing_components = [c for c in ner_components if c not in ' '.join(extractor_components).lower()]
missing_external = [e for e in ner_external if e not in ' '.join(extractor_external)]

print(f"\n❌ MISSING COMPONENTS: {missing_components}")
print(f"❌ MISSING EXTERNAL: {missing_external}")
