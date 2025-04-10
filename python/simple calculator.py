def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "❌ Error: Division by zero is not allowed."
    return x / y

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def calculator():
    print("🧮 Welcome to the Smart Calculator!")
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Enter new numbers")
        print("2. Perform operations")
        print("3. Exit")

        main_choice = input("Choose an option (1/2/3): ").strip()

        if main_choice == '1':
            num1 = get_number("Enter the first number: ")
            num2 = get_number("Enter the second number: ")

        elif main_choice == '2':
            if 'num1' not in locals() or 'num2' not in locals():
                print("⚠️ Please enter numbers first (option 1).")
                continue

            print("\n🧮 Operations Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Back to Main Menu")

            choice = input("Choose an operation (1/2/3/4/5): ").strip()

            if choice == '1':
                print(f"\n✅ Result: {num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"\n✅ Result: {num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"\n✅ Result: {num1} × {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"\n✅ Result: {num1} ÷ {num2} = {result}")
            elif choice == '5':
                continue
            else:
                print("❌ Invalid operation choice.")

        elif main_choice == '3':
            print("👋 Exiting the calculator. Goodbye!")
            break
        else:
            print("❌ Invalid menu option.")

# Run the calculator
if __name__ == "__main__":
    calculator()
