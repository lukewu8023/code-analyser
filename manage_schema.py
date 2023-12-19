import json
import os
import weaviate
import key_config

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))

# client.schema.delete_class("LangChain_10b4617a9f7e4626ad403e60e8843ed5")
class_name = "Code1"

new_class_obj = {
    "class": class_name,
    "properties": [
        {"name": "package_name", "dataType": ["text"]},
        {"name": "class_name", "dataType": ["text"]},
        {"name": "method_name", "dataType": ["text"]},
        {"name": "method_desc", "dataType": ["text"]},
    ],
    "vectorizer": "none",
}
# client.schema.create_class(new_class_obj)

response = client.schema.get(class_name)
# response = client.schema.get()
print(json.dumps(response, indent=2))
