import os
import weaviate
import key_config

import langchain
from langchain.vectorstores import Weaviate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

client = weaviate.Client(os.environ.get("WEAVIATE_URL"))
print(f"+++Weaviate is ready? {client.is_ready()}")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

model = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1024)
vectorstore = Weaviate(
    client=client,
    index_name="Algos",
    embedding=embeddings,
    text_key="text",
    by_text=False,
)
print(f"+++Vector BD indext name: {vectorstore._index_name}")
# print(vectorstore._client.schema.get())

# query = "what is the value change on the input parameter of PlanAndExecute?"
# query = "What is the logic of generating off spring by the 1st input paramaters in cross method of SinglePointCrossover?"
query = "describe the purpose SinglePointCrossover?"
docs = vectorstore.similarity_search(query)
print(f"+++Similarity Search: {docs}")

langchain.debug = True
retriever = vectorstore.as_retriever()
memory = ConversationSummaryMemory(
    llm=model, memory_key="chat_history", return_messages=True
)
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, memory=memory)
# result = qa(query)
result = qa({"question": query, "chat_history": []})
print(f"+++Conversational Search: {result['answer']}")
