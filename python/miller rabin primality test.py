import random

def is_prime(n, k=5):
    """
    Miller-Rabin primality test.

    Parameters:
    n (int): Number to test for primality.
    k (int): Number of accuracy iterations (default is 5).

    Returns:
    bool: True if n is probably prime, False if composite.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  

    return True  

def main():
    try:
        number = int(input("🔢 Enter a number to test for primality: "))
        if is_prime(number):
            print(f"✅ {number} is *probably* a **prime** number.")
        else:
            print(f"❌ {number} is **composite** (not prime).")
    except ValueError:
        print("❌ Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
