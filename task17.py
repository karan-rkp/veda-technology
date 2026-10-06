# ==========================================
# BANK ACCOUNT SIMULATOR
# Python Programming Track - Task 17
# ==========================================


# ------------------------------------------
# SHOW BALANCE
# ------------------------------------------
def check_balance(account):
    print("\n========== ACCOUNT BALANCE ==========")
    print(f"Account Holder : {account['name']}")
    print(f"Account Number : {account['account_number']}")
    print(f"Current Balance: ₹{account['balance']:.2f}")


# ------------------------------------------
# DEPOSIT MONEY
# ------------------------------------------
def deposit(account, transactions):

    print("\n========== DEPOSIT MONEY ==========")

    try:
        amount = float(input("Enter amount to deposit: ₹"))

        if amount <= 0:
            print("❌ Amount must be greater than 0.")
            return

        account["balance"] += amount

        transactions.append({
            "type": "Deposit",
            "amount": amount,
            "balance": account["balance"]
        })

        print(f"✅ ₹{amount:.2f} deposited successfully.")
        print(f"New Balance: ₹{account['balance']:.2f}")

    except ValueError:
        print("❌ Please enter a valid amount.")


# ------------------------------------------
# WITHDRAW MONEY
# ------------------------------------------
def withdraw(account, transactions):

    print("\n========== WITHDRAW MONEY ==========")

    try:
        amount = float(input("Enter amount to withdraw: ₹"))

        if amount <= 0:
            print("❌ Amount must be greater than 0.")
            return

        # Prevent withdrawal greater than balance
        if amount > account["balance"]:
            print("❌ Insufficient balance.")
            print(f"Available Balance: ₹{account['balance']:.2f}")
            return

        account["balance"] -= amount

        transactions.append({
            "type": "Withdrawal",
            "amount": amount,
            "balance": account["balance"]
        })

        print(f"✅ ₹{amount:.2f} withdrawn successfully.")
        print(f"Remaining Balance: ₹{account['balance']:.2f}")

    except ValueError:
        print("❌ Please enter a valid amount.")


# ------------------------------------------
# TRANSACTION HISTORY
# ------------------------------------------
def show_transactions(transactions):

    print("\n========== TRANSACTION HISTORY ==========")

    if not transactions:
        print("📭 No transactions available.")
        return

    print("-" * 60)
    print(f"{'No.':<6}{'Type':<18}{'Amount':<15}{'Balance':<15}")
    print("-" * 60)

    for index, transaction in enumerate(transactions, start=1):

        print(
            f"{index:<6}"
            f"{transaction['type']:<18}"
            f"₹{transaction['amount']:<14.2f}"
            f"₹{transaction['balance']:<14.2f}"
        )

    print("-" * 60)


# ------------------------------------------
# ACCOUNT DETAILS
# ------------------------------------------
def show_account_details(account):

    print("\n========== ACCOUNT DETAILS ==========")

    print(f"Account Holder : {account['name']}")
    print(f"Account Number : {account['account_number']}")
    print(f"Account Type   : {account['account_type']}")
    print(f"Balance        : ₹{account['balance']:.2f}")


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    # Account information
    account = {
        "name": "Karan",
        "account_number": "ACC1001",
        "account_type": "Savings",
        "balance": 5000.00
    }

    # Transaction history
    transactions = []

    print("\n==========================================")
    print("        🏦 BANK ACCOUNT SIMULATOR")
    print("==========================================")
    print(f"Welcome, {account['name']}!")

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Account Details")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transaction History")
        print("6. Exit")
        print("===============================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            show_account_details(account)

        elif choice == "2":
            check_balance(account)

        elif choice == "3":
            deposit(account, transactions)

        elif choice == "4":
            withdraw(account, transactions)

        elif choice == "5":
            show_transactions(transactions)

        elif choice == "6":
            print("\n👋 Thank you for using Bank Account Simulator!")
            print(f"Final Balance: ₹{account['balance']:.2f}")
            break

        else:
            print("❌ Invalid choice. Please select 1-6.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()