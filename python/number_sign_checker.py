def check_number_sign():
    try:
        number = float(input("🔢 Enter a number: "))
        print(f"The number is {number}")

        if number < 0:
            print("➖ It is a Negative number.")
        elif number > 0:
            print("➕ It is a Positive number.")
        else:
            print("🟰 It is Zero.")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

# Run the function
if __name__ == "__main__":
    check_number_sign()
