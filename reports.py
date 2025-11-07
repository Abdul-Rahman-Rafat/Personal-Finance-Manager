
# ============================================================================
# reports.py - Financial reports and dashboard
# ============================================================================

"""Financial reporting and dashboard functionality."""

import datetime
from decimal import Decimal
import config
from utils import clear_screen, print_header, print_box


def calculate_health_score(income, expenses, savings):
    """Calculate financial health score (0-100)."""
    if income == 0:
        return 0
    
    savings_rate = (savings / income) * 100 if income > 0 else 0
    expense_ratio = (expenses / income) * 100 if income > 0 else 100
    
    # Score based on savings rate and expense ratio
    score = 0
    
    if savings_rate >= 30:
        score += 50
    elif savings_rate >= 20:
        score += 40
    elif savings_rate >= 10:
        score += 30
    elif savings_rate >= 0:
        score += 20
    else:
        score += 0
    
    if expense_ratio <= 50:
        score += 50
    elif expense_ratio <= 70:
        score += 40
    elif expense_ratio <= 90:
        score += 30
    elif expense_ratio <= 100:
        score += 20
    else:
        score += 10
    
    return min(100, score)


def view_dashboard():
    """Display financial dashboard."""
    clear_screen()
    print_header("PERSONAL FINANCE MANAGER v1.0")
    
    user_transactions = {tid: t for tid, t in config.transactions.items() 
                        if t["username"] == config.current_user}
    
    # Calculate totals
    total_income = Decimal("0")
    total_expenses = Decimal("0")
    category_totals = {}
    
    current_month = datetime.date.today().strftime("%Y-%m")
    
    for tid, trans in user_transactions.items():
        amount = Decimal(trans["amount"])
        if trans["date"].startswith(current_month):
            if trans["type"] == "income":
                total_income += amount
            else:
                total_expenses += amount
                category = trans["category"]
                category_totals[category] = category_totals.get(category, Decimal("0")) + amount
    
    net_savings = total_income - total_expenses
    current_balance = net_savings + Decimal("10000")  # Example starting balance
    
    currency = config.users[config.current_user]["currency"]
    
    # Display dashboard
    print_box([
        f"User: {config.users[config.current_user]['name']}",
        f"Period: {datetime.date.today().strftime('%B %Y')}"
    ], 70)
    
    print()
    print_box([
        f"Total Income:        {currency}{total_income:>12,.2f}",
        f"Total Expenses:      {currency}{total_expenses:>12,.2f}",
        f"Net Savings:         {currency}{net_savings:>12,.2f}",
        "─" * 66,
        f"Current Balance:     {currency}{current_balance:>12,.2f}"
    ], 70)
    
    # Top spending categories
    print("\nTop Spending Categories:")
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for i, (cat, amount) in enumerate(sorted_categories, 1):
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        print(f"{i}. {cat:<20} {currency}{amount:>10,.2f}  ({percentage:5.1f}%)")
    
    # Financial Health Score
    health_score = calculate_health_score(total_income, total_expenses, net_savings)
    print(f"\n💰 Financial Health Score: {health_score}/100")
    
    if health_score >= 80:
        print("   Status: Excellent! Keep up the good work! 🌟")
    elif health_score >= 60:
        print("   Status: Good. Room for improvement. 👍")
    elif health_score >= 40:
        print("   Status: Fair. Consider reducing expenses. ⚠️")
    else:
        print("   Status: Needs attention. Review your budget. ⚠️")
    
    input("\nPress Enter to continue...")

