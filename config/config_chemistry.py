# Basic Configuration
import random
INITIAL_seed_CONFIG = {'seed': 322}
INITIAL_transaction_CONFIG = {'transaction': 300}

# Account Related Configuration
ACCOUNT_CONFIG = {
    "initial_cash": 3000000.00,     # 3 million cash
    "initial_bank_deposit": 5000000.00,  # 5 million bank deposit
    "initial_fixed_asset": 5000000.00,   # 5 million fixed assets
}

# Product Configuration - Reduced by 10x
INITIAL_inventory_CONFIG = {'product':[
    {"id": "P001", "name": "Chemical Product A", "cost": 10000.00, "price": 13000.00, "quantity": 0, "status": "On Sale"},
    {"id": "P002", "name": "Chemical Product B", "cost": 20000.00, "price": 26000.00, "quantity": 0, "status": "On Sale"},
    {"id": "P003", "name": "Chemical Product C", "cost": 50000.00, "price": 65000.00, "quantity": 0, "status": "On Sale"},
    {"id": "P004", "name": "Chemical Product D", "cost": 100000.00, "price": 130000.00, "quantity": 0, "status": "On Sale"},
]}

# Transfer Configuration - Reduced by 10x
INITIAL_transfer_CONFIG = {'amount': 100000.00}  # 100k

# Expense Configuration remains unchanged
INITIAL_expense_CONFIG = {
    'amount': 5,  # Increased base value to meet expense ratio requirements
    'weight': [3, 1, 1],  # Ratio for administrative and selling expenses
}

# Sales Configuration - Quantity and customer numbers remain unchanged
INITIAL_sale_CONFIG = {
    'max_quantity': 5.00,  # Quantity per transaction
    'min_profit_margin': 0.20,  # Minimum profit margin 10%
    'max_profit_margin': 0.40,  # Maximum profit margin 40%
    'pay_weight': [0.5, 0.5],  # Cash receipt ratio
    'customer_count': random.randint(10, 20),  # Customer count 10-20
}

# Purchase Configuration - Quantity and supplier numbers remain unchanged
INITIAL_purchase_CONFIG = {
    'max_quantity': 15.00,
    'max_base_quantity': 30.00,
    'min_base_quantity': 5.00,
    'payment_method': [0.3, 0.35, 0.35],
    'supplier_count': random.randint(8, 15),
    'price_volatility': random.uniform(0.20, 0.50),
}

# Fixed Asset Configuration - Reduced by 10x
INITIAL_fix_asset_CONFIG = {'asset': [
    {"name": "Chemical Production Line", "price_range": (300000.00, 500000.00), "life_span": random.randint(5, 30)},
    {"name": "Storage Facilities", "price_range": (200000.00, 400000.00), "life_span": random.randint(5, 30)},
    {"name": "Processing Equipment", "price_range": (300000.00, 600000.00), "life_span": random.randint(5, 30)}
]}

# Simulation Configuration remains unchanged
INITIAL_simulate_CONFIG = {
    'sale_count_min': 1.00,      # Minimum 2 times per month
    'sale_count_max': 2.00,      # Maximum 4 times per month
    'fixed_asset_min': 1.00,
    'fixed_asset_max': 2.00,
    'purchase_count_min': 1.00,  # Minimum 3 times per month
    'purchase_count_max': 3.00,  # Maximum 5 times per month
    'expense_count_min': 2.00,
    'expense_count_max': 4.00,
    'depreciation_rate': random.uniform(0.05, 0.10),  # Increased depreciation rate
}

# Inventory Configuration - Ratios remain unchanged
INVENTORY_CONTROL_CONFIG = {
    'min_inventory_ratio': 0.3,
    'max_inventory_ratio': 0.5,
    'target_turnover_days': 45,
}
