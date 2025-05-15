# config.py

import random
INITIAL_seed_CONFIG = {'seed': 322}
# Increase transaction frequency
INITIAL_transaction_CONFIG = {'transaction': 200}  # Increase transaction count

# Account related configuration remains unchanged
ACCOUNT_CONFIG = {
    "initial_cash": 3000000.00,
    "initial_bank_deposit": 5000000.00,
    "initial_fixed_asset": 5000000.00,
}

# Product configuration - Adjusted for high value-added products
INITIAL_inventory_CONFIG = {'product':[
    {"id": "P001", "name": "Premium Product A", "cost": 5000.00, "price": 9000, "quantity": 0, "status": "On Sale"},
    {"id": "P002", "name": "Premium Product B", "cost": 10000.00, "price": 18000, "quantity": 0, "status": "On Sale"},
    {"id": "P003", "name": "Premium Product C", "cost": 20000.00, "price": 36000, "quantity": 0, "status": "On Sale"},
    {"id": "P004", "name": "Premium Product D", "cost": 50000.00, "price": 90000, "quantity": 0, "status": "On Sale"},
]}  # Increase gross margin to 50-80%

# Transfer configuration
INITIAL_transfer_CONFIG = {'amount': 50000.00}  # Reduce single transaction amount

# Expense configuration
INITIAL_expense_CONFIG = {
    'amount': 3,  # Increase expense baseline
    'weight': [2, 4, 1],  # Increase sales expense proportion
}

# Sales configuration
INITIAL_sale_CONFIG = {
    'max_quantity': 3.00,  # Reduce quantity per transaction
    'min_profit_margin': 0.70,  # Increase minimum profit margin to 50%
    'max_profit_margin': 1.00,  # Increase maximum profit margin to 80%
    'pay_weight': [0.7, 0.3],  # Increase cash payment ratio
    'customer_count': random.randint(20, 50),  # Increase customer count to 20-50
}

# Purchase configuration
INITIAL_purchase_CONFIG = {
    'max_quantity': 5.00,
    'max_base_quantity': 10.00,
    'min_base_quantity': 3.00,
    'payment_method': [0.3, 0.4, 0.3],  # Adjust payment methods
    'supplier_count': random.randint(15, 25),  # Increase supplier count to 15-25
    'price_volatility': random.uniform(0.10, 0.30),
}

# Fixed asset configuration
INITIAL_fix_asset_CONFIG = {'asset': [
    {"name": "Production Line", "price_range": (200000.00, 30000.00), "life_span": random.randint(3, 20)},
    {"name": "Storage Facilities", "price_range": (150000.00, 250000.00), "life_span": random.randint(3, 20)},
    {"name": "Processing Equipment", "price_range": (200000.00, 400000.00), "life_span": random.randint(3, 20)}
]}  # Reduce fixed asset investment

# Simulation configuration - Increase transaction frequency
INITIAL_simulate_CONFIG = {
    'sale_count_min': 2.00,      # Minimum 4 times per month
    'sale_count_max': 4.00,      # Maximum 8 times per month
    'fixed_asset_min': 1.00,
    'fixed_asset_max': 2.00,
    'purchase_count_min': 2.00,  # Minimum 6 times per month
    'purchase_count_max': 4.00,  # Maximum 10 times per month
    'expense_count_min': 2.00,
    'expense_count_max': 3.00,
    'depreciation_rate': random.uniform(0.10, 0.20),  # Increase depreciation rate
}






