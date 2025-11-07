
# ============================================================================
# auth.py - Authentication module
# ============================================================================

"""User authentication and management."""

import hashlib
import uuid
import datetime
import config
from utils import clear_screen, print_header
from data_manager import save_data


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    """Register a new user."""
    clear_screen()
    print_header("USER REGISTRATION")
    
    name = input("Enter your name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        input("\nPress Enter to continue...")
        return False
    
    username = input("Enter username: ").strip()
    if not username or username in config.users:
        print("❌ Username already exists or is invalid!")
        input("\nPress Enter to continue...")
        return False
    
    password = input("Enter password (min 4 characters): ").strip()
    while True:
            print("❌ Password must be at least 4 characters!")
            password = input("Enter ur password again : ").strip()
            if len(password) >= 4:
                break
    if len(password) < 4:
        print("❌ Password must be at least 4 characters!")
        input("\nPress Enter to continue...")
        return False
    
    
    
    currency = input("Enter currency (e.g., USD, EUR, EGP) [USD]: ").strip() or "USD"
    
    user_id = str(uuid.uuid4())
    config.users[username] = {
        "user_id": user_id,
        "name": name,
        "password": hash_password(password),
        "currency": currency,
        "created_date": str(datetime.date.today())
    }
    
    save_data()
    print(f"\n✅ User registered successfully! Welcome, {name}!")
    input("\nPress Enter to continue...")
    return True


def login_user():
    """Login an existing user."""
    clear_screen()
    print_header("USER LOGIN")
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if username in config.users and config.users[username]["password"] == hash_password(password):
        config.current_user = username
        print(f"\n✅ Welcome back, {config.users[username]['name']}!")
        input("\nPress Enter to continue...")
        return True
    else:
        print("❌ Invalid credentials!")
        input("\nPress Enter to continue...")
        return False

