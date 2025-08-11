"""

Temmy Flight Booking System
A console-based application for booking flights with multiple class options,
discounts for children and returning customers, and VAT calculation.
"""

# ====================== CONFIGURATION CONSTANTS ======================
# Flight classes and their base prices (in £)
ticket_prices = {
    "premium": 9500,        # Highest class with premium services
    "first_class": 7500,     # Luxury class with extra amenities
    "second_class": 5535.70, # Mid-tier comfortable seating
    "economy": 3500          # Standard budget-friendly option
}

# Tax and discount rates
VAT_RATE = 0.15             # 15% Value Added Tax
RETURNING_DISCOUNT = 0.10   # 10% discount for returning customers
CHILD_DISCOUNT = 0.20       # 20% discount for children under 8

# ====================== UTILITY FUNCTIONS ======================
def get_valid_integer(prompt, min_value=0):
    """
    Safely gets and validates a positive integer input from user
    Args:
        prompt: Message to display to user
        min_value: Minimum acceptable value (default 0)
    Returns:
        Validated integer input
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"❌ Enter a number greater than or equal to {min_value}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def get_valid_string(prompt):
    """
    Gets and validates non-empty string input from user
    Args:
        prompt: Message to display to user
    Returns:
        Non-empty string input
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("❌ This field cannot be empty. Please enter valid text.")

# ====================== CORE FUNCTIONALITY ======================
def book_flight():
    """
    Handles the complete flight booking process:
    - Collects passenger details
    - Applies applicable discounts
    - Calculates final price with VAT
    - Saves booking to file
    """
    total_cost = 0  # Track total for all tickets in this booking session

    # Check for returning customer status
    returning = input("\nAre you a returning customer? (yes/no): ").strip().lower()
    is_returning = returning == "yes"

    # Get number of tickets needed
    num_tickets = get_valid_integer("\nHow many tickets would you like to book? ", 1)

    for i in range(num_tickets):
        print(f"\n=== Booking {i + 1} ===")
        
        # Display available flight classes and prices
        print("\nAvailable booking options:")
        for flight, price in ticket_prices.items():
            print(f" - {flight.replace('_', ' ').title()}: £{price}")

        # Validate flight class selection
        while True:
            flight_choice = input("Enter your booking option: ").lower().replace(" ", "_")
            if flight_choice in ticket_prices:
                break
            else:
                print("❌ Invalid option. Please choose from the available options.")

        # Collect passenger details
        name = get_valid_string("Full Name: ").strip()

        # Validate mobile number to be exactly 11 digits
        while True:
            telephone = get_valid_string("Mobile Number: ").strip()
            if telephone.isdigit() and len(telephone) == 11:
                 break
            else:
                print("❌ Invalid mobile number. Please enter exactly 11 digits.")

        age = get_valid_integer("Age: ", 0)
        email = get_valid_string("Email address: ").strip()

        # Calculate pricing with discounts
        base_price = ticket_prices[flight_choice]
        discount = 0

        # Apply child discount if passenger is under 8
        if age < 8:
            discount += base_price * CHILD_DISCOUNT
            print("✅ Child discount (20%) applied.")

        # Apply returning customer discount if applicable
        if is_returning:
            discount += base_price * RETURNING_DISCOUNT
            print("✅ Returning customer discount (10%) applied.")

        # Calculate final price with VAT
        price_after_discount = base_price - discount
        vat = price_after_discount * VAT_RATE
        total_price = price_after_discount + vat

        print(f"Total price for this ticket: £{total_price:.2f}")

        # Prepare booking record
        booking_data = {
            "Name": name,
            "Telephone": telephone,
            "Age": str(age),
            "Email": email,
            "Class": flight_choice.replace('_', ' ').title(),
            "Base Price": f"{base_price:.2f}",
            "Discount": f"{discount:.2f}",
            "VAT": f"{vat:.2f}",
            "Total": f"{total_price:.2f}"
        }
        
        # Save booking to persistent storage
        with open("bookings.txt", "a") as file:
            file.write(",".join(booking_data.values()) + "\n")
        
        total_cost += total_price

    # Display transaction summary
    print(f"\n✅ All bookings completed! Total cost for all tickets: £{total_cost:.2f}")

def view_bookings():
    """
    Displays all saved bookings from the bookings.txt file
    Handles cases where no bookings exist or file is missing
    """
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
      
        if not bookings:
            print("\n📝 No bookings found.")
            return
            
        # Display all bookings with formatted output
        print("\n📋 All Bookings:")
        for idx, booking in enumerate(bookings, 1):
            data = booking.strip().split(',')
            if len(data) < 9:
                print(f"❌ Data is incomplete: {booking.strip()}")
                continue
            print(f"\nBooking {idx}:")
            print(f" Name: {data[0]}")
            print(f" Mobile Number: {data[1]}")
            print(f" Age: {data[2]}")
            print(f" Email: {data[3]}")
            print(f" Class: {data[4]}")
            print(f" Base Price: £{data[5]}")
            print(f" Discount: -£{data[6]}")
            print(f" VAT (15%): +£{data[7]}")
            print(f" Total Paid: £{data[8]}")
            
    except FileNotFoundError:
        print("\n📝 No bookings information found. Book a flight first.")

# ====================== MAIN APPLICATION ======================
def main_menu():
    """
    Main program loop that displays menu and handles user choices
    """
    while True:
        # Display menu options
        print("\n==== Welcome to Temmy Flight Booking System Menu ====")
        print("1. Book a Flight")
        print("2. View All Bookings")
        print("3. Quit")

        # Get and validate user choice
        choice = input("Enter your choice (1, 2 or 3): ").strip()

        if choice == "1":
            book_flight()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            print("👋 Thanks for using our service, hope to see you again. Goodbye!😊")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

# Program entry point
if __name__ == "__main__":
    main_menu()