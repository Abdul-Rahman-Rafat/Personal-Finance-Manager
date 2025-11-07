
# ============================================================================
# budget.py - Budget management module
# ============================================================================

"""Monthly budget management functionality."""

import datetime
from decimal import Decimal
import config
from utils import clear_screen, print_header, validate_amount
from data_manager import save_data


def set_budget():
    """Set monthly budget for categories."""
    clear_screen()
    print_header("SET MONTHLY BUDGET")
    
    print("Available categories:")
    for i, cat in enumerate(config.EXPENSE_CATEGORIES, 1):
        print(f"{i}. {cat}")
    
    cat_choice = input("\nSelect category: ").strip()
    
    try:
        category = config.EXPENSE_CATEGORIES[int(cat_choice) - 1]
    except:
        print("❌ Invalid category!")
        input("\nPress Enter to continue...")
        return
    
    amount_str = input(f"\nEnter monthly budget for {category}: ").strip()
    amount = validate_amount(amount_str)
    
    if not amount:
        print("❌ Invalid amount!")
        input("\nPress Enter to continue...")
        return
    
    if config.current_user not in config.budgets:
        config.budgets[config.current_user] = {}
    
    config.budgets[config.current_user][category] = str(amount)
    save_data()
    
    print(f"\n✅ Budget set: {category} = {config.users[config.current_user]['currency']}{amount}")
    input("\nPress Enter to continue...")


def view_budget_status():
    """View budget status and spending."""
    clear_screen()
    print_header("BUDGET STATUS")
    
    if config.current_user not in config.budgets or not config.budgets[config.current_user]:
        print("No budgets set. Please set budgets first.")
        input("\nPress Enter to continue...")
        return
    
    user_budgets = config.budgets[config.current_user]
    current_month = datetime.date.today().strftime("%Y-%m")
    
    # Calculate spending per category this month
    category_spending = {}
    for tid, trans in config.transactions.items():
        if (trans["username"] == config.current_user and 
            trans["type"] == "expense" and 
            trans["date"].startswith(current_month)):
            cat = trans["category"]
            amount = Decimal(trans["amount"])
            category_spending[cat] = category_spending.get(cat, Decimal("0")) + amount
    
    currency = config.users[config.current_user]["currency"]
    
    print(f"{'Category':<20} {'Budget':>12} {'Spent':>12} {'Remaining':>12} {'Status':<10}")
    print("=" * 75)
    
    for category, budget_str in user_budgets.items():
        budget = Decimal(budget_str)
        spent = category_spending.get(category, Decimal("0"))
        remaining = budget - spent
        percentage = (spent / budget * 100) if budget > 0 else 0
        
        if percentage <= 80:
            status = "✅ Good"
        elif percentage <= 100:
            status = "⚠️  Warning"
        else:
            status = "❌ Over"
        
        print(f"{category:<20} {currency}{budget:>10,.2f} {currency}{spent:>10,.2f} "
              f"{currency}{remaining:>10,.2f} {status:<10}")
    
    input("\nPress Enter to continue...")

