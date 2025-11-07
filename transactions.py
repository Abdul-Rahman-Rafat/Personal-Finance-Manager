
# ============================================================================
# transactions.py - Transaction management module
# ============================================================================

"""Transaction CRUD operations and search functionality."""

import datetime
import uuid
from decimal import Decimal
import config
from utils import (clear_screen, print_header, validate_amount, validate_date)
from data_manager import save_data


def add_transaction():
    """Add a new transaction."""
    clear_screen()
    print_header("ADD TRANSACTION")
    
    print("1. Income")
    print("2. Expense")
    choice = input("\nSelect type: ").strip()
    
    if choice == "1":
        trans_type = "income"
        categories = config.INCOME_CATEGORIES
    elif choice == "2":
        trans_type = "expense"
        categories = config.EXPENSE_CATEGORIES
    else:
        print("❌ Invalid choice!")
        input("\nPress Enter to continue...")
        return
    
    # Amount
    amount_str = input("\nEnter amount: ").strip()
    amount = validate_amount(amount_str)
    if not amount:
        print("❌ Invalid amount!")
        input("\nPress Enter to continue...")
        return
    
    # Category
    print(f"\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    cat_choice = input("\nSelect category: ").strip()
    
    try:
        category = categories[int(cat_choice) - 1]
    except:
        print("❌ Invalid category!")
        input("\nPress Enter to continue...")
        return
    
    # Date
    date_str = input("\nEnter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = str(datetime.date.today())
    elif not validate_date(date_str):
        print("❌ Invalid date format!")
        input("\nPress Enter to continue...")
        return
    
    # Description
    description = input("Enter description: ").strip() or "No description"
    
    # Payment method
    payment_method = input("Payment method (Cash/Credit Card/Debit Card) [Cash]: ").strip() or "Cash"
    
    # Create transaction
    trans_id = "TXN" + str(len(config.transactions) + 1).zfill(4)
    transaction = {
        "transaction_id": trans_id,
        "user_id": config.users[config.current_user]["user_id"],
        "username": config.current_user,
        "type": trans_type,
        "amount": str(amount),
        "category": category,
        "date": date_str,
        "description": description,
        "payment_method": payment_method
    }
    
    config.transactions[trans_id] = transaction
    save_data()
    
    print(f"\n✅ Transaction {trans_id} added successfully!")
    input("\nPress Enter to continue...")


def view_transactions():
    """View all transactions for current user."""
    clear_screen()
    print_header("TRANSACTION LIST")
    
    user_transactions = {tid: t for tid, t in config.transactions.items() 
                        if t["username"] == config.current_user}
    
    if not user_transactions:
        print("No transactions found.")
        input("\nPress Enter to continue...")
        return
    
    # Sort by date
    sorted_trans = sorted(user_transactions.items(), 
                         key=lambda x: x[1]["date"], reverse=True)
    
    print("=" * 100)
    print(f"{'ID':<12} | {'Date':<12} | {'Type':<8} | {'Category':<15} | {'Amount':>12}")
    print("=" * 100)
    
    for tid, trans in sorted_trans:
        amount = Decimal(trans["amount"])
        symbol = config.users[config.current_user]["currency"]
        print(f"{tid:<12} | {trans['date']:<12} | {trans['type']:<8} | "
              f"{trans['category']:<15} | {symbol}{amount:>10,.2f}")
    
    print("=" * 100)
    input("\nPress Enter to continue...")


def edit_transaction():
    """Edit an existing transaction."""
    clear_screen()
    print_header("EDIT TRANSACTION")
    
    trans_id = input("Enter transaction ID: ").strip()
    
    if trans_id not in config.transactions:
        print("❌ Transaction not found!")
        input("\nPress Enter to continue...")
        return
    
    if config.transactions[trans_id]["username"] != config.current_user:
        print("❌ Access denied!")
        input("\nPress Enter to continue...")
        return
    
    trans = config.transactions[trans_id]
    print(f"\nCurrent details:")
    print(f"Type: {trans['type']}")
    print(f"Amount: {trans['amount']}")
    print(f"Category: {trans['category']}")
    print(f"Date: {trans['date']}")
    print(f"Description: {trans['description']}")
    
    print("\nLeave blank to keep current value")
    
    # Edit amount
    new_amount = input(f"\nNew amount [{trans['amount']}]: ").strip()
    if new_amount:
        amount = validate_amount(new_amount)
        if amount:
            trans['amount'] = str(amount)
    
    # Edit description
    new_desc = input(f"New description [{trans['description']}]: ").strip()
    if new_desc:
        trans['description'] = new_desc
    
    save_data()
    print("\n✅ Transaction updated successfully!")
    input("\nPress Enter to continue...")


def delete_transaction():
    """Delete a transaction."""
    clear_screen()
    print_header("DELETE TRANSACTION")
    
    trans_id = input("Enter transaction ID: ").strip()
    
    if trans_id not in config.transactions:
        print("❌ Transaction not found!")
        input("\nPress Enter to continue...")
        return
    
    if config.transactions[trans_id]["username"] != config.current_user:
        print("❌ Access denied!")
        input("\nPress Enter to continue...")
        return
    
    confirm = input(f"\nAre you sure you want to delete {trans_id}? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        del config.transactions[trans_id]
        save_data()
        print("\n✅ Transaction deleted successfully!")
    else:
        print("\n❌ Deletion cancelled.")
    
    input("\nPress Enter to continue...")


def search_transactions():
    """Search and filter transactions."""
    clear_screen()
    print_header("SEARCH TRANSACTIONS")
    
    print("1. Search by date range")
    print("2. Filter by category")
    print("3. Filter by amount range")
    print("4. Back")
    
    choice = input("\nSelect option: ").strip()
    
    user_transactions = {tid: t for tid, t in config.transactions.items() 
                        if t["username"] == config.current_user}
    
    results = []
    
    if choice == "1":
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        
        if not validate_date(start_date) or not validate_date(end_date):
            print("❌ Invalid date format!")
            input("\nPress Enter to continue...")
            return
        
        results = {tid: t for tid, t in user_transactions.items() 
                  if start_date <= t["date"] <= end_date}
    
    elif choice == "2":
        category = input("Enter category: ").strip()
        results = {tid: t for tid, t in user_transactions.items() 
                  if t["category"].lower() == category.lower()}
    
    elif choice == "3":
        min_amount = input("Minimum amount: ").strip()
        max_amount = input("Maximum amount: ").strip()
        
        min_amt = validate_amount(min_amount) or Decimal("0")
        max_amt = validate_amount(max_amount) or Decimal("999999999")
        
        results = {tid: t for tid, t in user_transactions.items() 
                if min_amt <= Decimal(t["amount"]) <= max_amt}
    
    else:
        return
    
    # Display results
    clear_screen()
    print_header("SEARCH RESULTS")
    
    if not results:
        print("No matching transactions found.")
    else:
        print(f"Found {len(results)} transaction(s)\n")
        print("=" * 100)
        print(f"{'ID':<12} | {'Date':<12} | {'Type':<8} | {'Category':<15} | {'Amount':>12}")
        print("=" * 100)
        
        for tid, trans in results.items():
            amount = Decimal(trans["amount"])
            symbol = config.users[config.current_user]["currency"]
            print(f"{tid:<12} | {trans['date']:<12} | {trans['type']:<8} | "
                f"{trans['category']:<15} | {symbol}{amount:>10,.2f}")
        
        print("=" * 100)
    
    input("\nPress Enter to continue...")

