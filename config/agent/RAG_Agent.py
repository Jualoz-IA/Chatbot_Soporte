from qdrant_client.http.models import Distance, VectorParams
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from config.agent.Gemma2_9b_it import llm
from config.agent.prompts import condense_question_prompt, qa_prompt
from langchain_qdrant import QdrantVectorStore
from config.database.qdrant_gen_connection import client, hf
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

class RAGAgent:
    def __init__(self):
        self.vector_stores = {}
        self.chains = {}

    def get_chain(self, collection_name):
        if collection_name in self.chains:
            return self.chains[collection_name]

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=hf,
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            condense_question_prompt=condense_question_prompt,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=True,
            verbose=True
        )

        self.chains[collection_name] = chain
        return chain

    def invoke(self, question, chat_history, collection="PRUEBA 2"):
        # Asegurar que la pregunta está en UTF-8
        question = question.encode("utf-8", "ignore").decode("utf-8")

        # Debug logging
        st.write(f"Pregunta recibida para colección {collection}:", question)

        # Parsear el historial del chat asegurando UTF-8
        chat_history_parsed = [
            HumanMessage(content=msg['content'].encode("utf-8", "ignore").decode("utf-8"))
            if msg['role'] == 'user' else
            AIMessage(content=msg['content'].encode("utf-8", "ignore").decode("utf-8"))
            for msg in chat_history[:-1]
        ]

        chain = self.get_chain(collection)

        # Obtener respuesta
        response = chain.invoke({
            "question": question,
            "chat_history": chat_history_parsed
        })

        # Debug de documentos recuperados
        st.write("Documentos recuperados:", [doc.page_content for doc in response['source_documents']])

        return response

# Crear una instancia global del agente
rag_agent = RAGAgent()
