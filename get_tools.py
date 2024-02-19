import os
import json
import weaviate

from langchain.embeddings import OpenAIEmbeddings


def get_db_schema(temp: str) -> str:
    db_schema = [{"database schema": "Unknown database schema"}]
    with open(r"data/table.json") as db_schema_file:
        db_schema = json.load(db_schema_file)
    return json.dumps(db_schema)


def get_meta_data(temp: str) -> str:
    meta_data = [{"meta data": "Unknown meta data"}]
    with open(r"data/metadata.json") as meta_data_file:
        meta_data = json.load(meta_data_file)
    return json.dumps(meta_data)


def get_code_info(userQuery: str) -> str:
    response = [{"code info": "Unknown code info"}]

    embeddings_model = OpenAIEmbeddings()
    embedded_query = embeddings_model.embed_query(userQuery)
    client = weaviate.Client(os.environ.get("WEAVIATE_URL"))
    response = (
        client.query.get("Codev1", ["method_summary"])
        .with_near_vector({"vector": embedded_query})
        .with_limit(3)
        .with_additional(["distance"])
        .do()
    )
    print(json.dumps(response, indent=2))
    return json.dumps(response, indent=2)
