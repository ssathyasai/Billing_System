import streamlit as st
from src.config.supabase_config import SupabaseConfig
from src.dao.customer_dao import CustomerDAO
from src.service.billing_service import BillingService
from src.dao.menu_dao import MenuDAO
from src.dao.cart_dao import CartDAO

def run(owner_id: str):
    st.header("Generate Bill")
    client = SupabaseConfig().get_client()
    customer_dao = CustomerDAO(client)
    menu_dao = MenuDAO(client)
    cart_dao = CartDAO(client)
    billing_service = BillingService(menu_dao, cart_dao, customer_dao)

    customers = customer_dao.get_all_customers(owner_id)
    if not customers:
        st.info("No customers available.")
        return

    cust_choice = st.selectbox("Select Customer", [c['cust_name'] for c in customers])
    cust = next(c for c in customers if c['cust_name'] == cust_choice)

    if st.button("Generate Bill"):
        try:
            bill = billing_service.calculate_bill(owner_id, cust['cust_id'])
            print_bill_formatted(bill)
            billing_service.clear_customer_cart(owner_id, cust['cust_id'])
        except Exception as e:
            st.error(f"Could not generate bill: {e}")

def print_bill_formatted(bill: dict):
    st.text("="*50)
    st.text(" " * 15 + "SMART BILLING")
    st.text("="*50)
    st.text(f"{'S.No':<5} {'Item':<20} {'Qty':<5} {'Price':>10} {'Total':>10}")
    st.text("-"*50)
    for idx, item in enumerate(bill['items'], start=1):
        st.text(f"{idx:<5} {item['item_name']:<20} {item['qty']:<5} "
                f"{item['price_per_item']:>10.2f} {item['total_price']:>10.2f}")
    st.text("-"*50)
    st.text(f"{'Subtotal:':>40} {bill['subtotal']:>10.2f}")
    st.text(f"{'GST (5%):':>40} {bill['gst']:>10.2f}")
    st.text(f"{'TOTAL:':>40} {bill['total']:>10.2f}")
    st.text("="*50)
    st.text(" " * 12 + "THANK YOU! VISIT AGAIN")
    st.text("="*50)
