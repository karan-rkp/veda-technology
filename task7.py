import secrets
import string


def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):

    character_sets = []

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_numbers:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append("!@#$%^&*()-_=+[]{}?")

    if not character_sets:
        return None

    if length < len(character_sets):
        return None

    # At least one character from every selected category
    password = [
        secrets.choice(characters)
        for characters in character_sets
    ]

    # Remaining characters
    all_characters = "".join(character_sets)

    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    # Secure shuffle
    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return "".join(password)


print("=" * 40)
print("       🔐 PASSWORD GENERATOR")
print("=" * 40)

length = int(input("Enter password length: "))

uppercase = input("Include uppercase letters? (y/n): ").lower() == "y"
lowercase = input("Include lowercase letters? (y/n): ").lower() == "y"
numbers = input("Include numbers? (y/n): ").lower() == "y"
symbols = input("Include symbols? (y/n): ").lower() == "y"

password = generate_password(
    length,
    uppercase,
    lowercase,
    numbers,
    symbols
)

if password:
    print("\n" + "=" * 40)
    print("Generated Password:")
    print(password)
    print("=" * 40)
else:
    print("\n❌ Invalid options.")
    print("Select at least one character type and use a sufficient length.")