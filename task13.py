# ==========================================
# PRIME NUMBER ANALYZER
# Python Programming Track
# ==========================================


# ------------------------------------------
# PRIME NUMBER CHECKER
# ------------------------------------------
def is_prime(number):

    # Numbers less than 2 are not prime
    if number < 2:
        return False

    # Check divisibility
    for i in range(2, int(number ** 0.5) + 1):

        if number % i == 0:
            return False

    return True


# ------------------------------------------
# GENERATE PRIME NUMBERS IN RANGE
# ------------------------------------------
def generate_primes(start, end):

    primes = []

    for number in range(start, end + 1):

        if is_prime(number):
            primes.append(number)

    return primes


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("          PRIME NUMBER ANALYZER")
    print("==========================================")

    # Check a single number
    number = int(input("\nEnter a number to check: "))

    if is_prime(number):
        print(f"✅ {number} is a PRIME number.")
    else:
        print(f"❌ {number} is NOT a prime number.")

    # Generate primes
    print("\n------------------------------------------")
    print("       PRIME NUMBER RANGE GENERATOR")
    print("------------------------------------------")

    start = int(input("Enter starting number: "))
    end = int(input("Enter ending number: "))

    if start > end:
        print("❌ Starting number cannot be greater than ending number.")
        return

    primes = generate_primes(start, end)

    print(f"\nPrime numbers from {start} to {end}:")

    if primes:
        print(primes)
        print(f"\nTotal prime numbers: {len(primes)}")
    else:
        print("No prime numbers found in this range.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()