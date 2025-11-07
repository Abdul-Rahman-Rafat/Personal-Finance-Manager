
# ============================================================================
# utils.py - Utility functions
# ============================================================================

"""Utility functions for the application."""

import os
import datetime
from decimal import Decimal


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"{title:^80}")
    print("=" * 80 + "\n")


def print_box(content, width=80):
    """Print content in a box."""
    print("┌" + "─" * (width - 2) + "┐")
    for line in content:
        print(f"│ {line:<{width-4}} │")
    print("└" + "─" * (width - 2) + "┘")


def validate_amount(amount_str):
    """Validate and convert amount string to Decimal."""
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return None
        return amount
    except:
        return None


def validate_date(date_str):
    """Validate date string in YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

