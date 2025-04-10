import os

def list_allowed_files():
    try:
        path = input("Enter your path: ").strip()

        # Check if path exists
        if not os.path.isdir(path):
            print("Invalid path. Please enter a valid directory path.")
            return

        files = os.listdir(path)

        allowed_extensions = {"jpg", "jpeg", "png", "webp", "pdf"}

        print("\nAllowed files found in directory:\n")

        for file in files:
          
            if os.path.isdir(os.path.join(path, file)) or file.startswith('.'):
                continue

        
            if "." in file:
                ext = file.split(".")[-1].lower()
                if ext in allowed_extensions:
                    print(f"✔ {file}")
            else:
                continue

    except Exception as e:
        print(f"Error: {e}")


list_allowed_files()
