import re

def check_password_complexity(password):
    """
    Check whether the password meets complexity requirements.

    Rules:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - No spaces allowed
    """
    if len(password) < 8:
        return "❌ Password must be at least 8 characters long."
    
    if ' ' in password:
        return "❌ Password must not contain spaces."

    if not re.search(r'[A-Z]', password):
        return "❌ Password must contain at least one uppercase letter."
    
    if not re.search(r'[a-z]', password):
        return "❌ Password must contain at least one lowercase letter."
    
    if not re.search(r'[0-9]', password):
        return "❌ Password must contain at least one digit."
    
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return "❌ Password must contain at least one special character (!@#$%^&* etc.)"
    
    return "✅ Password is strong and meets all complexity requirements."

def main():
    password = input("🔐 Enter a password to check its complexity: ")
    result = check_password_complexity(password)
    print(result)


if __name__ == "__main__":
    main()
