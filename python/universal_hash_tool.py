import hashlib
import os

def hash_string(input_string, algorithm='md5'):
    try:
        hash_func = getattr(hashlib, algorithm)
        hash_object = hash_func(input_string.encode())
        return hash_object.hexdigest()
    except AttributeError:
        return f"Error: Unsupported hash algorithm '{algorithm}'."

def hash_file(file_path, algorithm='md5'):
    try:
        hash_func = getattr(hashlib, algorithm)
        hasher = hash_func()
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except AttributeError:
        return f"Error: Unsupported hash algorithm '{algorithm}'."

def main():
    print("🔐 Hash Generator")
    print("1. Hash a string")
    print("2. Hash a file")
    choice = input("Select an option (1 or 2): ").strip()

    print("\nAvailable hash algorithms: md5, sha1, sha256")
    algorithm = input("Choose a hash algorithm [default: md5]: ").strip().lower() or "md5"

    if choice == '1':
        user_input = input("\nEnter the string to hash: ").strip()
        result = hash_string(user_input, algorithm)
        print(f"\n✅ {algorithm.upper()} hash of the string:\n{result}")

    elif choice == '2':
        file_path = input("\nEnter the full file path: ").strip()
        result = hash_file(file_path, algorithm)
        print(f"\n✅ {algorithm.upper()} hash of the file:\n{result}")
    else:
        print("❌ Invalid choice. Please select 1 or 2.")

# Run the program
