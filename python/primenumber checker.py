def is_prime(n):
    """
    Check whether a number is prime using trial division.

    Parameters:
    n (int): Number to check.

    Returns:
    bool: True if prime, False otherwise.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    try:
        n = int(input("🔢 Enter the number: "))
        if is_prime(n):
            print(f"✅ {n} is a Prime number.")
        else:
            print(f"❌ {n} is Not a Prime number.")
    except ValueError:
        print("❌ Invalid input. Please enter an integer.")

if __name__ == "__main__":
    main()
