import random
INITIAL_seed_CONFIG = {'seed': 322}

# Increase transaction frequency
INITIAL_transaction_CONFIG = {'transaction': 200}  # Increase transaction count for F&B characteristics

# Account configuration adjustments
ACCOUNT_CONFIG = {
    "initial_cash": 3000000.00,
    "initial_bank_deposit": 5000000.00,
    "initial_fixed_asset": 8000000.00,  # Increase initial fixed assets for capital-intensive business
}

# Product configuration - Adjusted for F&B products, lower unit price, more varieties
INITIAL_inventory_CONFIG = {'product':[
    {"id": "F001", "name": "Quick Meal Set", "cost": 150.00, "price": 280, "quantity": 0, "status": "Available"},
    {"id": "F002", "name": "Business Meal Set", "cost": 350.00, "price": 680, "quantity": 0, "status": "Available"},
    {"id": "F003", "name": "Deluxe Meal Set", "cost": 880.00, "price": 1680, "quantity": 0, "status": "Available"},
    {"id": "F004", "name": "Banquet Set", "cost": 2880, "price": 5880, "quantity": 0, "status": "Available"},
    {"id": "R001", "name": "Standard Room", "cost": 1500, "price": 2880, "quantity": 0, "status": "Available"},
    {"id": "R002", "name": "Business Room", "cost": 2000, "price": 3880, "quantity": 0, "status": "Available"},
    {"id": "R003", "name": "Luxury Suite", "cost": 5000, "price": 9880, "quantity": 0, "status": "Available"},
]}  # Maintain 30-80% gross margin

# Transfer configuration
INITIAL_transfer_CONFIG = {'amount': 50000.00}  # Lower single transaction amount

# Expense configuration - Increase management and selling expense ratio
INITIAL_expense_CONFIG = {
    'amount': 0.1,  # Increase expense baseline
    'weight': [4, 3, 1],  # Increase management and selling expense proportion
}

# Sales configuration - Adjust to high-frequency, low-price model
INITIAL_sale_CONFIG = {
    'max_quantity': 5.00,  # Multiple products per sale
    'min_profit_margin': 0.3,  # Lower minimum profit margin
    'max_profit_margin': 0.8,  # Lower maximum profit margin
    'pay_weight': [0.6, 0.4],  # Increase cash payment ratio
    'customer_count': random.randint(20, 50),  # Increase customer count to 20-50
}

# Purchase configuration
INITIAL_purchase_CONFIG = {
    'max_quantity': 500.00,  # Increase single purchase quantity
    'max_base_quantity': 300.00,
    'min_base_quantity': 100.00,
    'payment_method': [0.2, 0.2, 0.6],  # Adjust payment methods
    'supplier_count': random.randint(15, 25),  # Increase supplier count to 15-25
    'price_volatility': random.uniform(0.10, 0.30),  # Lower price volatility
}

# Fixed asset configuration - Increase fixed asset investment
INITIAL_fix_asset_CONFIG = {'asset': [
    {"name": "Kitchen Equipment", "price_range": (200000, 500000), "life_span": random.randint(5, 10)},
    {"name": "Room Facilities", "price_range": (300000, 800000), "life_span": random.randint(8, 15)},
    {"name": "Renovation Project", "price_range": (1000000, 2000000), "life_span": random.randint(5, 10)},
    {"name": "Central AC", "price_range": (500000, 1000000), "life_span": random.randint(10, 20)},
    {"name": "Elevator System", "price_range": (400000, 800000), "life_span": random.randint(15, 20)}
]}  # Capital-intensive model

# Simulation configuration - Adjust to high-frequency mode
INITIAL_simulate_CONFIG = {
    'sale_count_min': 2.00,      # Minimum 4 times per month
    'sale_count_max': 4.00,      # Maximum 8 times per month
    'fixed_asset_min': 0,     # Increase fixed asset purchase frequency
    'fixed_asset_max': 2.00,
    'purchase_count_min': 1.00,  # Increase purchase frequency
    'purchase_count_max': 3.00,
    'expense_count_min': 1.00,   # Increase expense frequency
    'expense_count_max': 2.00,
    'depreciation_rate': random.uniform(0.05, 0.15),  # Lower depreciation rate
}

# Inventory control configuration - Adapted for F&B business
INVENTORY_CONTROL_CONFIG = {
    'min_inventory_ratio': 0.05,  # Minimum inventory ratio 5%
    'max_inventory_ratio': 0.15,  # Maximum inventory ratio 15%
    'target_turnover_days': 3,    # Rapid turnover
}
