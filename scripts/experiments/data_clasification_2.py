from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

# Load the NER model
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/ner-model-2020.02.10.tar.gz")

# Sample text
text = """
Elizabeth Gardner
Calle arquitectura #419
615 El Paso St, El Paso, TX 79901
"""

# Make predictions
result = predictor.predict(sentence=text)

# Extract entities
for word, tag in zip(result["words"], result["tags"]):
    print(f"{word}: {tag}")
