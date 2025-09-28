💳 Smart Billing System

A Streamlit-based billing app built with Python 🐍 + Supabase ☁️.
Manage menu, customers, and carts — and generate instant bills with auto GST (5%).

✨ Features

Manage Menu (add/update/delete items)

Manage Customers

Add items to Cart & place orders

Generate Printable Bills with Auto GST

Cloud database powered by Supabase

📂 Project Structure
smart_billing_app/
├── main_app.py                    # Main Streamlit dashboard
├── display_menu.py                # Display menu UI
├── menu_management.py             # Menu management UI
├── place_order.py                 # Place order UI
├── generate_bill.py               # Bill generation UI
├── display_customers.py           # Customer display UI
├── customer_management.py         # Customer management UI
└── src/                           # Backend logic
    ├── config/
    │   └── supabase_config.py     # Supabase setup
    ├── dao/                       # Database access
    │   ├── menu_dao.py
    │   ├── customer_dao.py
    │   ├── cart_dao.py
    └── service/
        └── billing_service.py     # Billing logic


Explanation:

UI Files: Streamlit pages for user interactions

src/config/: Database connection & credentials

src/dao/: CRUD operations for menu, customer & cart

src/service/: Business logic for billing

🗄️ Database Tables (Supabase)

The system uses three main tables:

menu → item_id (PK), item_name, item_price

customer → cust_id (PK), cust_name, mobile, date_of_shopping, total_amount

cart → cart_id (PK), cust_id (FK → customer), item_id (FK → menu), quantity

Relations:

A customer can have many cart items

Cart links customers ↔ menu items

Bills (shopping date & total amount) are stored in the customer table

🚀 Quick Start

Clone the repo

git clone "https://github.com/ssathyasai/Billing_System.git"
cd smart_billing_app


Setup environment

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt


Add .env file with your Supabase keys:

SUPABASE_URL=your_project_url
SUPABASE_KEY=your_api_key


Run the app

streamlit run main_app.py

📜 License

MIT License

📧 Contact

For feedback or questions: sathyasai1357@gmail.com 🚀