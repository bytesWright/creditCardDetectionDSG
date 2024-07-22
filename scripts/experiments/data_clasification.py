import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample text
text = """
Elizabeth Gardner
615 El Paso St
El Paso
TX 79901
Bank of America
"""

# Process the text
for line in text.split("\n"):
    doc = nlp(line)
    print(line)
    # Extract entities
    for ent in doc.ents:
        print("    ", ent.text,">", ent.label_)
