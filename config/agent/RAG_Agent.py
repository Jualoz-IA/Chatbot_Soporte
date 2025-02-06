from qdrant_client.http.models import  Distance, VectorParams
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from  config.agent.Gemma2_9b_it import llm
from config.agent.prompts import condense_question_prompt, qa_prompt
from langchain_qdrant import QdrantVectorStore
from config.database.qdrant_gen_connection import client, hf
from langchain_core.messages import HumanMessage, AIMessage
# RAG (Retrieval-Augmented Generation)

collection_name = "text"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance="Cosine")
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="text",
    embedding=hf,
    )

# Convierte vector_store en un retriever (un sistema que busca los documentos más relevantes).
# search_kwargs={"k": 5}: Define que devuelve los 5 documentos más similares al input del usuario.
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Crea una cadena de recuperación conversacional con:
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,  # El modelo de lenguaje (GPT u otro).
    retriever=retriever,  # El recuperador de información.
    condense_question_prompt=condense_question_prompt,  # Un prompt para reformular la pregunta en un formato más claro.
    combine_docs_chain_kwargs={"prompt": qa_prompt},  # Usa qa_prompt para combinar la respuesta a partir de los documentos encontrados.
    return_source_documents=True,  # Devuelve los documentos fuente usados en la respuesta.
    verbose=True  # Activa la depuración para ver detalles de los pasos internos.
)
## ejemplo de entrada
## chat_history = [
#     {"role": "user", "content": "Hola, ¿cómo estás?"},
#     {"role": "assistant", "content": "Estoy bien, gracias. ¿Cómo puedo ayudarte?"},
#     {"role": "user", "content": "Quiero saber sobre Python."}
# ]
def invoke(question, chat_history):
    chat_history_parsed = [
        HumanMessage(content=msg['content']) if msg['role'] == 'user' else
        AIMessage(content=msg['content'])
        for msg in chat_history
    ]

#chain.combine_docs_chain
    return chain.invoke({"question": question, "chat_history":chat_history_parsed})

## ejemplo de salida
# [
#     HumanMessage(content="Hola, ¿cómo estás?"),
#     AIMessage(content="Estoy bien, gracias. ¿Cómo puedo ayudarte?"),
#     HumanMessage(content="Quiero saber sobre Python.")
# ]

