from pathlib import Path
import json
import random
import string


class Bank:
    database = "database.json"
    data = []

    # Load data from file
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                content = fs.read()
                data = json.loads(content) if content else []
        except Exception as err:
            print(f"Error loading database: {err}")
    else:
        with open(database, "w") as fs:
            json.dump([], fs)

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @staticmethod
    def _accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        acc = alpha + digits
        random.shuffle(acc)
        return "".join(acc)

    def create_account(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        pin = input("Enter your 4-digit pin: ")

        if not phone.isdigit() or len(phone) != 10:
            print("Invalid phone number!")
            return

        if not pin.isdigit() or len(pin) != 4:
            print("Invalid pin!")
            return

        account = {
            "name": name,
            "email": email,
            "phone": int(phone),
            "pin": int(pin),
            "account_no": Bank._accountno(),
            "balance": 0
        }

        Bank.data.append(account)
        Bank.__update()
        print(f"Account created successfully!")
        print(f"Your Account Number: {account['account_no']}")

    def deposite_money(self):
        acc = input("Enter account number: ")
        pin = int(input("Enter pin: "))

        user = next((i for i in Bank.data if i["account_no"] == acc and i["pin"] == pin), None)

        if not user:
            print("User not found!")
            return

        amount = int(input("Enter amount to deposit: "))
        if amount <= 0 or amount > 10000:
            print("Invalid amount!")
            return

        user["balance"] += amount
        Bank.__update()
        print("Amount deposited successfully!")

    def withdraw_money(self):
        acc = input("Enter account number: ")
        pin = int(input("Enter pin: "))

        user = next((i for i in Bank.data if i["account_no"] == acc and i["pin"] == pin), None)

        if not user:
            print("User not found!")
            return

        amount = int(input("Enter amount to withdraw: "))
        if amount <= 0 or amount > 10000:
            print("Invalid amount!")
        elif amount > user["balance"]:
            print("Insufficient balance!")
        else:
            user["balance"] -= amount
            Bank.__update()
            print("Amount withdrawn successfully!")

    def details(self):
        acc = input("Enter account number: ")
        pin = int(input("Enter pin: "))

        user = next((i for i in Bank.data if i["account_no"] == acc and i["pin"] == pin), None)

        if not user:
            print("User not found!")
            return

        for k, v in user.items():
            print(f"{k}: {v}")

    def update_details(self):
        acc = input("Enter account number: ")
        pin = int(input("Enter pin: "))

        user = next((i for i in Bank.data if i["account_no"] == acc and i["pin"] == pin), None)

        if not user:
            print("User not found!")
            return

        print("Press ENTER to skip a field")

        name = input("New name: ")
        email = input("New email: ")
        phone = input("New phone: ")
        new_pin = input("New pin: ")

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if phone and phone.isdigit() and len(phone) == 10:
            user["phone"] = int(phone)
        if new_pin and new_pin.isdigit() and len(new_pin) == 4:
            user["pin"] = int(new_pin)

        Bank.__update()
        print("Details updated successfully!")

    def delete_account(self):
        acc = input("Enter account number: ")
        pin = int(input("Enter pin: "))

        for i in Bank.data:
            if i["account_no"] == acc and i["pin"] == pin:
                Bank.data.remove(i)
                Bank.__update()
                print("Account deleted successfully!")
                return

        print("User not found!")


# ------------------ MAIN MENU ------------------

user = Bank()

print("\n--- BANK MANAGEMENT SYSTEM ---")
print("1. Create Account")
print("2. Deposit Money")
print("3. Withdraw Money")
print("4. View Account Details")
print("5. Update Account Details")
print("6. Delete Account")

choice = int(input("Enter your choice: "))

if choice == 1:
    user.create_account()
elif choice == 2:
    user.deposite_money()
elif choice == 3:
    user.withdraw_money()
elif choice == 4:
    user.details()
elif choice == 5:
    user.update_details()
elif choice == 6:
    user.delete_account()
else:
    print("Invalid choice!")
