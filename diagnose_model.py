"""Diagnose why architecture diagrams are not working well."""
import spacy
import os

print("=" * 80)
print("MODEL DIAGNOSIS")
print("=" * 80)

# Check what models exist
arch_path = './architecture_uml_model/model-best'
behav_path = './behavioral_uml_model/model-best'
my_uml_path = './my_uml_model/model-best'

print(f"\n[1] MODEL EXISTENCE:")
print(f"    architecture_uml_model exists: {os.path.exists(arch_path)}")
print(f"    behavioral_uml_model exists:   {os.path.exists(behav_path)}")
print(f"    my_uml_model exists:           {os.path.exists(my_uml_path)}")

# Test input
test_text = """The user interface service sends requests to an inventory service. 
The inventory service stores data in a MySQL database and uses a Redis cache. 
The inventory service is deployed inside Docker containers running on a Linux server. 
The system integrates with an external Amazon S3 storage service. 
Users access the system through desktop browsers."""

print(f"\n[2] TEST INPUT:")
print(f"    {test_text[:100]}...")

# Load and test architecture model
if os.path.exists(arch_path):
    print(f"\n[3] ARCHITECTURE MODEL:")
    nlp_arch = spacy.load(arch_path)
    print(f"    Labels: {nlp_arch.get_pipe('ner').labels}")
    
    doc = nlp_arch(test_text)
    print(f"\n    Entities extracted by architecture model:")
    if doc.ents:
        for ent in doc.ents:
            print(f"      - '{ent.text}' -> {ent.label_}")
    else:
        print("      [NONE - MODEL EXTRACTED NOTHING!]")
else:
    print("\n[3] ARCHITECTURE MODEL: NOT FOUND")

# Load and test behavioral model for comparison
if os.path.exists(behav_path):
    print(f"\n[4] BEHAVIORAL MODEL (for comparison):")
    nlp_behav = spacy.load(behav_path)
    print(f"    Labels: {nlp_behav.get_pipe('ner').labels}")
    
    doc = nlp_behav(test_text)
    print(f"\n    Entities extracted by behavioral model:")
    if doc.ents:
        for ent in doc.ents:
            print(f"      - '{ent.text}' -> {ent.label_}")
    else:
        print("      [NONE]")
else:
    print("\n[4] BEHAVIORAL MODEL: NOT FOUND")

# Check what my_uml_model does
if os.path.exists(my_uml_path):
    print(f"\n[5] MY_UML_MODEL (currently used in extractors):")
    nlp_uml = spacy.load(my_uml_path)
    print(f"    Labels: {nlp_uml.get_pipe('ner').labels}")
    
    doc = nlp_uml(test_text)
    print(f"\n    Entities extracted by my_uml_model:")
    if doc.ents:
        for ent in doc.ents:
            print(f"      - '{ent.text}' -> {ent.label_}")
    else:
        print("      [NONE - MODEL EXTRACTED NOTHING!]")
else:
    print("\n[5] MY_UML_MODEL: NOT FOUND")

# Now check what the EXTRACTORS actually use
print("\n" + "=" * 80)
print("EXTRACTOR MODEL USAGE")
print("=" * 80)

# Check what test_component_full.py loads
print("\n[6] Checking what models test_component_full.py loads...")
with open('test_component_full.py', 'r') as f:
    content = f.read()
    if 'architecture_uml_model' in content:
        print("    -> Uses architecture_uml_model")
    if 'behavioral_uml_model' in content:
        print("    -> Uses behavioral_uml_model")
    if 'my_uml_model' in content:
        print("    -> Uses my_uml_model")
    if 'en_core_web' in content:
        print("    -> Uses en_core_web_* (spacy standard)")

# Check ComponentDiagramExtractor
print("\n[7] Checking ComponentDiagramExtractor initialization...")
with open('uml_extractors.py', 'r') as f:
    content = f.read()
    # Find the __init__ of ComponentDiagramExtractor
    import re
    match = re.search(r'class ComponentDiagramExtractor.*?def __init__\(self,([^)]+)\)', content, re.DOTALL)
    if match:
        print(f"    Constructor params: {match.group(1).strip()}")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
