import streamlit as st
import pandas as pd
from config.database.conectionsql import SessionLocal
from config.database import user_crud, functionssql
from login import login
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter

def user_gestion():
    st.title("-- Gestión de Usuarios --")
    db = SessionLocal()

    # Obtener los roles desde la base de datos
    roles = functionssql.get_roles(db)
    if isinstance(roles, dict) and "error" in roles:
        st.error(roles["error"])
        roles = []  # Evitar errores si la consulta falla

    listar, agregar, modificar, eliminar = st.tabs(["Listar", "Agregar", "Modificar", "Eliminar"])

    with listar:
        # Ajustamos el tamaño de las columnas (70% para la tabla, 30% para la gráfica)
        col1, col2 = st.columns([0.7, 0.3])  

        users = user_crud.get_users(db)  # Obtener usuarios solo una vez

        if isinstance(users, dict) and "error" in users:
            st.error(users["error"])
        else:
            with col1:
                st.subheader("📋 Lista de Usuarios")
                df_users = pd.DataFrame([
                    {"ID": u.id, "Username": u.username, "Email": u.email, "Roles": ", ".join([role.name for role in u.roles])}
                    for u in users
                ])
                st.dataframe(df_users, use_container_width=True)  # Se expande mejor en la columna

            with col2:
                # Contar usuarios por rol usando Counter (más eficiente)
                role_counts = Counter(role.name for u in users for role in u.roles)

                if role_counts:
                    fig = px.pie(
                        values=role_counts.values(),
                        names=role_counts.keys(),
                        title="Distribución de Usuarios por Rol"
                    )
                    st.plotly_chart(fig, use_container_width=True)# Se ajusta mejor a la columna

    with agregar:
        st.subheader("➕ Agregar Nuevo Usuario")
        with st.form(key='Crear Cuenta'):
            col1, col2 = st.columns(2)  # Divide en dos columnas

            with col1:
                username_input = st.text_input('Enter UserName')
                password_input = st.text_input('Enter Password', type='password')

            with col2:
                email_input = st.text_input('Enter Email')
                role_input = st.selectbox("Selecciona un rol", roles, index=roles.index("user") if "user" in roles else 0)

            submit_button = st.form_submit_button('Crear Cuenta')

            if submit_button:
                if not username_input or not email_input or not password_input:
                    st.error("All fields are required.")
                elif len(username_input) < 3 or len(username_input) > 15:
                    st.error("Username must be between 3 and 15 characters long.")
                elif not login.is_valid_email(email_input):
                    st.error("Please enter a valid email address.")
                else:
                    result = functionssql.create_user(db, username_input, email_input, password_input, role_input)
                    if "error" in result:
                        st.error(result["error"])
                    elif "user" in result:
                        user = result["user"]
                        st.success(f"Account created for {user['username']} with role {user['roles']}!")
                        st.rerun()

    with modificar:
        st.subheader("✏️ Actualizar Usuario")
        col1, col2 = st.columns(2)  # Divide en dos columnas

        with col1:
            user_id = st.number_input("ID del Usuario", min_value=1, step=1)
            new_username = st.text_input("Nuevo Nombre de Usuario")

        with col2:
            new_email = st.text_input("Nuevo Correo Electrónico")
            new_role = st.selectbox("Selecciona un nuevo rol", roles)
        
        if st.button("Actualizar Usuario"):
            result = user_crud.update_user(db, user_id, new_username, new_email, new_role)
            if "success" in result:
                st.success(result["success"])
                st.rerun()
            else:
                st.error(result["error"])

    with eliminar:
        st.subheader("🗑️ Eliminar Usuario")
        user_id_to_delete = st.number_input("ID del Usuario a Eliminar", min_value=1, step=1)
        if st.button("Eliminar Usuario"):
            result = user_crud.delete_user(db, user_id_to_delete)
            if "success" in result:
                st.success(result["success"])
                st.rerun()
            else:
                st.error(result["error"])

    db.close()

if __name__ == "__main__":
    user_gestion()
