import streamlit as st
from src.auth import Auth

def run(user):
    st.header("User Settings")
    auth = Auth()
    email = st.text_input("Email", value=user.email)
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Email / Password"):
        try:
            update_data = {}
            if email != user.email:
                update_data['email'] = email
            if new_password:
                update_data['password'] = new_password
            if update_data:
                auth.update_user(update_data)
                st.success("User details updated. Please log out and log in again.")
            else:
                st.info("No changes to update.")
        except Exception as e:
            st.error(f"Failed to update user info: {e}")
