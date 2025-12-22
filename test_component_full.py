"""Test complete component diagram flow with improvements."""
import json
import spacy
import os
from uml_extractors import ComponentDiagramExtractor
from uml_extractors import DeploymentDiagramExtractor
from uml_generator import DiagramGenerator

# Load models
print("Loading models...")
nlp_standard = spacy.load("en_core_web_lg")
try:
    nlp_architecture = spacy.load("./architecture_uml_model/model-best")
    print("[OK] Architecture NER model loaded")
except:
    nlp_architecture = None
    print("[WARNING] No architecture model, using pattern-based extraction only")

# Test input
test_narration = """The user interface service sends requests to an inventory service. The inventory service stores data in a MySQL database and uses a Redis cache. The inventory service is deployed inside Docker containers running on a Linux server. The system integrates with an external Amazon S3 storage service. Users access the system through desktop browsers."""

print("\n" + "="*80)
print("FULL COMPONENT & DEPLOYMENT DIAGRAM TEST")
print("="*80)
print(f"\nInput:\n{test_narration}\n")

# ============================================================================
# COMPONENT DIAGRAM TEST
# ============================================================================
print("\n" + "="*80)
print("COMPONENT DIAGRAM")
print("="*80)

# Step 1: Extract components
print("\n" + "-"*80)
print("STEP 1: COMPONENT EXTRACTION")
print("-"*80)

component_extractor = ComponentDiagramExtractor(nlp_standard, nlp_architecture)
component_elements = component_extractor.extract(test_narration)

print(f"\n[OK] Extracted {len(component_elements)} model elements\n")

print(f"Components ({len(component_extractor.components)}):")
for name, data in component_extractor.components.items():
    print(f"  • {name:35s} {data['stereotype'] or '(no stereotype)'}")

print(f"\nExternal Systems ({len(component_extractor.external_systems)}):")
for sys in component_extractor.external_systems:
    print(f"  • {sys}")

print(f"\nRelationships ({len(component_extractor.relationships)}):")
for rel in component_extractor.relationships:
    print(f"  • {rel['source']:30s} --[{rel['type']}]--> {rel['target']}")

print(f"\nModel Elements ({len(component_elements)}):")
for i, el in enumerate(component_elements, 1):
    if el['type'] == 'Component':
        print(f"  {i}. Component: {el['data']['name']:30s} {el['data'].get('stereotype', '')}")
    elif el['type'] == 'ComponentRelationship':
        print(f"  {i}. Relationship: {el['data']['source']} --> {el['data']['target']}")

# Step 2: Generate component diagram
print("\n" + "-"*80)
print("STEP 2: COMPONENT DIAGRAM GENERATION")
print("-"*80)

generator = DiagramGenerator()
test_project_id = "test-architecture-diagrams"

# Create directories if needed
os.makedirs("static", exist_ok=True)
os.makedirs("generated_puml", exist_ok=True)

generator.generate_component_diagram(test_project_id, component_elements, "static", "generated_puml")

# Step 3: Show generated component PUML
print("\n" + "-"*80)
print("STEP 3: COMPONENT PLANTUML CODE")
print("-"*80)

component_puml_file = f"generated_puml/component_{test_project_id}.puml"
if os.path.exists(component_puml_file):
    with open(component_puml_file, 'r') as f:
        puml_content = f.read()
    print(f"\nFile: {component_puml_file}\n")
    print(puml_content)
else:
    print(f"⚠️ PUML file not found: {component_puml_file}")

# Step 4: Check component output image
print("\n" + "-"*80)
print("STEP 4: COMPONENT OUTPUT IMAGE")
print("-"*80)

component_png_file = f"static/component_{test_project_id}.png"
if os.path.exists(component_png_file):
    file_size = os.path.getsize(component_png_file)
    print(f"\n✅ Component diagram generated: {component_png_file}")
    print(f"   File size: {file_size:,} bytes")
else:
    print(f"\n❌ PNG file not found: {component_png_file}")

# ============================================================================
# DEPLOYMENT DIAGRAM TEST
# ============================================================================
print("\n" + "="*80)
print("DEPLOYMENT DIAGRAM")
print("="*80)

# Step 1: Extract deployment architecture
print("\n" + "-"*80)
print("STEP 1: DEPLOYMENT EXTRACTION")
print("-"*80)

deployment_extractor = DeploymentDiagramExtractor(nlp_standard, nlp_architecture)

# Pass components from component diagram as artifacts for deployment
# This ensures consistency - services extracted for component diagram
# become deployable artifacts in deployment diagram
deployment_elements = deployment_extractor.extract(
    test_narration, 
    component_artifacts=component_extractor.components
)

print(f"\n✅ Extracted {len(deployment_elements)} model elements\n")

print(f"Nodes ({len(deployment_extractor.nodes)}):")
for name, data in deployment_extractor.nodes.items():
    print(f"  • {name:35s} {data.get('stereotype', '(no stereotype)')}")

print(f"\nDevices ({len(deployment_extractor.devices)}):")
for dev in deployment_extractor.devices:
    print(f"  • {dev}")

print(f"\nArtifacts ({len(deployment_extractor.artifacts)}):")
for name, data in deployment_extractor.artifacts.items():
    print(f"  • {name}")

print(f"\nDeployment Relationships ({len(deployment_extractor.deployment_relationships)}):")
for rel in deployment_extractor.deployment_relationships:
    print(f"  • {rel.get('source', 'N/A'):25s} --[{rel.get('type', 'connects')}]--> {rel.get('target', 'N/A')}")

print(f"\nModel Elements ({len(deployment_elements)}):")
for i, el in enumerate(deployment_elements, 1):
    if el['type'] == 'Node':
        children = el['data'].get('children', [])
        if children:
            print(f"  {i}. Node: {el['data']['name']:30s} {el['data'].get('stereotype', '')} [CONTAINS: {', '.join(children)}]")
        else:
            print(f"  {i}. Node: {el['data']['name']:30s} {el['data'].get('stereotype', '')}")
    elif el['type'] == 'Device':
        print(f"  {i}. Device: {el['data']['name']}")
    elif el['type'] == 'Artifact':
        print(f"  {i}. Artifact: {el['data']['name']}")
    elif el['type'] == 'DeploymentRelationship':
        print(f"  {i}. Relationship: {el['data'].get('source', 'N/A')} --[{el['data'].get('type', 'connects')}]--> {el['data'].get('target', 'N/A')}")

# Step 2: Generate deployment diagram
print("\n" + "-"*80)
print("STEP 2: DEPLOYMENT DIAGRAM GENERATION")
print("-"*80)

generator.generate_deployment_diagram(test_project_id, deployment_elements, "static", "generated_puml")

# Step 3: Show generated deployment PUML
print("\n" + "-"*80)
print("STEP 3: DEPLOYMENT PLANTUML CODE")
print("-"*80)

deployment_puml_file = f"generated_puml/deployment_{test_project_id}.puml"
if os.path.exists(deployment_puml_file):
    with open(deployment_puml_file, 'r') as f:
        puml_content = f.read()
    print(f"\nFile: {deployment_puml_file}\n")
    print(puml_content)
else:
    print(f"⚠️ PUML file not found: {deployment_puml_file}")

# Step 4: Check deployment output image
print("\n" + "-"*80)
print("STEP 4: DEPLOYMENT OUTPUT IMAGE")
print("-"*80)

deployment_png_file = f"static/deployment_{test_project_id}.png"
if os.path.exists(deployment_png_file):
    file_size = os.path.getsize(deployment_png_file)
    print(f"\n✅ Deployment diagram generated: {deployment_png_file}")
    print(f"   File size: {file_size:,} bytes")
else:
    print(f"\n❌ PNG file not found: {deployment_png_file}")

print("\n" + "="*80 + "\n")
