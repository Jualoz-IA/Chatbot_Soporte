import streamlit as st
from config.database.qdrant_gen_connection import (
    create_qdrant_collection,
    dump_txt_pdf_documents_to_qdrant,
    pdf_to_document,
)
import pandas as pd
import fitz  # PyMuPDF
import os

def main():  # Cambié doc_gestion() a main()
    st.title("Document Management")
    st.write("Upload CSV or PDF files to train the model")

    # Collection name input
    collection_name = st.text_input(
        "Collection Name", 
        help="Enter a name for the collection where documents will be stored"
    )

    uploaded_file = st.file_uploader(
        "Upload Document", 
        type=["csv", "pdf"],
        help="Select a CSV or PDF file to upload"
    )

    if uploaded_file and collection_name:
        with st.spinner("Processing document..."):
            try:
                # Create collection if it doesn't exist
                create_qdrant_collection(collection_name)

                # Process file based on type
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    text_content = df.to_string()
                    dump_txt_pdf_documents_to_qdrant(
                        name=collection_name,
                        raw_text=text_content
                    )
                elif uploaded_file.name.endswith('.pdf'):
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    pdf_docs = pdf_to_document(temp_path)
                    dump_txt_pdf_documents_to_qdrant(
                        name=collection_name,
                        pdf_docs=pdf_docs
                    )
                    os.remove(temp_path)

                st.success(f"Document successfully uploaded to collection: {collection_name}")

                # Display document preview
                st.subheader("Document Preview")
                if uploaded_file.name.endswith('.csv'):
                    st.dataframe(df.head())
                elif uploaded_file.name.endswith('.pdf'):
                    with st.expander("View PDF Content"):
                        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                        for page_num in range(min(len(doc), 3)):  # Preview first 3 pages
                            st.write(f"Page {page_num + 1}")
                            st.text(doc[page_num].get_text())

            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

    with st.expander("Usage Instructions"):
        st.markdown("""
        1. Enter a collection name where your documents will be stored.
        2. Upload either a CSV or PDF file.
        3. Wait for processing to complete.
        4. View the document preview to confirm successful upload.

        **Note**: Documents are processed and stored in the vector database for model training.
        """)

if __name__ == "__main__":
    main()
