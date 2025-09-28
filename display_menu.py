import streamlit as st
import pandas as pd
from src.config.supabase_config import SupabaseConfig
from src.dao.menu_dao import MenuDAO

def run():
    st.header("Menu Items")
    config = SupabaseConfig()
    client = config.get_client()
    menu_dao = MenuDAO(client)
    items = menu_dao.get_all_items()
    if not items:
        st.info("No items in menu.")
        return
    df = pd.DataFrame([
        {"No.": idx+1, "Item": item['item_name'], "Price": float(item['item_price'])}
        for idx, item in enumerate(items)
    ])
    st.table(df)
