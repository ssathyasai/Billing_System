import streamlit as st
import pandas as pd
from src.dao.customer_dao import CustomerDAO
from src.config.supabase_config import SupabaseConfig

def run(owner_id: str):
    st.header("Customers")
    client = SupabaseConfig().get_client()
    customer_dao = CustomerDAO(client)
    customers = customer_dao.get_all_customers(owner_id)
    if not customers:
        st.info("No customers found.")
        return
    df = pd.DataFrame([
        {
            "No.": idx+1,
            "Name": cust['cust_name'],
            "Mobile": cust.get('mobile', ''),
            "Date": cust.get('date_of_shopping', ''),
            "Total Amount": float(cust.get('total_amount', 0))
        }
        for idx, cust in enumerate(customers)
    ])
    st.table(df)
