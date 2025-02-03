from qdrant_client.http.models import  Distance, VectorParams
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from  config.langchainModels.Gemma2_9b_it import llm
from langchain_qdrant import QdrantVectorStore
from langchain.prompts import ChatPromptTemplate
from config.database.qdrant_gen_connection import client, hf

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

condense_question_template = """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone Question: 
"""

condense_question_prompt = ChatPromptTemplate.from_template(condense_question_template)

from langchain_core.prompts import PromptTemplate

qa_prompt = """I want you to act as a knowledge-based assistant named 'AI Expert'. Using only the provided context, answer the user's questions accurately and concisely.  
- If the context does not contain relevant information, respond with: "Hmm, I'm not sure" and stop there.  
- Do not fabricate or assume any information beyond what is provided.  
- Stay in character at all times.  

-------------------  
{{context}}  

REMEMBER: If no relevant information is found in the context, simply say "Hmm, I'm not sure." Do not attempt to generate an answer beyond the given data.  

Based on the following conversation and a follow-up question, rephrase the follow-up question as a self-contained question.  

Chat History:  
{{chat_history}}  

Question:{{question}}  
"""

qa_prompt = ChatPromptTemplate.from_messages(qa_prompt)
retriever = vector_store.retrieval_mode(search_kwargs={"k": 5})

chain = ConversationalRetrievalChain.from_llm(llm, retriever,
        condense_question_prompt=condense_question_prompt,
        combine_docs_chain_kwargs={"prompt": qa_prompt,},
        return_source_document=True, verbose=True)

chain.combine_docs_chain
ai_msg = chain.invoke({"question": "Whats the capital of France", "chat_history":[]})


