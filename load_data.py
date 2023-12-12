import json
import os
import weaviate
import key_config

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

with open("source_code2.json") as f:
    contents = f.read()
data = json.loads(contents)
# f = open("source_code.json")
# data = json.load(f)
print(f"+++Data: {data}")

for i, method in enumerate(data["methods"]):
    print(f"+++method: {i+1}")
    print(method["method_name"])

embeddings_model = OpenAIEmbeddings()
embeddings = embeddings_model.embed_documents(["Hi there!"])
print(len(embeddings[0]))

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))

client.batch.configure(batch_size=100)
with client.batch as batch:
    for i, method in enumerate(data["methods"]):
        print(f"+++importing method info: {i+1}")

        properties = {
            "method_name": method["method_name"],
            "package_name": method["package_name"],
            "class_name": method["class_name"],
            "method_desc": method["method_desc"],
        }

        embed_document = (
            "method name is "
            + method["method_name"]
            + ", package name is "
            + method["package_name"]
            + ", class name is "
            + method["class_name"]
            + ", method description is "
            + method["method_desc"]
        )
        print(f"+++embed document: {embed_document}")

        embeddings = embeddings_model.embed_documents([method["method_desc"]])
        print(len(embeddings[0]))
        # print(embeddings[0])

        batch.add_data_object(properties, "Code1", vector=embeddings[0])
