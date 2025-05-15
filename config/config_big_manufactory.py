# config.py

# Basic Configuration
import random
INITIAL_seed_CONFIG = {'seed': 322}
INITIAL_transaction_CONFIG = {'transaction': 200}  # 200 transactions

# Account Related Configuration
ACCOUNT_CONFIG = {
    "initial_cash": 5000000.00,  # 5 million cash
    "initial_bank_deposit": 15000000.00,  # 15 million bank deposit
    "initial_fixed_asset": 8000000.00,  # 8 million fixed assets
}

# Product Configuration
INITIAL_inventory_CONFIG = {'product':[
    {"id": "P001", "name": "Heavy Equipment A", "cost": 500000, "price": 750000, "quantity": 0, "status": "On Sale"},
    {"id": "P002", "name": "Heavy Equipment B", "cost": 800000, "price": 1200000, "quantity": 0, "status": "On Sale"},
    {"id": "P003", "name": "Heavy Equipment C", "cost": 1000000, "price": 1500000, "quantity": 0, "status": "On Sale"},
    {"id": "P004", "name": "Heavy Equipment D", "cost": 1500000, "price": 2250000, "quantity": 0, "status": "On Sale"},
]}

# Transfer Configuration
INITIAL_transfer_CONFIG = {'amount': 1000000.00}  # 1 million

# Expense Configuration
INITIAL_expense_CONFIG = {
    'amount': 10,  #* 1000
    'weight': [3, 3, 1]
}

# Sales Configuration
INITIAL_sale_CONFIG = {
    'max_quantity': 1.00,  # Maximum 1 unit per transaction
    'min_profit_margin': 0.30,  # Minimum profit margin 30%
    'max_profit_margin': 0.50,  # Maximum profit margin 50%
    'pay_weight': [0.4, 0.6],  # Accounts receivable ratio slightly higher
}

# Purchase Configuration
INITIAL_purchase_CONFIG = {
    'max_quantity': 1.00,  # Maximum quantity 1
    'max_base_quantity': 2.00,  # Maximum base quantity 2
    'min_base_quantity': 1.00,  # Minimum base quantity 1
    'payment_method': [0.3, 0.6, 0.1],  # Higher ratio for accounts payable
}

# Fixed Asset Configuration
INITIAL_fix_asset_CONFIG = {'asset': [
    {"name": "Production Line Equipment", "price_range": (500000.00, 1000000.00)},
    {"name": "Heavy Machinery", "price_range": (800000.00, 1500000.00)},
    {"name": "Industrial Facilities", "price_range": (1000000.00, 2000000.00)}
]}

# Simulation Configuration
INITIAL_simulate_CONFIG = {
    'sale_count_min': 0.00,
    'sale_count_max': 1.00,
    'fixed_asset_min': 0.00,
    'fixed_asset_max': 2.00,
    'purchase_count_min': 1.00,
    'purchase_count_max': 2.00,
    'expense_count_min': 1.00,
    'expense_count_max': 2.00
}



