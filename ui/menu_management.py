import streamlit as st
from src.config.supabase_config import SupabaseConfig
from src.dao.menu_dao import MenuDAO

def run(owner_id: str):
    st.header("Menu Management")
    client = SupabaseConfig().get_client()
    menu_dao = MenuDAO(client)

    action = st.radio("Action", ["Add Item", "Update Item", "Delete Item"])

    if action == "Add Item":
        name = st.text_input("New Item Name")
        price = st.number_input("Item Price", min_value=0.0, format="%.2f")
        if st.button("Add Item"):
            try:
                menu_dao.add_item(owner_id, name, price)
                st.success("Item added.")
            except Exception as e:
                st.error(f"Failed to add item: {e}")

    elif action == "Update Item":
        items = menu_dao.get_all_items(owner_id)
        if not items:
            st.info("No items to update.")
            return
        idx = st.selectbox("Select Item", range(len(items)), format_func=lambda i: items[i]['item_name'])
        item = items[idx]
        new_name = st.text_input("New Name", value=item['item_name'])
        new_price = st.number_input("New Price", min_value=0.0, value=float(item['item_price']), format="%.2f")
        if st.button("Update Item"):
            try:
                menu_dao.update_item(owner_id, item['item_id'], new_name, new_price)
                st.success("Item updated.")
            except Exception as e:
                st.error(f"Failed to update item: {e}")

    elif action == "Delete Item":
        items = menu_dao.get_all_items(owner_id)
        if not items:
            st.info("No items to delete.")
            return
        idx = st.selectbox("Select Item", range(len(items)), format_func=lambda i: items[i]['item_name'])
        item = items[idx]
        if st.button("Delete Item"):
            try:
                menu_dao.delete_item(owner_id, item['item_id'])
                st.success("Item deleted.")
            except Exception as e:
                st.error(f"Failed to delete item: {e}")
