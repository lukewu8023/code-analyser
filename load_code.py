import os
import weaviate

from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate

code_path = ""
loader = GenericLoader.from_filesystem(
    code_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(),
)
documents = loader.load()
print(len(documents))
python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON)
texts = python_splitter.split_documents(documents)
for text in texts:
    print(text)

client = weaviate.Client(url="")
print(f"+++Weaviate is ready? {client.is_ready()}")

os.environ["OPENAI_API_BASE"] = ""
os.environ["OPENAI_API_KEY"] = ""

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
text = "This is a test document."
query_result = embeddings.embed_query(text)
print(query_result[:5])
doc_result = embeddings.embed_documents([text])
print(doc_result[0][:5])

vectorstore = Weaviate.from_documents(
    texts, embeddings, client=client, by_text=False, index_name="Lcpe"
)
print(f"+++Vector BD indext name:  {vectorstore._index_name}")
