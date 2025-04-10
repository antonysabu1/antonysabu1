def find_factors():
    try:
        n = int(input("Enter a number: "))
        if n <= 0:
            print("Please enter a positive integer.")
            return

        print(f"\nThe number is {n}")
        print("Factors:")

        for i in range(1, n + 1):
            if n % i == 0:
                print(i)

    except ValueError:
        print("Invalid input. Please enter a valid integer.")

find_factors()
