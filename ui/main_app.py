import sys
import os

# Add project root directory to Python path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.auth import Auth
from ui import display_menu, menu_management, place_order, generate_bill, display_customers, customer_management, settings

auth = Auth()

def safe_rerun():
    # Toggle a dummy session state variable to force rerun
    st.session_state['rerun'] = not st.session_state.get('rerun', False)

def login_ui():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            result = auth.login(email, password)
            if result.user:
                st.session_state['user'] = result.user
                safe_rerun()  # safe rerun workaround
            else:
                st.error("Invalid credentials")
        except Exception as e:
            if "Email not confirmed" in str(e):
                st.error("Email not confirmed. Please check your inbox to verify your email.")
            else:
                st.error(f"Login failed: {e}")

def signup_ui():
    st.header("Register")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        result = auth.signup(email, password)
        if result.user:
            st.success("Registration successful! Please check your email to verify account before logging in.")
        else:
            st.error("Failed to register. Please try again.")

def main_ui():
    st.title("SMART BILLING SYSTEM")
    user = st.session_state.get('user', None)
    if not user:
        tab = st.radio("Choose", ["Login", "Register"])
        if tab == "Login":
            login_ui()
        else:
            signup_ui()
        return

    st.sidebar.write(f"Logged in as: {user.email}")
    page = st.sidebar.selectbox("Navigate", [
        "Display Menu",
        "Menu Management",
        "Place Order",
        "Generate Bill",
        "Display Customers",
        "Customer Management",
        "Settings"
    ])

    if page == "Display Menu":
        display_menu.run(user.id)
    elif page == "Menu Management":
        menu_management.run(user.id)
    elif page == "Place Order":
        place_order.run(user.id)
    elif page == "Generate Bill":
        generate_bill.run(user.id)
    elif page == "Display Customers":
        display_customers.run(user.id)
    elif page == "Customer Management":
        customer_management.run(user.id)
    elif page == "Settings":
        settings.run(user)

    if st.sidebar.button("Logout"):
        auth.logout()
        st.session_state.pop('user', None)
        safe_rerun()  # safe rerun workaround after logout

if __name__ == "__main__":
    main_ui()
