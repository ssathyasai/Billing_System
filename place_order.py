import streamlit as st
from src.config.supabase_config import SupabaseConfig
from src.dao.menu_dao import MenuDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.cart_dao import CartDAO

def run():
    st.header("Place Order")
    config = SupabaseConfig()
    client = config.get_client()
    menu_dao = MenuDAO(client)
    customer_dao = CustomerDAO(client)
    cart_dao = CartDAO(client)

    items = menu_dao.get_all_items()
    if not items:
        st.info("Menu is empty.")
        return

    st.subheader("Select Items and Quantities")
    order = {}
    for item in items:
        qty = st.number_input(f"{item['item_name']} (Price: {item['item_price']})", min_value=0, step=1, key=f"qty_{item['item_id']}")
        if qty > 0:
            order[item['item_id']] = qty

    customers = customer_dao.get_all_customers()
    cust_options = [f"{c['cust_name']} (Mobile: {c.get('mobile', '')})" for c in customers]
    cust_options.append("Add New Customer")
    cust_choice = st.selectbox("Select Customer", cust_options)

    new_cust_name = None
    new_cust_mobile = None
    if cust_choice == "Add New Customer":
        new_cust_name = st.text_input("New Customer Name")
        new_cust_mobile = st.text_input("New Customer Mobile")

    if st.button("Place Order"):
        if not order:
            st.warning("No items selected.")
            return
        try:
            if cust_choice == "Add New Customer":
                if not new_cust_name:
                    st.error("Customer name required.")
                    return
                cust_id = customer_dao.add_customer(new_cust_name, new_cust_mobile or "")
            else:
                idx = cust_options.index(cust_choice)
                cust_id = customers[idx]['cust_id']
            for item_id, qty in order.items():
                cart_dao.add_to_cart(cust_id, item_id, qty)
            st.success("Order placed.")
        except Exception as e:
            st.error(f"Error placing order: {e}")
