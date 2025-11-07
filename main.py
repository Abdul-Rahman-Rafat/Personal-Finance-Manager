"""
Personal Finance Manager - Main Entry Point
Module-based architecture for better organization
"""

# main.py
import os
import sys

# Import all modules
from auth import register_user, login_user
from transactions import (add_transaction, view_transactions, 
                        edit_transaction, delete_transaction, search_transactions)
from reports import view_dashboard
from budget import set_budget, view_budget_status
from savings import add_savings_goal, view_savings_goals
from data_manager import load_data, save_data, export_to_csv
from utils import clear_screen, print_header
import config


def main_menu():
    """Display and handle main menu."""
    while True:
        clear_screen()
        print_header("MAIN MENU")
        
        print(f"Logged in as: {config.users[config.current_user]['name']}\n")
        
        print("1.  Dashboard")
        print("2.  Add Transaction")
        print("3.  View Transactions")
        print("4.  Edit Transaction")
        print("5.  Delete Transaction")
        print("6.  Search Transactions")
        print("7.  Set Budget")
        print("8.  View Budget Status")
        print("9.  Add Savings Goal")
        print("10. View Savings Goals")
        print("11. Export to CSV")
        print("12. Logout")
        print("13. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            view_dashboard()
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            edit_transaction()
        elif choice == "5":
            delete_transaction()
        elif choice == "6":
            search_transactions()
        elif choice == "7":
            set_budget()
        elif choice == "8":
            view_budget_status()
        elif choice == "9":
            add_savings_goal()
        elif choice == "10":
            view_savings_goals()
        elif choice == "11":
            export_to_csv()
        elif choice == "12":
            return
        elif choice == "13":
            print("\nThank you for using Personal Finance Manager!")
            exit(0)
        else:
            print("❌ Invalid option!")
            input("\nPress Enter to continue...")


def main():
    """Main program entry point."""
    load_data()
    
    while True:
        clear_screen()
        print_header("💰 PERSONAL FINANCE MANAGER")
        
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            if login_user():
                main_menu()
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("❌ Invalid option!")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

