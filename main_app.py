import streamlit as st

st.title("SMART BILLING SYSTEM")

page = st.sidebar.selectbox("Navigate", [
    "Display Menu",
    "Menu Management",
    "Place Order",
    "Generate Bill",
    "Display Customers",
    "Customer Management"
])

if page == "Display Menu":
    import display_menu
    display_menu.run()

elif page == "Menu Management":
    import menu_management
    menu_management.run()

elif page == "Place Order":
    import place_order
    place_order.run()

elif page == "Generate Bill":
    import generate_bill
    generate_bill.run()

elif page == "Display Customers":
    import display_customers
    display_customers.run()

elif page == "Customer Management":
    import customer_management
    customer_management.run()
