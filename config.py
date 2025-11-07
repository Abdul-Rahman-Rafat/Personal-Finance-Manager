
# ============================================================================
# config.py - Global configuration and data storage
# ============================================================================

"""Configuration and global data storage."""

# Global data storage
users = {}
transactions = {}
budgets = {}
savings_goals = {}
current_user = None

# File paths
USERS_FILE = "users.json"
TRANSACTIONS_FILE = "transactions.json"
BUDGETS_FILE = "budgets.json"
GOALS_FILE = "savings_goals.json"

# Categories
EXPENSE_CATEGORIES = ["Food", "Rent", "Transportation", "Entertainment", "Utilities", 
                    "Healthcare", "Shopping", "Education", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Investment", "Gift", "Other"]

