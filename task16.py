# ==========================================
# EMPLOYEE SALARY CALCULATOR
# Python Programming Track - Task 16
# ==========================================


# ------------------------------------------
# SALARY RULES
# ------------------------------------------

SALARY_RULES = {
    "hra_rate": 20,       # 20% of basic salary
    "da_rate": 10,        # 10% of basic salary
    "pf_rate": 12,        # 12% of basic salary

    # Tax rates based on gross salary
    "tax_rules": [
        (50000, 10),
        (30000, 5),
        (0, 0)
    ]
}


# ------------------------------------------
# GET TAX RATE
# ------------------------------------------
def get_tax_rate(gross_salary):

    for minimum_salary, tax_rate in SALARY_RULES["tax_rules"]:

        if gross_salary >= minimum_salary:
            return tax_rate

    return 0


# ------------------------------------------
# CALCULATE SALARY
# ------------------------------------------
def calculate_salary(basic_salary):

    # Allowances
    hra = basic_salary * SALARY_RULES["hra_rate"] / 100
    da = basic_salary * SALARY_RULES["da_rate"] / 100

    # Gross salary
    gross_salary = basic_salary + hra + da

    # PF deduction
    pf = basic_salary * SALARY_RULES["pf_rate"] / 100

    # Tax
    tax_rate = get_tax_rate(gross_salary)
    tax = gross_salary * tax_rate / 100

    # Total deductions
    total_deductions = pf + tax

    # Net salary
    net_salary = gross_salary - total_deductions

    return {
        "basic_salary": basic_salary,
        "hra": hra,
        "da": da,
        "gross_salary": gross_salary,
        "pf": pf,
        "tax_rate": tax_rate,
        "tax": tax,
        "total_deductions": total_deductions,
        "net_salary": net_salary
    }


# ------------------------------------------
# DISPLAY SALARY SLIP
# ------------------------------------------
def display_salary_slip(employee, salary):

    print("\n")
    print("=" * 55)
    print("              EMPLOYEE SALARY SLIP")
    print("=" * 55)

    print(f"Employee ID   : {employee['id']}")
    print(f"Employee Name : {employee['name']}")
    print(f"Department    : {employee['department']}")

    print("-" * 55)

    print(f"Basic Salary  : ₹{salary['basic_salary']:,.2f}")
    print(f"HRA           : ₹{salary['hra']:,.2f}")
    print(f"DA            : ₹{salary['da']:,.2f}")

    print("-" * 55)

    print(f"Gross Salary  : ₹{salary['gross_salary']:,.2f}")

    print("\nDEDUCTIONS")
    print("-" * 55)

    print(f"PF            : ₹{salary['pf']:,.2f}")
    print(
        f"Income Tax ({salary['tax_rate']}%)"
        f" : ₹{salary['tax']:,.2f}"
    )

    print(f"Total Deduction: ₹{salary['total_deductions']:,.2f}")

    print("=" * 55)
    print(f"NET SALARY    : ₹{salary['net_salary']:,.2f}")
    print("=" * 55)


# ------------------------------------------
# GET EMPLOYEE DETAILS
# ------------------------------------------
def get_employee_details():

    print("\n========== EMPLOYEE DETAILS ==========")

    employee_id = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()

    while True:

        try:
            basic_salary = float(input("Enter Basic Salary: ₹"))

            if basic_salary <= 0:
                print("❌ Salary must be greater than 0.")
                continue

            break

        except ValueError:
            print("❌ Please enter a valid salary.")

    employee = {
        "id": employee_id,
        "name": name,
        "department": department
    }

    return employee, basic_salary


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
def main():

    print("\n==========================================")
    print("       EMPLOYEE SALARY CALCULATOR")
    print("==========================================")

    employee, basic_salary = get_employee_details()

    salary = calculate_salary(basic_salary)

    display_salary_slip(employee, salary)


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()