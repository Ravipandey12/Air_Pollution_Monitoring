import csv
import re
import hashlib
import os

# Function to hash the password using a salt
def hash_password(password):
    salt = os.urandom(16)  
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return salt.hex(), hashed_password  

def check_password(stored_salt, stored_hash, user_password):
    hashed_password = hashlib.sha256(bytes.fromhex(stored_salt) + user_password.encode('utf-8')).hexdigest()
    return hashed_password == stored_hash


def is_valid_email(email):
    return "@" in email and "." in email
    
def is_valid_password(password):
    return (len(password) >= 8 and 
            any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password) and 
            any(not c.isalnum() for c in password))

def register_user(email, password, nickname, filename='12325807.csv'):
    if not is_valid_email(email):
        return "Invalid email format"
    if not is_valid_password(password):
        return "Password doesn't meet the criteria"

    try:
       
        user_exists = False
        try:
            with open(filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['email'] == email:
                        user_exists = True
                        break
        except FileNotFoundError:
            pass  

        if user_exists:
            return "User already exists."

        # Register new user
        salt, hashed_password = hash_password(password)
        with open(filename, mode='a', newline='') as file:
            fieldnames = ['email', 'salt', 'password', 'nickname']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({'email': email, 'salt': salt, 'password': hashed_password, 'nickname': nickname})
        return "User registered successfully"
    
    except Exception as e:
        return f"Error registering user: {e}"


def verify_login(email, password, filename='12325807.csv'):
    attempts = 0
    try:
        while attempts < 5:
            with open(filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['email'] == email:
                        if check_password(row['salt'], row['password'], password):
                            return "Login successful"
                        else:
                            attempts += 1
                            print(f"Incorrect password. {5 - attempts} attempts left.")
                            if attempts == 5:
                                return "Too many failed attempts. Locked out."
            return "Email not found"
    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return f"Error verifying login: {e}"


def forgot_password(email, nickname, new_password, filename='12325807.csv'):
    if not is_valid_password(new_password):
        return "New password does not meet the criteria"

    rows = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            user_found = False
            for row in csv_reader:
                if row['email'] == email:
                    user_found = True
                    if row['nickname'] == nickname:
                        row['salt'], row['password'] = hash_password(new_password)
                    else:
                        return "Incorrect nickname"
                rows.append(row)

        if not user_found:
            return "Email not found"

        with open(filename, mode='w', newline='') as file:
            fieldnames = ['email', 'salt', 'password', 'nickname']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return "Password updated successfully"

    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return f"Error resetting password: {e}"
