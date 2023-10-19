import os
from langchain import PromptTemplate
import key_config

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = GenericLoader.from_filesystem(
    "/Users/luke/Documents/workspace/java/load-example",
    glob="**/*",
    suffixes=[".java"],
    parser=LanguageParser(),
)

documents = loader.load()
print(f"+++Number of loaded documents: {len(documents)}")

code = ""
for document in documents:
    name = document.metadata["source"]
    code = document.page_content
print(f"+++Code content: {code}")

# java_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.JAVA)

# texts = java_splitter.split_documents(documents)
# for text in texts:
#     print(f"+++Trunk text content: {text}")

chat = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1024)

template_string = """

Please read the code: 
'''{sourceCode}''' 

extract the below information:
1) what is the package name of the class
2) what is the class name
3) how many methods and methods name
4) what are the parameters of method
5) description of method, describe as details as possible

Output the json string with the above information to below attributes, data seperate by each method:
"method_name"
"package_name"
"class_name"
"parameters"
"method_desc"

"""

prompt_template = ChatPromptTemplate.from_template(template_string)
message = prompt_template.format_messages(sourceCode=code)
response = chat(message)
print(f"+++ChatGPT response: {response.content}")
