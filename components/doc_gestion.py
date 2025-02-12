import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import os
import chardet
from config.database.qdrant_gen_connection import (
    create_qdrant_collection,
    dump_txt_pdf_documents_to_qdrant,
    pdf_to_document,
)

def detect_encoding(file):
    """Detecta la codificación de un archivo usando chardet."""
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding_detected = result["encoding"]
    file.seek(0)  # Resetear puntero del archivo
    return encoding_detected

def process_txt(file, collection_name):
    """Procesa archivos TXT con detección de codificación."""
    encoding = detect_encoding(file)
    text_content = file.read().decode(encoding, errors="ignore")

    # Enviar datos a la base de datos vectorial
    dump_txt_pdf_documents_to_qdrant(
        name=collection_name,
        raw_text=text_content
    )

    # Vista previa
    st.subheader("File Content Preview")
    st.text_area("Preview", text_content[:1000])  # Muestra los primeros 1000 caracteres

def process_csv(file, collection_name):
    """Procesa archivos CSV con detección de codificación."""
    encoding = detect_encoding(file)
    df = pd.read_csv(file, encoding=encoding)

    text_content = df.to_string()
    dump_txt_pdf_documents_to_qdrant(
        name=collection_name,
        raw_text=text_content
    )

    # Vista previa
    st.subheader("CSV Preview")
    st.dataframe(df.head())  # Muestra las primeras filas

def process_pdf(file, collection_name):
    """Procesa archivos PDF extrayendo texto."""
    temp_path = f"temp_{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())  # Guardar temporalmente el PDF

    pdf_docs = pdf_to_document(temp_path)
    dump_txt_pdf_documents_to_qdrant(
        name=collection_name,
        pdf_docs=pdf_docs
    )
    os.remove(temp_path)  # Eliminar archivo temporal

    # Vista previa del PDF
    st.subheader("PDF Preview")
    with st.expander("View PDF Content"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page_num in range(min(len(doc), 3)):  # Muestra las primeras 3 páginas
            st.write(f"Page {page_num + 1}")
            st.text(doc[page_num].get_text())

def doc_gestion():
    """Gestión de documentos en Streamlit."""
    st.title("Document Management")
    st.write("Upload TXT, CSV, or PDF files to train the model")

    collection_name = st.text_input(
        "Collection Name", 
        help="Enter a name for the collection where documents will be stored"
    )

    uploaded_file = st.file_uploader(
        "Upload Document", 
        type=["txt", "csv", "pdf"],
        help="Select a TXT, CSV, or PDF file to upload"
    )

    if uploaded_file and collection_name:
        with st.spinner("Processing document..."):
            try:
                create_qdrant_collection(collection_name)

                if uploaded_file.name.endswith('.txt'):
                    process_txt(uploaded_file, collection_name)
                elif uploaded_file.name.endswith('.csv'):
                    process_csv(uploaded_file, collection_name)
                elif uploaded_file.name.endswith('.pdf'):
                    process_pdf(uploaded_file, collection_name)

                st.success(f"Document successfully uploaded to collection: {collection_name}")

            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

    with st.expander("Usage Instructions"):
        st.markdown("""
        1. Enter a collection name where your documents will be stored.
        2. Upload a TXT, CSV, or PDF file.
        3. Wait for processing to complete.
        4. View the document preview to confirm successful upload.

        **Note**: Documents are processed and stored in the vector database for model training.
        """)

doc_gestion()
