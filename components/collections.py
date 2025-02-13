import streamlit as st
from config.database.controllers import qdrant_controller

__name__ = '__collections__'

# Función para eliminar colección
def delete_collection(collection_name):
    try:
        qdrant_controller.delete_collection(collection_name)
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar la colección: {e}")

# Simulación de Modal
def collection_modal(edit_mode=None):
    with st.container():
        if edit_mode:
            st.subheader(f"Editar Colección: {edit_mode['Nombre']}")
            collection_name = edit_mode["Nombre"]  # No se puede cambiar el nombre al editar
            vector_size = st.number_input("Tamaño del vector:", min_value=1, value=edit_mode["Tamaño"])
            distance = st.selectbox(
                "Métrica de distancia:",
                ["Cosine", "Euclid", "Dot", "Manhattan"],
                index=["Cosine", "Euclid", "Dot", "Manhattan"].index(edit_mode["Métrica"])
            )
            action = "Actualizar"
        else:
            st.subheader("Crear Nueva Colección")
            collection_name = st.text_input("Nombre de la colección:")
            vector_size = st.number_input("Tamaño del vector:", min_value=1, value=768)
            distance = st.selectbox("Métrica de distancia:", ["Cosine", "Euclid", "Dot", "Manhattan"])
            action = "Crear"

        if st.button(action):
            try:
                if action == "Actualizar":
                    qdrant_controller.delete_collection(collection_name)
                qdrant_controller.recreate(collection_name, vector_size, distance)
                st.success(f"Colección '{collection_name}' {action.lower()}ada exitosamente.")
                st.session_state["modal_open"] = False
                st.rerun()
            except Exception as e:
                st.error(f"Error al {action.lower()} la colección: {e}")

# Mostrar la tabla con acciones
def display_table_with_actions():
    collections = qdrant_controller.table_collections()

    if collections:
        for idx, collection in enumerate(collections):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            with col1:
                st.text(collection["Nombre"])
            with col2:
                st.text(collection["Tamaño"])
            with col3:
                st.text(collection["Métrica"])
            with col4:
                if st.button("Editar", key=f"edit_{idx}"):
                    st.session_state["modal_open"] = True
                    st.session_state["edit_mode"] = collection
            with col5:
                if st.button("Eliminar", key=f"delete_{idx}"):
                    delete_collection(collection["Nombre"])
    else:
        st.write("No hay colecciones disponibles.")

# Interfaz principal
def main():
    st.title("Gestor de Colecciones - Qdrant")
    st.divider()
    display_table_with_actions()

    if st.session_state.get("modal_open"):
        collection_modal(st.session_state.get("edit_mode"))
    
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Crear Colección", use_container_width=True):
            st.session_state["modal_open"] = True
            st.session_state["edit_mode"] = None

if __name__ == "__collections__":
    if "modal_open" not in st.session_state:
        st.session_state["modal_open"] = False
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = None
    main()
