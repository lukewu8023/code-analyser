import os
import key_config

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = GenericLoader.from_filesystem(
    "/Users/luke/Documents/workspace/java/code-understanding",
    glob="**/*",
    suffixes=[".java"],
    parser=LanguageParser(),
)

documents = loader.load()
print(f"+++Number of loaded documents: {len(documents)}")
# java_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.JAVA)

# texts = java_splitter.split_documents(documents)
# for text in texts:
#     print(f"+++Trunk text content: {text}")

chat = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1024)

with open("prompt/prompt_extraction.txt") as f:
    contents = f.read()
template_string = contents
prompt_template = ChatPromptTemplate.from_template(template_string)

code = ""
with open("data/code.json", "a") as file:
    for document in documents:
        name = document.metadata["source"]
        code = document.page_content
        print(f"+++Code content: {code}")

        message = prompt_template.format_messages(sourceCode=code)
        response = chat(message)
        print(f"+++ChatGPT response: {response.content}")
        file.write(response.content + "\n")
