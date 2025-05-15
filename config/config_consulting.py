# config.py

import random
INITIAL_seed_CONFIG = {'seed': 322}

# Reduce transaction frequency
INITIAL_transaction_CONFIG = {'transaction': 200}  # Reduce transaction count to match consulting service characteristics

# Account related configuration remains unchanged
ACCOUNT_CONFIG = {
    "initial_cash": 3000000.00,
    "initial_bank_deposit": 5000000.00,
    "initial_fixed_asset": 5000000.00,
}

# Product configuration - Adjusted for consulting services, increased price differentiation
INITIAL_inventory_CONFIG = {'product':[
    {"id": "S001", "name": "Basic Consulting", "cost": 1000.00, "price": 3000, "quantity": 0, "status": "Available"},
    {"id": "S002", "name": "Standard Consulting", "cost": 5000.00, "price": 15000, "quantity": 0, "status": "Available"},
    {"id": "S003", "name": "Premium Consulting", "cost": 20000.00, "price": 60000, "quantity": 0, "status": "Available"},
    {"id": "S004", "name": "Enterprise Solution", "cost": 100000.00, "price": 800000, "quantity": 0, "status": "Available"},
]}  # Maintain 50-80% gross margin, expand price range to 1000-800k

# Transfer configuration
INITIAL_transfer_CONFIG = {'amount': 100000.00}  # Increase single transaction amount

# Expense configuration - Increase management and sales expense ratio
INITIAL_expense_CONFIG = {
    'amount': 2.00,  # Increase expense baseline
    'weight': [3, 4, 1],  # Increase management and sales expense proportion
}

# Sales configuration - Adjusted to low-frequency high-price model
INITIAL_sale_CONFIG = {
    'max_quantity': 1.00,  # Sell only one service item per transaction
    'min_profit_margin': 0.8,  # Maintain high profit margin
    'max_profit_margin': 2.0,  # Allow higher profit margin
    'pay_weight': [0.3, 0.7],  # Reduce cash payment ratio
    'customer_count': random.randint(5, 20),  # Reduce customer count to 5-20
}

# Purchase configuration (mainly external expert resources for consulting firms)
INITIAL_purchase_CONFIG = {
    'max_quantity': 2.00,
    'max_base_quantity': 3.00,
    'min_base_quantity': 1.00,
    'payment_method': [0.2, 0.5, 0.3],  # Adjust payment methods
    'supplier_count': random.randint(3, 5),  # Reduce supplier (external expert) count to 3-5
    'price_volatility': random.uniform(0.20, 0.50),  # Increase price volatility
}

# Fixed asset configuration - Reduce fixed asset investment
INITIAL_fix_asset_CONFIG = {'asset': [
    {"name": "Office Equipment", "price_range": (50000, 100000), "life_span": random.randint(3, 10)},
    {"name": "IT Infrastructure", "price_range": (100000, 200000), "life_span": random.randint(3, 10)},
    {"name": "Office Furniture", "price_range": (30000, 80000), "life_span": random.randint(3, 10)}
]}  # Asset-light model

# Simulation configuration - Adjusted to low-frequency model
INITIAL_simulate_CONFIG = {
    'sale_count_min': 0,      # Minimum 0 per month
    'sale_count_max': 3.00,      # Maximum 3 per month (corresponding to 0-5 times per week)
    'fixed_asset_min': 0,     # Reduce fixed asset purchase frequency
    'fixed_asset_max': 1.00,
    'purchase_count_min': 0,  # Reduce purchase frequency
    'purchase_count_max': 2.00,
    'expense_count_min': 1.00,   # Maintain stable expense outflow
    'expense_count_max': 2.00,
    'depreciation_rate': random.uniform(0.15, 0.25),  # Accelerate depreciation
}

# Inventory control configuration - Service companies have minimal inventory
INVENTORY_CONTROL_CONFIG = {
    'min_inventory_ratio': 0,    # Minimum inventory ratio 0
    'max_inventory_ratio': 0.05, # Maximum inventory ratio 5%
    'target_turnover_days': 7,   # Rapid turnover
}
