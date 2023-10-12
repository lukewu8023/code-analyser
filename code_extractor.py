from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = GenericLoader.from_filesystem(
    "/Users/luke/Documents/workspace/gpt/langchain/libs/experimental/langchain_experimental/plan_and_execute",
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(),
)

documents = loader.load()
print(len(documents))
for document in documents:
    name = document.metadata["source"]
    code = document.page_content

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON
)

texts = python_splitter.split_documents(documents)
for text in texts:
    print(text)
