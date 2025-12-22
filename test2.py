import spacy

# Load the trained model
nlp = spacy.load("./architecture_uml_model/model-best")

print("Pipeline components:", nlp.pipe_names)  # Should include 'ner'
print("Entity labels:", nlp.get_pipe("ner").labels)  # Should list all custom labels

# Test extraction
test_text = "The frontend component uses a REST API interface to communicate with the backend service. The backend is deployed on a Docker container running on an AWS EC2 node."

doc = nlp(test_text)
print(f"\nTest text: {test_text}\n")
print("Extracted entities:")
for ent in doc.ents:
    print(f"  - {ent.text:30s} → {ent.label_}")
