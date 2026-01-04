import streamlit as st
import json
from pathlib import Path
import random
import string

# ===================== CONFIG =====================
st.set_page_config(page_title="MyBank", page_icon="🏦", layout="centered")
st.title("🏦 MyBank - Simple Banking System")

DATABASE = "database.json"

# ===================== DATA HANDLING =====================
def load_data():
    if Path(DATABASE).exists():
        try:
            with open(DATABASE, "r") as f:
                content = f.read()
                return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=5)
    digits = random.choices(string.digits, k=4)
    chars = alpha + digits
    random.shuffle(chars)
    return "".join(chars)

# ===================== SESSION STATE =====================
if "bank_data" not in st.session_state:
    st.session_state.bank_data = load_data()

data = st.session_state.bank_data

# ===================== HELPER FUNCTION =====================
def find_user(acc_no, pin):
    for user in data:
        if user["account_no"] == acc_no and user["pin"] == pin:
            return user
    return None

# ===================== SIDEBAR MENU =====================
st.sidebar.title("Menu")
choice = st.sidebar.selectbox(
    "Choose Action",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "View Details",
        "Update Details",
        "Delete Account"
    ]
)

# ===================== CREATE ACCOUNT =====================
if choice == "Create Account":
    st.header("🆕 Create New Account")

    with st.form("create_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number (10 digits)")
        pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Create Account")

        if submitted:
            if not all([name, email, phone, pin]):
                st.error("All fields are required!")
            elif not phone.isdigit() or len(phone) != 10:
                st.error("Phone number must be exactly 10 digits")
            elif not pin.isdigit() or len(pin) != 4:
                st.error("PIN must be exactly 4 digits")
            else:
                acc_no = generate_account_no()
                new_user = {
                    "name": name,
                    "email": email,
                    "phone": int(phone),
                    "pin": int(pin),
                    "account_no": acc_no,
                    "balance": 0
                }
                data.append(new_user)
                save_data(data)
                st.session_state.bank_data = data
                st.success("Account Created Successfully!")
                st.info(f"Your Account Number: **{acc_no}**")
                st.balloons()

# ===================== DEPOSIT MONEY =====================
elif choice == "Deposit Money":
    st.header("💰 Deposit Money")

    with st.form("deposit_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount (₹)", min_value=1, max_value=10000, step=1)

        submitted = st.form_submit_button("Deposit")

        if submitted:
            if not pin.isdigit() or len(pin) != 4:
                st.error("Invalid PIN")
            else:
                user = find_user(acc_no, int(pin))
                if not user:
                    st.error("Invalid Account Number or PIN")
                else:
                    user["balance"] += int(amount)
                    save_data(data)
                    st.success(f"₹{int(amount)} deposited successfully!")
                    st.write(f"New Balance: ₹{user['balance']}")

# ===================== WITHDRAW MONEY =====================
elif choice == "Withdraw Money":
    st.header("💸 Withdraw Money")

    with st.form("withdraw_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount (₹)", min_value=1, max_value=10000, step=1)

        submitted = st.form_submit_button("Withdraw")

        if submitted:
            if not pin.isdigit() or len(pin) != 4:
                st.error("Invalid PIN")
            else:
                user = find_user(acc_no, int(pin))
                if not user:
                    st.error("Invalid Account Number or PIN")
                elif int
