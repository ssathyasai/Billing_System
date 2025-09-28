# 💳 Smart Billing System

A **command-line billing app** built with Python 🐍 + Supabase ☁️.
Manage menu, customers, and carts — and generate **instant bills with auto GST (5%)**.

---

## ✨ Features

* Manage **Menu** (add/update/delete items)
* Manage **Customers**
* Add items to **Cart** & place orders
* **Auto GST** + nicely formatted printable bills 🧾
* Cloud database powered by **Supabase**

---

## 📂 Project Structure

```
smart-billing/
├── .env        # Supabase credentials  
├── run.py      # Entry point  
└── src/  
    ├── cli/    # CLI menus  
    ├── config/ # Supabase setup  
    ├── dao/    # Database access  
    └── service/# Billing logic  
```

---

## 🗄️ Database Tables (Supabase)

The system uses **three main tables**:

* **menu** → `item_id` (PK), `item_name`, `item_price`
* **customer** → `cust_id` (PK), `cust_name`, `mobile`, `date_of_shopping`, `total_amount`
* **cart** → `cart_id` (PK), `cust_id` (FK → customer), `item_id` (FK → menu), `quantity`

**Relations:**

* A customer can have many cart items
* Cart links customers ↔ menu items
* Bills (shopping date & total amount) are stored in the customer table

---

## 🚀 Quick Start

1. Clone the repo

   ```bash
   git clone <repo-url>
   cd smart-billing
   ```

2. Setup environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Add `.env` file with your Supabase keys:

   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_api_key
   ```

4. Run the app

   ```bash
   python run.py
   ```

---

## 📜 License

MIT License

---

## 📧 Contact

For feedback or questions: **[your email/contact]** 🚀
