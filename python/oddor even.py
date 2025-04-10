def is_even(number):
    return number % 2 == 0

def main():
    print("🔢 Even or Odd Checker")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter an integer number: ").strip()

        if user_input.lower() == "exit":
            print("\n👋 Exiting the program. Goodbye!")
            break

        if user_input.lstrip('-').isdigit():
            number = int(user_input)
            if is_even(number):
                print(f"✅ {number} is Even.\n")
            else:
                print(f"🔹 {number} is Odd.\n")
        else:
            print("❌ Invalid input. Please enter a valid integer or type 'exit' to quit.\n")

# Run the program
if __name__ == "__main__":
    main()
