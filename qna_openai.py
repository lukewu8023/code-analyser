import os
import weaviate

from langchain.vectorstores import Weaviate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

os.environ["OPENAI_API_BASE"] = ""
os.environ["OPENAI_API_KEY"] = ""

client = weaviate.Client(url="http://149.28.241.76:8088")
print(f"+++Weaviate is ready? {client.is_ready()}")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

model = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1024)
vectorstore = Weaviate(
    client=client,
    index_name="LangChain_a95eb91a363145d68aa5fb7c9d151e00",
    embedding=embeddings,
    text_key="text",
)
retriever = vectorstore.as_retriever()
memory = ConversationSummaryMemory(llm=model, memory_key="chat_history")
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, memory=memory)
query = "what is the code about?"
# docs = vectorstore.similarity_search_by_text(query)
# print(docs[0].page_content)

print(vectorstore._client.schema.get())
