from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.docstore.document import Document
from qdrant_client.models import VectorParams
import streamlit as st
import os

model_name = os.getenv('EMBEDDINGS_MODEL')

client = QdrantClient(
    url = os.getenv('QDRANT_DATABASE_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)
@st.cache_resource
def load_embeddings(model_name):
    return HuggingFaceEmbeddings(model_name=model_name)

hf = load_embeddings(model_name)

def create_qdrant_collection(name):
    client.recreate_collection(
        collection_name = name,
        vectors_config=VectorParams(size=768, distance="Cosine")
    )

def pdf_to_document(pdf_path):
    # --- Procesamiento de un archivo PDF ---
    pdf_loader = PyPDFLoader(pdf_path)
    return pdf_loader.load()

def txt_to_document(txt_path):
    # --- Procesamiento de un archivo TXT ---
    txt_loader = TextLoader(txt_path)
    return txt_loader.load()

def dump_txt_pdf_documents_to_qdrant(name, raw_text=None, pdf_docs=None, txt_documents=None):
    """
    Combina documentos de PDF y TXT (si se proporcionan) y los indexa en una colección de Qdrant.
    
    Parámetros:
      name (str): Nombre de la colección en Qdrant.
      pdf_docs (list, opcional): Lista de documentos obtenidos de archivos PDF.
      txt_documents (list, opcional): Lista de documentos obtenidos de archivos TXT.
    """
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=name,
        embedding=hf,
    )

    # Combinar documentos de PDF y TXT en una sola lista
    documents = []
    if pdf_docs is not None:
        documents.extend(pdf_docs)
    if txt_documents is not None:
        documents.extend(txt_documents)
    # Agregar raw_text, convirtiéndolo en Document, si se proporciona
    if raw_text is not None:
        # Se crea un documento con el texto; puedes agregar metadatos si lo necesitas.
        documents.append(Document(page_content=raw_text))
    
    # Verificar que exista al menos un documento
    if not documents:
        return

    # Dividir documentos en fragmentos (chunks) para mejorar la calidad de los embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_with_chunks = text_splitter.split_documents(documents)

    # Agregar los documentos fragmentados al vector store en Qdrant
    vector_store.add_documents(docs_with_chunks)

    # Agregar los documentos al vector store
    vector_store.add_documents(docs_with_chunks)