def is_palindrome_string(s):
    """Check if a string is a palindrome (ignores case and spaces)."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

def is_palindrome_number(n):
    """Check if a number is a palindrome."""
    original = n
    reversed_num = 0

    while n > 0:
        digit = n % 10
        reversed_num = reversed_num * 10 + digit
        n //= 10

    return original == reversed_num

def main():
    user_input = input("Enter a number or string to check if it's a palindrome: ")

    if user_input.isdigit():
        num = int(user_input)
        if is_palindrome_number(num):
            print(f"✅ {num} is a Palindrome number.")
        else:
            print(f"🔁 {num} is NOT a Palindrome number.")
    else:
        if is_palindrome_string(user_input):
            print(f"✅ \"{user_input}\" is a Palindrome string.")
        else:
            print(f"🔁 \"{user_input}\" is NOT a Palindrome string.")


if __name__ == "__main__":
    main()
