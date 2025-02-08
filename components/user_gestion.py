import streamlit as st
import pandas as pd
from config.database.conectionsql import SessionLocal
from config.database import user_crud
from config.database import functionssql
from login import login

def user_gestion():
    st.title("-- Gestión de Usuarios --")

    db = SessionLocal()

    # **Mostrar Usuarios**
    st.subheader("📋 Lista de Usuarios")
    users = user_crud.get_users(db)
    
    if isinstance(users, dict) and "error" in users:
        st.error(users["error"])
    else:
        df_users = pd.DataFrame([{"ID": u.id, "Username": u.username, "Email": u.email, "pass": u.password} for u in users])
        st.dataframe(df_users)

    # **Crear Usuario**
    st.subheader("➕ Agregar Nuevo Usuario")
    with st.form(key='Crear Cuenta'):
        username_input = st.text_input('Enter UserName')
        email_input = st.text_input('Enter Email')
        password_input = st.text_input('Enter Password', type='password')
        submit_button = st.form_submit_button('Crear Cuenta')

        if submit_button:
            # Validar que los campos no estén vacíos
            if not username_input or not email_input or not password_input:
                st.error("All fields are required.")
            # Validar rango de longitud para el username
            elif len(username_input) < 3 or len(username_input) > 15:
                st.error("Username must be between 3 and 15 characters long.")
            # Validar formato del email
            elif not login.is_valid_email(email_input):
                st.error("Please enter a valid email address.")
            else:
                db = SessionLocal()
                result = functionssql.create_user(db, username_input, email_input, password_input)
                
                if "error" in result:
                    st.error(result["error"])  # Muestra el mensaje de error
                elif "user" in result:
                    user = result["user"]
                    st.success(f"Account created for {user.username} with email {user.email}!")
                else:
                    st.error("Unexpected error occurred.")

    # **Actualizar Usuario**
    st.subheader("✏️ Actualizar Usuario")
    user_id = st.number_input("ID del Usuario", min_value=1, step=1)
    new_username = st.text_input("Nuevo Nombre de Usuario")
    new_email = st.text_input("Nuevo Correo Electrónico")
    if st.button("Actualizar Usuario"):
        result = user_crud.update_user(db, user_id, new_username, new_email)
        if "success" in result:
            st.success(result["success"])
            st.experimental_rerun()
        else:
            st.error(result["error"])

    # **Eliminar Usuario**
    st.subheader("🗑️ Eliminar Usuario")
    user_id_to_delete = st.number_input("ID del Usuario a Eliminar", min_value=1, step=1)
    if st.button("Eliminar Usuario"):
        result = user_crud.delete_user(db, user_id_to_delete)
        if "success" in result:
            st.success(result["success"])
            st.experimental_rerun()
        else:
            st.error(result["error"])

    db.close()

# Ejecutar en modo independiente
if __name__ == "__main__":
    user_gestion()
