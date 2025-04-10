def sort_user_input_numbers():
    """
    Accepts space-separated integers from the user, sorts them, and prints the result.
    """
    try:
        user_input = input("🔢 Enter numbers separated by spaces: ")
        numbers = list(map(int, user_input.split()))

        sorted_numbers = sorted(numbers)

        print("\n📋 Results:")
        print("➡️ Original list:", numbers)
        print("✅ Sorted list:  ", sorted_numbers)

    except ValueError:
        print("❌ Invalid input. Please enter only integers separated by spaces.")

# Run the function
if __name__ == "__main__":
    sort_user_input_numbers()
