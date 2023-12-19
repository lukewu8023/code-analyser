import os
import json
import weaviate

from langchain.embeddings import OpenAIEmbeddings


def get_data_model(userQuery: str) -> str:
    response = [{"data model": "Unknown data model"}]
    with open(r"data/concept.json") as meta_data_file:
        meta_data = json.load(meta_data_file)
    return json.dumps(meta_data)


def get_data_info(userQuery: str) -> str:
    response = [{"data model": "Unknown data model"}]

    embeddings_model = OpenAIEmbeddings()
    embedded_query = embeddings_model.embed_query(userQuery)
    client = weaviate.Client(os.environ.get("WEAVIATE_URL"))
    response = (
        client.query.get("Codev1", ["method_summary"])
        .with_near_vector({"vector": embedded_query})
        .with_limit(1)
        .with_additional(["distance"])
        .do()
    )
    print(json.dumps(response, indent=2))
    return json.dumps(response, indent=2)
