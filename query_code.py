import os
import json
import weaviate
import openai_config

from langchain.embeddings import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings()

embedded_query = embeddings_model.embed_query(
    "What is the method which calculates using uniform rate?"
)

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))

response = (
    client.query.get("Code1", ["method_name", "method_desc"])
    .with_near_vector({"vector": embedded_query})
    .with_limit(1)
    .with_additional(["distance"])
    .do()
)
print(json.dumps(response, indent=2))
