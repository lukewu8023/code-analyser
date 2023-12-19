import json
import os
import weaviate
import key_config

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))

# client.schema.delete_class("Codev1")
class_name = "Codev1"

new_class_obj = {
    "class": class_name,
    "properties": [
        {"name": "package_name", "dataType": ["text"]},
        {"name": "class_name", "dataType": ["text"]},
        {"name": "method_name", "dataType": ["text"]},
        {"name": "is_interface", "dataType": ["boolean"]},
        {
            "name": "parameters",
            "dataType": ["object[]"],
            "nestedProperties": [
                {"dataType": ["text"], "name": "name"},
                {"dataType": ["text"], "name": "type"},
            ],
        },
        {
            "name": "invoked_methods",
            "dataType": ["object[]"],
            "nestedProperties": [
                {"dataType": ["text"], "name": "variable_class_name"},
                {
                    "dataType": ["text"],
                    "name": "variable_name",
                },  # need handle null vaule
                {"dataType": ["text"], "name": "method_name"},
            ],
        },
        {"name": "method_desc", "dataType": ["text"]},
    ],
    "vectorizer": "none",
}
client.schema.create_class(new_class_obj)

response = client.schema.get(class_name)
# response = client.schema.get()
print(json.dumps(response, indent=2))
