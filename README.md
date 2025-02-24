# Gestión de Documentos 

## Descripción General

Este código implementa una aplicación en Streamlit para la gestión de documentos de texto, CSV ,TXT y PDF. Su objetivo es permitir la carga y procesamiento de estos documentos, extrayendo su contenido y almacenándolo en una base de datos vectorial utilizando Qdrant. Además, proporciona una vista previa del contenido de los documentos subidos.

## Estructura del Código

### 1. Detección de Codificación de Archivos TXT y CSV

```python
def detect_encoding(file):
    """Detecta la codificación de un archivo usando chardet."""
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding_detected = result["encoding"]
    file.seek(0)  # Resetear puntero del archivo
    return encoding_detected
```

- Lee el contenido del archivo.
- Utiliza `chardet.detect` para determinar la codificación.
- Restablece el puntero del archivo para futuras lecturas.

### 2. Procesamiento de Archivos TXT

```python
def process_txt(file, collection_name):
    """Procesa archivos TXT con detección de codificación."""
    encoding = detect_encoding(file)
    text_content = file.read().decode(encoding, errors="ignore")
    dump_txt_pdf_documents_to_qdrant(name=collection_name, raw_text=text_content)
    st.subheader("File Content Preview")
    st.text_area("Preview", text_content[:1000])
```

- Detecta la codificación del archivo.
- Lee y decodifica el contenido.
- Almacena el texto en la base de datos vectorial.
- Muestra una vista previa de los primeros 1000 caracteres.

### 3. Procesamiento de Archivos CSV

```python
def process_csv(file, collection_name):
    """Procesa archivos CSV con detección de codificación."""
    encoding = detect_encoding(file)
    df = pd.read_csv(file, encoding=encoding)
    text_content = df.to_string()
    dump_txt_pdf_documents_to_qdrant(name=collection_name, raw_text=text_content)
    st.subheader("CSV Preview")
    st.dataframe(df.head())
```

- Detecta la codificación del archivo CSV.
- Carga los datos en un DataFrame de Pandas.
- Convierte el contenido a texto y lo almacena en Qdrant.
- Muestra una vista previa de las primeras filas del archivo.

### 4. Procesamiento de Archivos PDF

```python
def process_pdf(file, collection_name):
    """Procesa archivos PDF extrayendo texto."""
    temp_path = f"temp_{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())
    pdf_docs = pdf_to_document(temp_path)
    dump_txt_pdf_documents_to_qdrant(name=collection_name, pdf_docs=pdf_docs)
    os.remove(temp_path)
```

- Guarda el archivo PDF temporalmente.
- Extrae el contenido utilizando `pdf_to_document`.
- Almacena el texto extraído en la base de datos vectorial.
- Elimina el archivo temporal para optimizar el uso de espacio.

### 5. Interfaz Principal en Streamlit

```python
def doc_gestion():
    """Gestión de documentos en Streamlit."""
    st.title("Document Management")
    st.write("Upload TXT, CSV, or PDF files to train the model")
    collection_name = st.text_input("Collection Name", help="Enter a name for the collection where documents will be stored")
    uploaded_file = st.file_uploader("Upload Document", type=["txt", "csv", "pdf"], help="Select a TXT, CSV, or PDF file to upload")

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
```

- Crea la interfaz de usuario en Streamlit.
- Permite ingresar un nombre de colección.
- Permite cargar archivos TXT, CSV o PDF.
- Llama a la función correspondiente según el tipo de archivo.
- Maneja errores y muestra mensajes de éxito o fallo.

### 6. Instrucciones de Uso

```
with st.expander("Usage Instructions"):
    st.markdown("""
    1. Enter a collection name where your documents will be stored.
    2. Upload a TXT, CSV, or PDF file.
    3. Wait for processing to complete.
    4. View the document preview to confirm successful upload.

    **Note**: Documents are processed and stored in the vector database for model training.
    """)
```

- Explicación de los pasos para usar la aplicación.
- Notas sobre el procesamiento y almacenamiento de los documentos.

