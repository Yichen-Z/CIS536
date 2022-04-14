from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
import sparknlp

# Start Spark Session with Spark NLP
spark = sparknlp.start()

# Download a pre-trained pipeline
pipeline = PretrainedPipeline('explain_document_dl', lang='en')

# Annotate your testing dataset
result = pipeline.annotate(
    "The Mona Lisa is a 16th century oil painting created by Leonardo. It's held at the Louvre in Paris.")

# What's in the pipeline
list(result.keys())
# Output: ['entities', 'stem', 'checked', 'lemma', 'document',
#          'pos', 'token', 'ner', 'embeddings', 'sentence']

# Check the results
result['entities']
# Output: ['Mona Lisa', 'Leonardo', 'Louvre', 'Paris']
