
# ============================================================================
# savings.py - Savings goals module
# ============================================================================

"""Savings goals management functionality."""

import datetime
from decimal import Decimal
import config
from utils import clear_screen, print_header, validate_amount, validate_date
from data_manager import save_data


def add_savings_goal():
    """Add a savings goal."""
    clear_screen()
    print_header("ADD SAVINGS GOAL")
    
    goal_name = input("Goal name: ").strip()
    if not goal_name:
        print("❌ Goal name cannot be empty!")
        input("\nPress Enter to continue...")
        return
    
    target_str = input("Target amount: ").strip()
    target = validate_amount(target_str)
    
    if not target:
        print("❌ Invalid amount!")
        input("\nPress Enter to continue...")
        return
    
    deadline = input("Target date (YYYY-MM-DD): ").strip()
    if not validate_date(deadline):
        print("❌ Invalid date!")
        input("\nPress Enter to continue...")
        return
    
    current_str = input("Current savings (0 if starting new): ").strip() or "0"
    current = validate_amount(current_str)
    if current is None:
        current = Decimal("0")
    
    goal_id = "GOAL" + str(len(config.savings_goals) + 1).zfill(3)
    
    if config.current_user not in config.savings_goals:
        config.savings_goals[config.current_user] = {}
    
    config.savings_goals[config.current_user][goal_id] = {
        "goal_id": goal_id,
        "name": goal_name,
        "target": str(target),
        "current": str(current),
        "deadline": deadline,
        "created_date": str(datetime.date.today())
    }
    
    save_data()
    print(f"\n✅ Savings goal '{goal_name}' created!")
    input("\nPress Enter to continue...")


def view_savings_goals():
    """View all savings goals with progress."""
    clear_screen()
    print_header("SAVINGS GOALS")
    
    if config.current_user not in config.savings_goals or not config.savings_goals[config.current_user]:
        print("No savings goals set.")
        input("\nPress Enter to continue...")
        return
    
    currency = config.users[config.current_user]["currency"]
    
    for goal_id, goal in config.savings_goals[config.current_user].items():
        target = Decimal(goal["target"])
        current = Decimal(goal["current"])
        percentage = (current / target * 100) if target > 0 else 0
        remaining = target - current
        
        print(f"\n{goal['name']} ({goal_id})")
        print(f"Target: {currency}{target:,.2f} | Current: {currency}{current:,.2f} | "
              f"Remaining: {currency}{remaining:,.2f}")
        print(f"Deadline: {goal['deadline']}")
        
        # Progress bar
        bar_length = 40
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"Progress: [{bar}] {percentage:.1f}%")
    
    input("\nPress Enter to continue...")
