from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = GenericLoader.from_filesystem(
    "",
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
)

documents = loader.load()
print(documents)
for document in documents:
    name = document.metadata["source"]
    code = document.page_content

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
)

texts = python_splitter.split_documents(documents)
for text in texts:
    print(text)
