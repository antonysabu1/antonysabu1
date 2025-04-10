import calendar

def display_calendar():
    while True:
        try:
            year = int(input("Enter the year (e.g., 2024): "))
            if year <= 0:
                print("Year must be a positive integer. Please try again.")
                continue

            month = int(input("Enter the month (1-12): "))
            if month < 1 or month > 12:
                print("Month must be between 1 and 12. Please try again.")
                continue

            print("\n" + calendar.month(year, month))
            break  # Exit loop after successful input

        except ValueError:
            print("Invalid input. Please enter numeric values for year and month.")

display_calendar()
