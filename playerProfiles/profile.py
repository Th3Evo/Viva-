import csv
import os


csv_file_path = '/home/runner/Viva-Discord-Bot/Statistics/users.csv'

def initialize_csv():
    """
    Initializes the CSV file for storing user profiles if it doesn't exist.
    """
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)


    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'UserID'])
        print("CSV file initialized successfully.")
    else:
        print("CSV file already exists.")

def create_user_profile(user_id, username):
    """
    Creates a user profile in the CSV file by adding their username and user ID.
    """
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, user_id])
    print(f"User profile for {username} (ID: {user_id}) created successfully.")

def user_exists(user_id):
    """
    Checks if a user already exists in the CSV file based on their user ID.
    """
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == str(user_id):
                return True
    return False

def get_user_by_id(user_id):
    """
    Retrieves the username associated with a user ID.
    """
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == str(user_id):
                return row[0]
    return None 