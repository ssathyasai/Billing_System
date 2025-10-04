import streamlit as st
from src.dao.customer_dao import CustomerDAO
from src.config.supabase_config import SupabaseConfig

def run(owner_id: str):
    st.header("Customer Management")
    client = SupabaseConfig().get_client()
    customer_dao = CustomerDAO(client)

    action = st.radio("Action", ["Add Customer", "Update Customer", "Delete Customer"])

    if action == "Add Customer":
        name = st.text_input("Customer Name")
        mobile = st.text_input("Mobile Number")
        if st.button("Add Customer"):
            try:
                customer_dao.add_customer(owner_id, name, mobile)
                st.success("Customer added.")
            except Exception as e:
                st.error(f"Failed to add customer: {e}")

    elif action == "Update Customer":
        customers = customer_dao.get_all_customers(owner_id)
        if not customers:
            st.info("No customers to update.")
            return
        idx = st.selectbox("Select Customer", range(len(customers)), format_func=lambda i: customers[i]['cust_name'])
        cust = customers[idx]
        new_name = st.text_input("New Name", value=cust['cust_name'])
        new_mobile = st.text_input("New Mobile", value=cust.get('mobile', ''))
        if st.button("Update Customer"):
            try:
                customer_dao.update_customer(owner_id, cust['cust_id'], new_name, new_mobile)
                st.success("Customer updated.")
            except Exception as e:
                st.error(f"Failed to update customer: {e}")

    elif action == "Delete Customer":
        customers = customer_dao.get_all_customers(owner_id)
        if not customers:
            st.info("No customers to delete.")
            return
        idx = st.selectbox("Select Customer", range(len(customers)), format_func=lambda i: customers[i]['cust_name'])
        cust = customers[idx]
        if st.button("Delete Customer"):
            try:
                # clear_cart is handled separately if needed
                from src.dao.cart_dao import CartDAO
                cart_dao = CartDAO(client)
                cart_dao.clear_cart(owner_id, cust['cust_id'])
                customer_dao.delete_customer(owner_id, cust['cust_id'])
                st.success("Customer and related cart items deleted.")
            except Exception as e:
                st.error(f"Failed to delete customer: {e}")
