import os
import json
import weaviate
import key_config

from langchain.embeddings import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings()

embedded_query = embeddings_model.embed_query(
    "what are the invoked methods of link method"
)

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))

response = (
    client.query.get("Codev1", ["method_summary"])
    .with_near_vector({"vector": embedded_query})
    .with_limit(3)
    .with_additional(["distance"])
    .do()
)
print(json.dumps(response, indent=2))

# STEP 1 - Prepare a helper function to iterate through data in batches
# def get_batch_with_cursor(collection_name, batch_size, cursor=None):
#     # First prepare the query to run through data
#     query = (
#         client.query.get(
#             collection_name,  # update with your collection name
#             ["method_name", "method_desc"],  # update with the required properties
#         )
#         .with_additional(["id vector"])
#         .with_limit(batch_size)
#     )

#     # Fetch the next set of results
#     if cursor is not None:
#         result = query.with_after(cursor).do()
#     # Fetch the first set of results
#     else:
#         result = query.do()

#     return result["data"]["Get"][collection_name]


# # STEP 2 - Iterate through the data
# cursor = None
# while True:
#     # Get the next batch of objects
#     next_batch = get_batch_with_cursor("Codev1", 100, cursor)

#     # Break the loop if empty – we are done
#     if len(next_batch) == 0:
#         break

#     # Here is your next batch of objects
#     print(next_batch)

#     # Move the cursor to the last returned uuid
#     cursor = next_batch[-1]["_additional"]["id"]
