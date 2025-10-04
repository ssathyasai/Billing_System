# 💼 SMART BILLING SYSTEM

A simple **multi-user billing system** built with **Streamlit** and **Supabase**.  
Manage your menu, customers, orders, and generate bills with GST calculation. Each user sees only their own data.

---

## 🚀 Features

- User registration and login (Supabase Auth)  
- Menu and customer management  
- Place orders with live cart  
- Auto GST calculation on bills  
- Business name displayed on bills  
- User settings: update details, logout  

---

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/Billing_System.git
cd Billing_System

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run ui/main_app.py
```

Create a `.env` file with:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

---

## 📁 Project Structure

```
billing_system/
├── src/                  # Backend logic
│   ├── auth.py
│   ├── config/
│   ├── dao/
│   └── service/
├── ui/                   # Streamlit pages
├── requirements.txt
└── README.md
```

---

## 📞 Contact

**Developer:** Sathyasai

📧 Email: sathyasai1357@gmail.com  


---

✅ *Simple. Secure. Smart Billing.*
