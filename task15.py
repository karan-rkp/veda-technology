# ==========================================
# SHOPPING BILL GENERATOR
# Python Programming Track - Task 15
# ==========================================


# ------------------------------------------
# ADD PRODUCT
# ------------------------------------------
def add_product(products):

    print("\n---------- ADD PRODUCT ----------")

    name = input("Enter product name: ").strip()

    if not name:
        print("❌ Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per item: "))

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return

        if price < 0:
            print("❌ Price cannot be negative.")
            return

        product = {
            "name": name,
            "quantity": quantity,
            "price": price
        }

        products.append(product)

        print("✅ Product added successfully!")

    except ValueError:
        print("❌ Please enter valid numbers.")


# ------------------------------------------
# CALCULATE SUBTOTAL
# ------------------------------------------
def calculate_subtotal(products):

    subtotal = 0

    for product in products:
        subtotal += product["quantity"] * product["price"]

    return subtotal


# ------------------------------------------
# CALCULATE DISCOUNT
# ------------------------------------------
def calculate_discount(subtotal):

    # Discount rules
    if subtotal >= 5000:
        discount_rate = 10
    elif subtotal >= 2000:
        discount_rate = 5
    else:
        discount_rate = 0

    discount = subtotal * discount_rate / 100

    return discount, discount_rate


# ------------------------------------------
# CALCULATE TAX
# ------------------------------------------
def calculate_tax(amount):

    tax_rate = 18
    tax = amount * tax_rate / 100

    return tax, tax_rate


# ------------------------------------------
# GENERATE BILL
# ------------------------------------------
def generate_bill(products):

    if not products:
        print("\n❌ No products added.")
        return

    subtotal = calculate_subtotal(products)

    discount, discount_rate = calculate_discount(subtotal)

    amount_after_discount = subtotal - discount

    tax, tax_rate = calculate_tax(amount_after_discount)

    final_amount = amount_after_discount + tax

    print("\n")
    print("=" * 65)
    print("                    SHOPPING BILL")
    print("=" * 65)

    print(f"{'Product':<20}{'Qty':<10}{'Price':<15}{'Total':<15}")
    print("-" * 65)

    for product in products:

        total = product["quantity"] * product["price"]

        print(
            f"{product['name']:<20}"
            f"{product['quantity']:<10}"
            f"₹{product['price']:<14.2f}"
            f"₹{total:<14.2f}"
        )

    print("-" * 65)

    print(f"{'Subtotal':<50} ₹{subtotal:.2f}")
    print(f"{'Discount (' + str(discount_rate) + '%)':<50} -₹{discount:.2f}")
    print(f"{'Amount After Discount':<50} ₹{amount_after_discount:.2f}")
    print(f"{'Tax (' + str(tax_rate) + '%)':<50} ₹{tax:.2f}")

    print("=" * 65)
    print(f"{'FINAL AMOUNT':<50} ₹{final_amount:.2f}")
    print("=" * 65)

    print("\nThank you for shopping! 😊")


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    products = []

    print("\n==========================================")
    print("       🛒 SHOPPING BILL GENERATOR")
    print("==========================================")

    while True:

        print("\n---------- MENU ----------")
        print("1. Add Product")
        print("2. Generate Bill")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":

            add_product(products)

        elif choice == "2":

            generate_bill(products)

        elif choice == "3":

            print("\n👋 Thank you for using Shopping Bill Generator!")
            break

        else:

            print("❌ Invalid choice. Please select 1-3.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()