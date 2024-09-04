import pyodbc

# Connect to the database
def connect_to_db():
    server = 'NOONE'
    database = 'Hotel'
    username = 'yogi03'
    password = 'Yogithathesql@03'
    cnxn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    try:
        cnxn = pyodbc.connect(cnxn_str)
        print("Connection to the database successful!")
        return cnxn
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to fetch booking IDs
def fetch_booking_ids(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT BookingID FROM Bookings")
    rows = cursor.fetchall()
    booking_ids = [row[0] for row in rows]
    print("Booking IDs fetched successfully.")
    return booking_ids

# Add a new guest
def add_guest(cnxn, first_name, last_name, email, phone):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Guests (FirstName, LastName, Email, Phone) VALUES (?, ?, ?, ?)", (first_name, last_name, email, phone))
    cnxn.commit()
    print("Guest added successfully.")

# Add a new room
def add_room(cnxn, room_number, room_type, price, capacity, availability):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Rooms (RoomNumber, RoomType, Price, Capacity, Availability) VALUES (?, ?, ?, ?, ?)", (room_number, room_type, price, capacity, availability))
    cnxn.commit()
    print("Room added successfully.")

# Make a reservation
def make_reservation(cnxn, guest_id, room_id, check_in_date, check_out_date, total_amount):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Reservations (RoomID, GuestID, CheckInDate, CheckOutDate, TotalAmount) VALUES (?, ?, ?, ?, ?)", (room_id, guest_id, check_in_date, check_out_date, total_amount))
    cnxn.commit()
    print("Reservation made successfully.")

# Confirm a booking
def confirm_booking(cnxn, room_id, check_in_date, check_out_date, total_amount):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Bookings (RoomID, CheckInDate, CheckOutDate, TotalAmount, IsConfirmed) VALUES (?, ?, ?, ?, 1)", (room_id, check_in_date, check_out_date, total_amount))
    cnxn.commit()
    print("Booking confirmed successfully.")
    return fetch_booking_ids(cnxn)[-1]

# Make a payment
def make_payment(cnxn, booking_id, amount, payment_date, payment_method):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Payments (BookingID, Amount, PaymentDate, PaymentMethod) VALUES (?, ?, ?, ?)", (booking_id, amount, payment_date, payment_method))
    cnxn.commit()
    print("Payment made successfully.")


def show_menu():
    print("\nHotel Management System")
    print("1. Add Guest")
    print("2. Add Room")
    print("3. Make Reservation")
    print("4. Confirm Booking")
    print("5. Make Payment")
    print("6. Exit")

def main():
    cnxn = connect_to_db()
    booking_id = None

    if cnxn:
        while True:
            show_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                phone = input("Enter phone number: ")
                add_guest(cnxn, first_name, last_name, email, phone)

            elif choice == "2":
                room_number = input("Enter room number: ")
                room_type = input("Enter room type: ")
                price = float(input("Enter price per night: "))
                capacity = int(input("Enter room capacity: "))
                availability = input("Is the room available (yes/no)? ").strip().lower() == 'yes'
                add_room(cnxn, room_number, room_type, price, capacity, 1 if availability else 0)

            elif choice == "3":
                guest_id = int(input("Enter guest ID: "))
                room_id = int(input("Enter room ID: "))
                check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
                check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
                total_amount = float(input("Enter total amount: "))
                make_reservation(cnxn, guest_id, room_id, check_in_date, check_out_date, total_amount)

            elif choice == "4":
                room_id = int(input("Enter room ID: "))
                check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
                check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
                total_amount = float(input("Enter total amount for the booking: "))
                booking_id = confirm_booking(cnxn, room_id, check_in_date, check_out_date, total_amount)

            elif choice == "5":
                if booking_id:
                    amount = float(input("Enter payment amount: "))
                    payment_date = input("Enter payment date (YYYY-MM-DD): ")
                    payment_method = input("Enter payment method (e.g., cash, credit card): ")
                    make_payment(cnxn, booking_id, amount, payment_date, payment_method)
                else:
                    print("No booking ID found. Please confirm a booking first.")

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice, please try again.")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
