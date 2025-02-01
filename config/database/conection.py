from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import  Distance, VectorParams
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import os

model_name = "paraphrase-MiniLM-L6-v2"

hf = HuggingFaceEmbeddings( 
    model_name = model_name
)

client = QdrantClient(
    url = "",
    api_key=os.getenv('QDRANT_API_KEY')
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="Pdd",
    embedding=hf,
)

retriver = vector_store.retrieval_mode(search_kwargs={"k": 5})
chain = ConversationalRetrievalChain.from_llm(llm, retriever, return_source_document=True)


#Módulo de colecciones debe consumir esta función
def create_qdrant_collection(name, vector_size):
    # Crear la colección en Qdrant
    # client.create_collection(
    #     collection_name=name,
    #     vectors_config=vector_params
    # )
    print(f'Colección "{name}" creada con éxito.')