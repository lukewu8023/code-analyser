import os
import weaviate
import key_config

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate

EMBEDDING_MODEL = "text-embedding-ada-002"

embeddings = OpenAIEmbeddings()

text = "I like banana."
query_result = embeddings.embed_query(text)
print(f"+++Text embedding length: {len(query_result)}")

client = weaviate.Client(
    url=os.environ.get("WEAVIATE_URL"),
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
)
print(f"+++Weaviate is ready? {client.is_ready()}")

db = Weaviate.from_texts(
    text, embeddings, weaviate_url=os.environ.get("WEAVIATE_URL"), by_text=False
)

query = "what do you like?"
docs = db.similarity_search(query)

print(f"+++Weaviate response: {docs}")
