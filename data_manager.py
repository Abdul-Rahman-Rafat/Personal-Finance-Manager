
# ============================================================================
# data_manager.py - Data persistence module
# ============================================================================

"""Data loading, saving, and export functionality."""

import json
import csv
import datetime
import os
import config
from utils import clear_screen, print_header
from decimal import Decimal


def load_data():
    """Load all data from JSON files."""
    try:
        if os.path.exists(config.USERS_FILE):
            with open(config.USERS_FILE, 'r') as f:
                config.users = json.load(f)
        
        if os.path.exists(config.TRANSACTIONS_FILE):
            with open(config.TRANSACTIONS_FILE, 'r') as f:
                config.transactions = json.load(f)
        
        if os.path.exists(config.BUDGETS_FILE):
            with open(config.BUDGETS_FILE, 'r') as f:
                config.budgets = json.load(f)
        
        if os.path.exists(config.GOALS_FILE):
            with open(config.GOALS_FILE, 'r') as f:
                config.savings_goals = json.load(f)
                
    except Exception as e:
        print(f"Error loading data: {e}")


def save_data():
    """Save all data to JSON files."""
    try:
        with open(config.USERS_FILE, 'w') as f:
            json.dump(config.users, f, indent=4)
        
        with open(config.TRANSACTIONS_FILE, 'w') as f:
            json.dump(config.transactions, f, indent=4)
        
        with open(config.BUDGETS_FILE, 'w') as f:
            json.dump(config.budgets, f, indent=4)
        
        with open(config.GOALS_FILE, 'w') as f:
            json.dump(config.savings_goals, f, indent=4)
            
    except Exception as e:
        print(f"Error saving data: {e}")


def export_to_csv():
    """Export transactions to CSV file."""
    clear_screen()
    print_header("EXPORT TO CSV")
    
    user_transactions = {tid: t for tid, t in config.transactions.items() 
                        if t["username"] == config.current_user}
    
    if not user_transactions:
        print("No transactions to export.")
        input("\nPress Enter to continue...")
        return
    
    filename = f"transactions_{config.current_user}_{datetime.date.today()}.csv"
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['transaction_id', 'date', 'type', 'category', 
                         'amount', 'description', 'payment_method']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tid, trans in user_transactions.items():
                writer.writerow({
                    'transaction_id': trans['transaction_id'],
                    'date': trans['date'],
                    'type': trans['type'],
                    'category': trans['category'],
                    'amount': trans['amount'],
                    'description': trans['description'],
                    'payment_method': trans['payment_method']
                })
        
        print(f"✅ Transactions exported to {filename}")
    except Exception as e:
        print(f"❌ Export failed: {e}")
    
    input("\nPress Enter to continue...")

