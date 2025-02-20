import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from typing import Dict
import pandas as pd
from config.database.controllers import collection_controller as cc, qdrant_controller
from config.database.sql_connection import SessionLocal

__name__ = '__options__'

def chat_options_view():
    st.title("Gestión de Opciones de Chat")
    
    db: Session = SessionLocal()
    
    # Crear tabs para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs(["Ver Opciones", "Crear/Editar Opción", "Importar Opciones"])
    
    # Tab 1: Ver Opciones
    with tab1:
        st.header("Opciones Actuales")
        
        # Obtener todas las opciones y convertir a DataFrame
        options = cc.get_all_options(db)
        if isinstance(options, dict) and "error" in options:
            st.error(options["error"])
        else:
            df = pd.DataFrame(
                [(opt.option, opt.colleption, opt.active) for opt in options],
                columns=["Opción", "Colección", "Activo"]
            )
            
            # Mostrar DataFrame con editor
            edited_df = st.data_editor(
                df,
                hide_index=True,
                column_config={
                    "Activo": st.column_config.CheckboxColumn(
                        "Activo",
                        help="Activar/Desactivar opción",
                        default=True,
                    )
                }
            )
            
            # Botón para guardar cambios
            if st.button("Guardar Cambios"):
                try:
                    for idx, row in edited_df.iterrows():
                        cc.update_option(
                            db,
                            option=row["Opción"],
                            collection=row["Colección"],
                            active=row["Activo"]
                        )
                    st.success("Cambios guardados exitosamente")
                except Exception as e:
                    st.error(f"Error al guardar cambios: {str(e)}")
    
    # Tab 2: Crear/Editar Opción
    with tab2:
        st.header("Crear Nueva Opción")
        names = qdrant_controller.get_names_collections()
        
        # Formulario para nueva opción
        with st.form("nueva_opcion"):
            option = st.text_input("Texto de la Opción")
            collection = st.selectbox("Collection", names)
            active = st.checkbox("Activo", value=True)
            
            submitted = st.form_submit_button("Crear Opción")
            if submitted:
                if option and collection:
                    result = cc.create_option(db, option, collection, active)
                    if "success" in result:
                        st.success(result["success"])
                    else:
                        st.error(result["error"])
                else:
                    st.warning("Por favor completa todos los campos")
    
    # Tab 3: Importar Opciones
    with tab3:
        st.header("Importar Opciones")
        st.write("Sube un archivo CSV con las columnas: Opción, Colección, Activo")
        
        uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if st.button("Importar Opciones"):
                    options_data = [
                        {
                            "option": row["Opción"],
                            "collection": row["Colección"],
                            "active": row["Activo"]
                        }
                        for _, row in df.iterrows()
                    ]
                    result = cc.bulk_create_options(db, options_data)
                    if "success" in result:
                        st.success(result["success"])
                    else:
                        st.error(result["error"])
            except Exception as e:
                st.error(f"Error al procesar el archivo: {str(e)}")

        # Mostrar ejemplo de formato CSV
        st.write("Ejemplo de formato CSV:")
        example_df = pd.DataFrame([
            ["Debo hacer facturación electrónica", "obligated_collection", True],
            ["Que documentos necesito", "documents_collection", True]
        ], columns=["Opción", "Colección", "Activo"])
        st.dataframe(example_df)

if __name__ == "__options__":
    chat_options_view()