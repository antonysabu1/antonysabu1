def factorial_recursive(n):
    """
    Calculate the factorial of a non-negative integer using recursion.
    
    Parameters:
    n (int): A non-negative integer
    
    Returns:
    int: Factorial of n if valid
    str: Error message if n is negative
    """
    if n < 0:
        return "Error: Factorial cannot be a negative number."
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)

def main():
    try:
        user_input = input("Enter a non-negative integer to compute its factorial: ")
        n = int(user_input)

        result = factorial_recursive(n)

        if isinstance(result, str):
            # Handles error message returned from function
            print(result)
        else:
            print(f"The factorial of {n} is {result}")
    except ValueError:
        print("Invalid input. Please enter an integer number.")

# Run the program
if __name__ == "__main__":
    main()
