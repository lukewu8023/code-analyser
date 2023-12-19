import json
import os
import weaviate
import key_config

from langchain.embeddings import OpenAIEmbeddings

with open("data/code_cu.json") as f:
    contents = f.read()
data = json.loads(contents)
# f = open("source_code.json")
# data = json.load(f)
print(f"+++Data: {data}")

# [test file load]
# for i, method in enumerate(data["methods"]):
#     print(f"+++method: {i+1}")
#     print(method["method_name"])

embeddings_model = OpenAIEmbeddings()
# [test embedding]
# embeddings = embeddings_model.embed_documents(["Hi there!"])
# print(len(embeddings[0]))
# print(len(embeddings))

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))
print(f"+++Weaviate is ready? {client.is_ready()}")

client.batch.configure(batch_size=100)
with client.batch as batch:
    for i, method in enumerate(data["methods"]):
        print(f"+++importing method info: {i+1}")

        method_summary = (
            "method name is ["
            + method["method_name"]
            + "], package name is ["
            + method["package_name"]
            + "], class name is ["
            + method["class_name"]
            + "], this method "
            + ("" if method["is_interface"] else "not")
            + " belongs to an interface"
            + ", parameters in this method are "
            + json.dumps(method["parameters"])
            + ", invoked methods in this method are "
            + json.dumps(method["invoked_methods"])
            + ", method description is ["
            + method["method_desc"]
            + "]"
        )

        properties = {
            "method_name": method["method_name"],
            "package_name": method["package_name"],
            "class_name": method["class_name"],
            "is_interface": method["is_interface"],
            "parameters": method["parameters"],
            "invoked_methods": method["invoked_methods"],
            "method_desc": method["method_desc"],
            "method_summary": method_summary,
        }

        embed_document = method_summary
        print(f"+++embed document: {embed_document}")
        embeddings = embeddings_model.embed_documents([embed_document])
        print(len(embeddings))
        print(len(embeddings[0]))

        batch.add_data_object(properties, "Codev1", vector=embeddings[0])
