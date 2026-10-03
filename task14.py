# ==========================================
# TEMPERATURE CONVERTER
# Python Programming Track - Task 14
# ==========================================


# ------------------------------------------
# CELSIUS CONVERSIONS
# ------------------------------------------
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def celsius_to_kelvin(celsius):
    return celsius + 273.15


# ------------------------------------------
# FAHRENHEIT CONVERSIONS
# ------------------------------------------
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15


# ------------------------------------------
# KELVIN CONVERSIONS
# ------------------------------------------
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("        🌡️ TEMPERATURE CONVERTER")
    print("==========================================")

    print("\nSelect the input temperature unit:")
    print("1. Celsius")
    print("2. Fahrenheit")
    print("3. Kelvin")

    choice = input("\nEnter your choice (1-3): ").strip()

    # --------------------------------------
    # INPUT VALIDATION
    # --------------------------------------
    if choice not in ["1", "2", "3"]:
        print("❌ Invalid choice!")
        return

    try:
        temperature = float(input("Enter temperature: "))
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    # --------------------------------------
    # CELSIUS
    # --------------------------------------
    if choice == "1":

        if temperature < -273.15:
            print("❌ Temperature cannot be below absolute zero.")
            return

        fahrenheit = celsius_to_fahrenheit(temperature)
        kelvin = celsius_to_kelvin(temperature)

        print("\n========== RESULT ==========")
        print(f"Celsius    : {temperature:.2f} °C")
        print(f"Fahrenheit : {fahrenheit:.2f} °F")
        print(f"Kelvin     : {kelvin:.2f} K")


    # --------------------------------------
    # FAHRENHEIT
    # --------------------------------------
    elif choice == "2":

        if temperature < -459.67:
            print("❌ Temperature cannot be below absolute zero.")
            return

        celsius = fahrenheit_to_celsius(temperature)
        kelvin = fahrenheit_to_kelvin(temperature)

        print("\n========== RESULT ==========")
        print(f"Fahrenheit : {temperature:.2f} °F")
        print(f"Celsius    : {celsius:.2f} °C")
        print(f"Kelvin     : {kelvin:.2f} K")


    # --------------------------------------
    # KELVIN
    # --------------------------------------
    elif choice == "3":

        if temperature < 0:
            print("❌ Kelvin temperature cannot be negative.")
            return

        celsius = kelvin_to_celsius(temperature)
        fahrenheit = kelvin_to_fahrenheit(temperature)

        print("\n========== RESULT ==========")
        print(f"Kelvin     : {temperature:.2f} K")
        print(f"Celsius    : {celsius:.2f} °C")
        print(f"Fahrenheit : {fahrenheit:.2f} °F")

    print("============================")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()