import random
from datetime import datetime


random.seed(datetime.now().timestamp())

def generate_random_numbers(count=5, lower=0, upper=10):
    """
    Generate and print random integers between lower and upper bounds.

    Parameters:
    count (int): Number of random integers to generate
    lower (int): Lower bound (inclusive)
    upper (int): Upper bound (inclusive)
    """
    print("🎲 Random Numbers:")
    for _ in range(count):
        print(random.randint(lower, upper), end="\t")
    print()


generate_random_numbers()
