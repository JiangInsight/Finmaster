from datetime import datetime, timedelta
import random
import json
import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config_selector import *


from data_generate import (
    generate_balance_sheet,
    generate_income_statement,
    generate_daily_profit,
    generate_cash_flow_statement,
    generate_auditable_risk_transactions,
    export_to_csv
)
class FinancialStatementGenerator:
    def __init__(self, start_date=None, random_seed=42):
        """Initialize generator"""
        # First create account_balances attribute
        self.account_balances = {}
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.current_date = start_date or datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Initialize basic account balances
        self.account_balances.update({
            "1001": 0,  # Cash on Hand
            "1002": 0,  # Bank Deposits
            "1405": 0,  # Inventory Goods
            "2221": 0,  # Taxes Payable
            "4104": 0,  # Current Year Profit
            "6001": 0,  # Main Business Revenue
            "6401": 0,  # Main Business Cost
            "6601": 0,  # Administrative Expenses
            "6602": 0,  # Sales Expenses
            "6603": 0   # Financial Expenses
        })
        
        # Initialize basic data
        self.chart_of_accounts = self._init_chart_of_accounts()
        self.customers = self._init_customers()
        self.suppliers = self._init_suppliers()
        self.employees = self._init_employees()
        self.inventory = self._init_inventory()
        
        self.initial_cash = ACCOUNT_CONFIG["initial_cash"]
        self.initial_bank_deposit = ACCOUNT_CONFIG["initial_bank_deposit"] # 30 到 100 万
        self.initial_fixed_asset = ACCOUNT_CONFIG["initial_fixed_asset"]
        self.fixed_assets = self._init_fixed_assets()
        self.transactions = []
        self.journal_entries = []
        self.cash_flow_data = []  # Add cash flow data list
        
        # Initialize risk settings
        
        
        # Initialize opening balance
        self._init_opening_balance(start_date)
    def _safe_update_account_balance(self, account_code, amount, is_debit):
        """
        Safely update account balance based on account type and transaction direction
        
        Args:
            account_code (str): The account code to update
            amount (float): The amount to update
            is_debit (bool): Whether the transaction is a debit or credit
        """
        account = self.chart_of_accounts.get(account_code)
        if not account:
            raise ValueError(f"Account code {account_code} does not exist")
        
        account_type = account["type"]
        old_balance = account["balance"]

        if account_type in ["asset", "expense", "cost"]:
            # For asset, expense, and cost accounts: 
            # Debit increases balance, Credit decreases balance
            if is_debit:
                account["balance"] += amount
            else:
                account["balance"] -= amount
        elif account_type in ["liability", "equity", "income", "contra_asset"]:
            # For liability, equity, income, and contra asset accounts:
            # Debit decreases balance, Credit increases balance
            if is_debit:
                account["balance"] -= amount
            else:
                account["balance"] += amount
        else:
            raise ValueError(f"Unknown account type: {account_type}")
        
        # Log the account update
        self._log_account_update(account_code, old_balance, amount, is_debit, account["balance"])

    def _check_balance_sufficient(self, account, amount):
        """
        Check if the account has sufficient balance for a transaction
        
        Args:
            account (dict): The account to check
            amount (float): The amount to be deducted
        
        Raises:
            ValueError: If account data is invalid or balance is insufficient
        """
        if not isinstance(account, dict) or 'code' not in account or 'balance' not in account:
            print('Invalid account data format')
            raise ValueError(f"Account data format error! Received account data: {account}")
        
        if account['balance'] < amount:
            print('Insufficient balance! Bankrupt!')
            raise ValueError(f"Insufficient balance! Account {account['code']} current balance: {account['balance']}, attempting to reduce: {amount}")

    def _log_account_update(self, account_code, old_balance, amount, is_debit, new_balance):
        """
        Log account balance update
        
        Args:
            account_code (str): The account code
            old_balance (float): The balance before update
            amount (float): The transaction amount
            is_debit (bool): Whether the transaction is a debit
            new_balance (float): The balance after update
        """
        direction = "Debit" if is_debit else "Credit"
        print(f"Account {account_code} update successful! " 
            f"Previous balance: {old_balance}, "
            f"{direction} change amount: {'+' if is_debit else '-'}{amount}, "
            f"New balance: {new_balance}")

    def check_accounts_balance(self):
        """
        Check and verify the overall balance of accounts
        
        This method calculates total debits and credits, 
        updates the current year's profit/loss, 
        and checks if the accounts are balanced
        """
        debit_total = 0
        credit_total = 0
        profit_and_loss = 0  # Accumulate net profit or net loss for the period

        for account_code, account in self.chart_of_accounts.items():
            balance = account["balance"]
            account_type = account["type"]

            # Output account balance (optional)
            print(f"Reading account balance: {account_code} - {account['name']}, Balance: {balance}")

            # Additional logic for calculating debit/credit totals can be added here
            # Placeholder for more complex balance calculation logic

        # Update "Current Year Profit" account balance
        if "4104" in self.chart_of_accounts:
            self.chart_of_accounts["4104"]["balance"] = profit_and_loss
            
            # Output net profit information
            if profit_and_loss != 0:
                if profit_and_loss > 0:
                    print(f"Net Profit for the Period: {profit_and_loss}")
                else:
                    print(f"Net Loss for the Period: {abs(profit_and_loss)}")
        else:
            raise ValueError("Account 4104 - Current Year Profit does not exist")

        # Calculate the difference between total debits and credits
        difference = debit_total - credit_total
        if abs(difference) > 0.01:
            print(f"Error: Accounts not balanced! Difference: {difference}")
        else:
            print("Accounts balanced!")

    def _get_account_balance(self, account_code):
        """Get account balance"""
        # Check chart_of_accounts data structure
        if not isinstance(self.chart_of_accounts, dict):
            raise ValueError("chart_of_accounts data structure is incorrect, should be dictionary type")
        
        # Check if account code exists
        if account_code not in self.chart_of_accounts:
            raise ValueError(f"Account code {account_code} does not exist")
        
        # Check if account data is complete
        account = self.chart_of_accounts[account_code]
        if "balance" not in account:
            raise ValueError(f"Account code {account_code} lacks balance field")
        if "name" not in account:
            raise ValueError(f"Account code {account_code} lacks name field")
        
        # Get balance
        balance = account["balance"]
        
        # Debug log
        print(f"Reading account balance: {account_code} - {account['name']}, Balance: {balance}")
        
        return balance

    def _reset_account_balance(self, account):
        """Reset specified account balance to 0"""
        self.account_balances[account] = 0

    def _update_account_balance(self, account, amount):
        """Update specified account balance"""
        self.account_balances[account] = self.account_balances.get(account, 0) + amount


    


    def _init_opening_balance(self,date):
        """Initialize opening balance"""
        # Opening entries
        print(self.initial_bank_deposit,self.initial_fixed_asset)
        opening_entries = [
            {"account": "1001", "debit": self.initial_cash, "credit": 0},      # Cash on Hand
            {"account": "1002", "debit": self.initial_bank_deposit, "credit": 0},      # Bank Deposits
            {"account": "4001", "debit": 0, "credit": self.initial_bank_deposit+self.initial_fixed_asset+self.initial_cash}, 
            {"account": "1601", "debit": self.initial_fixed_asset, "credit": 0},
            # Paid-in Capital
        ]
        
        # Record opening entries
        je_entry = {
            "id": "JE000001",
            "date": self.current_date,
            "transaction_id": "INIT001",
            "description": "Opening Balance",
            "entries": opening_entries,
            "approver": "System Administrator",
            "preparer": "System Administrator",
            "risk_issues": []
        }
        transaction = {
            "id": self.generate_transaction_id(date, "Initial"),
            "type": "Cash deposit",
            "date": date,
            'recorded_date' : date,
            "amount": self.initial_cash,
            'recorded_amount': self.initial_cash,
        }
        self.transactions.append(transaction)
        transaction = {
            "id": self.generate_transaction_id(date, "Initial"),
            "type": "Bank deposit",
            "date": date,
            'recorded_date' : date,
            "amount": self.initial_bank_deposit,
            'recorded_amount': self.initial_bank_deposit,
        }
        self.transactions.append(transaction)
        transaction = {
            "id": self.generate_transaction_id(date, "Initial"),
            "type": "Fixed Assets",
            "date": date,
            'recorded_date' : date,
            "amount": self.initial_fixed_asset,
            'recorded_amount': self.initial_fixed_asset,
        }
        self.transactions.append(transaction)
        # Check if opening entries are balanced
        total_debit = sum(entry["debit"] for entry in opening_entries)
        total_credit = sum(entry["credit"] for entry in opening_entries)
        if total_debit != total_credit:
            raise ValueError(f"Opening entries are not balanced! Total Debit: {total_debit}, Total Credit: {total_credit}")
        
        # Update account balances
        for entry in opening_entries:
            account_code = entry["account"]
            account = self.chart_of_accounts[account_code]
            
            # Determine balance direction based on account type
            if account["type"] in ["asset", "expense"]:
                # Asset and expense accounts: increase with debit, decrease with credit
                balance_change = entry["debit"] - entry["credit"]
            else:
                # Liability, equity, and income accounts: increase with credit, decrease with debit
                balance_change = entry["credit"] - entry["debit"]
                
            self.chart_of_accounts[account_code]["balance"] += balance_change
        
        self.journal_entries.append(je_entry)

    def simulate_fixed_asset_depreciation(self, date):
        """Calculate fixed asset depreciation"""
        return self.calculate_depreciation(date)

    def generate_trial_balance(self, date=None):
        """Generate trial balance"""
        if not date:
            date = self.current_date
            
        trial_balance = {
            "date": date.strftime("%Y-%m-%d"),
            "accounts": [],
            "total_debit": 0,
            "total_credit": 0
        }
        
        for code, account in self.chart_of_accounts.items():
            if account["balance"] != 0:
                balance = account["balance"]
                debit = max(balance, 0)
                credit = abs(min(balance, 0))
                
                trial_balance["accounts"].append({
                    "code": code,
                    "name": account["name"],
                    "type": account["type"],
                    "debit": debit,
                    "credit": credit
                })
                
                trial_balance["total_debit"] += debit
                trial_balance["total_credit"] += credit
        
        return trial_balance

    def export_data(self, filename):
        """Export data to JSON file"""
        data = {
            "chart_of_accounts": self.chart_of_accounts,
            "transactions": self.transactions,
            "journal_entries": self.journal_entries,
            "fixed_assets": self.fixed_assets
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    def _init_chart_of_accounts(self):
        """Initialize chart of accounts"""
        return {
        # Asset Accounts
        "1001": {"code": "1001", "name": "Cash on Hand", "type": "asset", "balance": 0.00},
        "1002": {"code": "1002", "name": "Bank Deposits", "type": "asset", "balance":0.00},
        
        "1221": {"code": "1221", "name": "Other Receivables", "type": "asset", "balance": 0.00},  # New
        "1222": {"code": "1222", "name": "Interest Receivables", "type": "asset", "balance": 0.00},  # New
        "1405": {"code": "1405", "name": "Inventory Goods", "type": "asset", "balance": 0.00},
        "1601": {"code": "1601", "name": "Fixed Assets", "type": "asset", "balance": 0.00},
        "1602": {"code": "1602", "name": "Accumulated Depreciation", "type": "contra_asset", "balance": 0.00},  # Modified type

        # Liability Accounts
        "2202": {"code": "2202", "name": "Accounts Payable", "type": "liability", "balance": 0.00},
        "2221": {"code": "2221", "name": "Taxes Payable", "type": "liability", "balance": 0.00},  # New

        # Equity Accounts
        "4001": {"code": "4001", "name": "Paid-in Capital", "type": "equity", "balance": 0.00},
        "4104": {"code": "4104", "name": "Current Year Profit", "type": "equity", "balance": 0.00},  # Corrected account number

        # Cost Accounts
        "6401": {"code": "6401", "name": "Cost of Main Business", "type": "cost", "balance": 0.00},  # Modified type

        # Expense Accounts
        "6601": {"code": "6601", "name": "Administrative Expenses", "type": "expense", "balance": 0.00},
        "6602": {"code": "6602", "name": "Sales Expenses", "type": "expense", "balance": 0.00},
        "6603": {"code": "6603", "name": "Financial Expenses", "type": "expense", "balance": 0.00},

        # Income Accounts
        "6001": {"code": "6001", "name": "Main Business Revenue", "type": "income", "balance": 0.00},

        
        }

    def _init_inventory(self):
        """Initialize product information with status field"""
        inventory = INITIAL_inventory_CONFIG['product']

        # Calculate total inventory value for each product
        for item in inventory:
            item["total_value"] = item["cost"] * item["quantity"]

        return inventory



    def _init_customers(self):
        """Initialize customer information"""
        return [
            {"id": f"C{i:03d}", "name": f"Customer {i}", "credit_limit": random.randint(50000, 200000)}
            for i in range(1, 21)
        ]

    def _init_suppliers(self):
        """Initialize supplier information"""
        return [
            {"id": f"S{i:03d}", "name": f"Supplier {i}"}
            for i in range(1, 11)
        ]

    def _init_employees(self):
        """Initialize employee information with more details"""
        departments = [
            "Sales", 
            "Finance", 
            "Operations", 
            "Management", 
            "Human Resources", 
            "IT", 
            "Marketing", 
            "Procurement", 
            "Customer Service"
        ]
        
        positions = [
            "Staff", 
            "Junior Staff", 
            "Senior Staff", 
            "Supervisor", 
            "Senior Supervisor", 
            "Manager", 
            "Senior Manager", 
            "Director", 
            "Executive Director"
        ]
        
        seniority_levels = ["Junior", "Mid-level", "Senior", "Executive"]
        
        employees = []
        
        # Generate a more diverse set of employees
        for i in range(1, 101):  # Increased to 100 employees
            department = random.choice(departments)
            position = random.choice(positions)
            seniority = random.choice(seniority_levels)
            
            # Create more realistic employee data
            employee = {
                "id": f"E{i:03d}",
                "name": f"Employee {i}",
                "department": department,
                "position": position,
                "seniority": seniority,
                "email": f"employee{i}@company.com",
                "hire_date": self.current_date - timedelta(days=random.randint(30, 3650)),  # Hired in last 10 years
                "approval_levels": self._determine_approval_levels(position)
            }
            
            employees.append(employee)
        
        return employees
    def _determine_approval_levels(self, position):
        """
        Determine approval levels based on employee position
        
        Returns a dictionary of approval capabilities
        """
        approval_levels = {
            "expense_approval": 0,
            "sales_approval": 0,
            "purchase_approval": 0,
            "fixed_asset_approval": 0
        }
        
        # Define approval capabilities based on position
        if position in ["Staff", "Junior Staff"]:
            # No direct approval, can only prepare
            pass
        
        elif position in ["Senior Staff", "Supervisor"]:
            # Can approve small transactions
            approval_levels["expense_approval"] = 1000000  # Up to 1000
            approval_levels["sales_approval"] = 500000    # Up to 5000
        
        elif position in ["Senior Supervisor", "Manager"]:
            # Can approve medium transactions
            approval_levels["expense_approval"] = 1000000  # Up to 10000
            approval_levels["sales_approval"] = 2000000    # Up to 20000
            approval_levels["purchase_approval"] = 5000000 # Up to 50000
        
        elif position in ["Senior Manager", "Director"]:
            # Can approve larger transactions
            approval_levels["expense_approval"] = 5000000   # Up to 50000
            approval_levels["sales_approval"] = 10000000    # Up to 100000
            approval_levels["purchase_approval"] = 20000000 # Up to 200000
            approval_levels["fixed_asset_approval"] = 50000000 # Up to 500000
        
        elif position in ["Executive Director"]:
            # Can approve almost any transaction
            approval_levels = {
                "expense_approval": 100000000,
                "sales_approval": 100000000,
                "purchase_approval": 100000000,
                "fixed_asset_approval": 100000000
            }
        
        return approval_levels

    def _select_approver(self, transaction_type, amount):
        """
        Intelligently select an approver based on transaction type and amount
        
        Args:
            transaction_type (str): Type of transaction
            amount (float): Transaction amount
        
        Returns:
            dict: Selected approver
        """
        # Map transaction types to approval categories
        approval_map = {
            "Expense": "expense_approval",
            "Sale": "sales_approval",
            "Purchase": "purchase_approval",
            "FixedAsset": "fixed_asset_approval"
        }
        
        approval_category = approval_map.get(transaction_type, None)
        
        if not approval_category:
            raise ValueError(f"Unknown transaction type: {transaction_type}")
        
        # Filter employees who can approve this transaction
        eligible_approvers = [
            emp for emp in self.employees 
            if emp['approval_levels'].get(approval_category, 0) >= amount
        ]
        
        # Prioritize higher positions
        position_priority = [
            "Executive Director1", 
            "Executive Director2", 
            "Director", 
            "Senior Manager", 
            "Manager", 
            "Senior Supervisor"
        ]
        
        for position in position_priority:
            position_approvers = [
                emp for emp in eligible_approvers 
                if emp['position'] == position
            ]
            
            if position_approvers:
                return random.choice(position_approvers)
        
        # Fallback: choose from all eligible approvers
        if eligible_approvers:
            return random.choice(eligible_approvers)
        
        # If no approver found, raise an exception
        raise ValueError(f"No approver found for {transaction_type} of amount {amount}")

    def _select_preparer(self, department):
        """
        Select a preparer from a specific department
        
        Args:
            department (str): Department to select preparer from
        
        Returns:
            dict: Selected preparer
        """
        department_preparers = [
            emp for emp in self.employees 
            if emp['department'] == department and 
            emp['position'] in ["Staff", "Senior Staff", "Supervisor"]
        ]
        
        if department_preparers:
            return random.choice(department_preparers)
        
        # Fallback: choose from Finance department
        finance_preparers = [
            emp for emp in self.employees 
            if emp['department'] == "Finance"
        ]
        
        if finance_preparers:
            return random.choice(finance_preparers)
        
        # Last resort: choose any employee
        return random.choice(self.employees)


    
    def _init_fixed_assets(self):
        """Initialize fixed assets information"""
        return [
            {
                "id": "FA001",
                "name": "Office Building",
                "cost": 5000000,
                "salvage_value": 500000,
                "useful_life": 20,
                "purchase_date": self.current_date - timedelta(days=365),
                "depreciation_method": "straight_line",
                "accumulated_depreciation": 0,  # Added accumulated depreciation field
                "net_value": 5000000  # Added net value field, initially equal to cost
            },
            {
                "id": "FA002",
                "name": "Production Equipment",
                "cost": 2000000,
                "salvage_value": 200000,
                "useful_life": 10,
                "purchase_date": self.current_date - timedelta(days=180),
                "depreciation_method": "straight_line",
                "accumulated_depreciation": 0,
                "net_value": 2000000
            },
            {
                "id": "FA003",
                "name": "Transport Vehicle",
                "cost": 800000,
                "salvage_value": 80000,
                "useful_life": 5,
                "purchase_date": self.current_date - timedelta(days=90),
                "depreciation_method": "straight_line",
                "accumulated_depreciation": 0,
                "net_value": 800000
            }
        ]
    def generate_transaction_id(self, date, type_prefix):
            """
            Generate a unique transaction ID
            
            Args:
                date (datetime): The date of the transaction
                type_prefix (str): Prefix indicating transaction type
            
            Returns:
                str: A unique transaction identifier
            """
            count = len([t for t in self.transactions if t["type"].startswith(type_prefix)])
            return f"{type_prefix}{date.strftime('%Y%m%d')}{count+1:03d}"
    
    def ensure_cash_balance(self,date):
        """
        如果现金账户余额小于 10 万，从银行账户转账 10 万到现金账户。
        """
        # 获取账户余额
        cash = self._get_account_balance("1001") or 0  
        bank = self._get_account_balance("1002") or 0  

        # 转账金额
        transfer_amount = INITIAL_transfer_CONFIG['amount']

        if cash < INITIAL_transfer_CONFIG['amount']:
            if bank >= transfer_amount:
                
                # 执行转账
                cash += transfer_amount
                bank -= transfer_amount
                self._safe_update_account_balance("1001", INITIAL_transfer_CONFIG['amount'], True)  
                
                self._safe_update_account_balance("1002", INITIAL_transfer_CONFIG['amount'], False)  
                # cash = self._get_account_balance("1001") or 0  
                # bank = self._get_account_balance("1002") or 0  
                # print(cash,bank)
                # exit()
                print(f"已从银行账户转账 {transfer_amount} 到现金账户。")
                
                transaction = {
            "id": self.generate_transaction_id(date, "Transfer"),
            "type": "Bank to cash transfer",
            "date": date,
            "recorded_date": date,
            "amount": INITIAL_transfer_CONFIG['amount'],
            "recorded_amount":  INITIAL_transfer_CONFIG['amount']
        }
                self.transactions.append(transaction)
            else:
                print("银行账户余额不足，无法完成转账。")
        elif bank < INITIAL_transfer_CONFIG['amount']:
            if cash >= transfer_amount:
                self._safe_update_account_balance("1002", INITIAL_transfer_CONFIG['amount'], True)  
                self._safe_update_account_balance("1001", INITIAL_transfer_CONFIG['amount'], False) 
                transaction = {
            "id": self.generate_transaction_id(date, "Transfer"),
            "type": "Cash to bank transfer",
            "date": date,
            "recorded_date": date,
            "amount": INITIAL_transfer_CONFIG['amount'],
            "recorded_amount":  INITIAL_transfer_CONFIG['amount']
        }
                self.transactions.append(transaction)
        else:
            print("No need for transfer")

        
        

    def _reset_account_balance(self, account):
        """Reset the balance of a specified account to zero"""
        # Use _safe_update_account_balance method to update balance to 0
        current_balance = self._get_account_balance(account)
        if current_balance > 0:
            self._safe_update_account_balance(account, current_balance, True)  # If credit balance, make a debit entry
        elif current_balance < 0:
            self._safe_update_account_balance(account, abs(current_balance), False)  # If debit balance, make a credit entry
        
        
        
        
        

        
        
    def simulate_expense(self, date):
        """Simulate expense expenditure"""
        import random

        # Generate expense amount (random number between 1000-10000)
        amount = round(random.uniform(INITIAL_expense_CONFIG['amount']*1000, INITIAL_expense_CONFIG['amount']*10000), 2)
        
        # Select an expense account (extended to include contra asset accounts)
        expense_accounts = [
            ("6601", "Administrative Expenses", None),  # No contra asset account
            ("6602", "Sales Expenses", None),  # No contra asset account
            ("6603", "Financial Expenses", None)  # No contra asset account
        ]
        expense_account = random.choices(
    expense_accounts,
    weights=INITIAL_expense_CONFIG['weight'],  
    k=1
)[0]
        approver = self._select_approver("Expense", amount)
        preparer = self._select_preparer("Finance")
        # Get payment_method and balance (if no contra asset account)
        payment_methods = [
            ("1001", "Cash on Hand"),
            ("1002", "Bank Deposits")
        ]
        payment_method = None
        if expense_account[2] is None:  # If no contra asset account, use payment_method
            for method in payment_methods:
                current_balance = self._get_account_balance(method[0])
                if current_balance >= amount:
                    payment_method = method
                    break
            
            # If no payment_method with sufficient balance is found, raise an error
            if not payment_method:
                print('dddd')
                raise ValueError(
                    f"Bankrupt! Insufficient balance! Unable to pay {expense_account[1]}. "
                    f"Required amount: {amount}, Cash on Hand balance: {self._get_account_balance('1001')}, "
                    f"Bank Deposits balance: {self._get_account_balance('1002')}"
                )
        
        # Generate transaction ID
        transaction_id = f"EXP{date.strftime('%Y%m%d')}{str(random.randint(1000, 9999))}"
        
        # Create journal entries
        entries = [
            {
                "account": expense_account[0],  # Debit: expense account
                "debit": amount,
                "credit": 0
            }
        ]
        
        # Credit: based on whether there's a contra asset account
        if expense_account[2]:  # If there's a contra asset account
            entries.append({
                "account": expense_account[2],  # Contra asset account
                "debit": 0,
                "credit": amount
            })
        else:  # Otherwise, use payment_method
            entries.append({
                "account": payment_method[0],  # payment_method account
                "debit": 0,
                "credit": amount
            })
        
        # Create voucher
        je_entry = {
            "id": f"JE{date.strftime('%Y%m%d')}{str(random.randint(1000, 9999))}",
            "date": date,
            "transaction_id": transaction_id,
            "description": f"Pay {expense_account[1]}",
            "entries": entries,
            "approver": approver['position'],
            "preparer": preparer['position'],
            "risk_issues": []
        }
        
        transaction = {
            "id": self.generate_transaction_id(date, "Expense"),
            "type": expense_account[1],
            'payment/receipt_status': 'Paid',
            'payment_method':'Cash',
            "date": date,
            "amount": amount,
            "approver": approver['position'],
            "preparer": preparer['position'],
            'recorded_amount' : amount,
            'recorded_date' : date,
            
            
        }
        self.transactions.append(transaction)
        # Check if journal entries are balanced
        total_debit = sum(entry["debit"] for entry in entries) 
        total_credit = sum(entry["credit"] for entry in entries)
        if abs(total_debit - total_credit) > 0.01:
            raise ValueError(f"Entries not balanced! Total Debit: {total_debit}, Total Credit: {total_credit}")
        
        # Update account balances
        for entry in entries:
            try:
                self._safe_update_account_balance(
                    entry["account"],
                    entry["debit"] if entry["debit"] > 0 else entry["credit"],
                    entry["debit"] > 0
                )
            except ValueError as e:
                # Catch balance update errors and log
                print(f"Balance update failed: {e}")
                raise
        
        # Add to journal
        self.journal_entries.append(je_entry)
        
        # Update cash flow data (only affects cash flow table when using payment_method)
        if not expense_account[2]:  # Only update cash flow table when using payment_method
            self.cash_flow_data.append({
                "date": date,
                "transaction_id": transaction_id,
                "type": "operating",
                "amount": -amount,
                "description": f"Pay {expense_account[1]}"
            })
        
        # Print transaction log (optional, for debugging)
        print(f"\n=== Simulate Expense Expenditure ===")
        print(f"Transaction ID: {transaction_id}")
        print(f"Date: {date}")
        print(f"Expense Account: {expense_account[1]} ({expense_account[0]})")
        if expense_account[2]:
            print(f"Credit Account: {expense_account[2]} (Contra Asset Account)")
        else:
            print(f"payment_method: {payment_method[1]} ({payment_method[0]})")
        print(f"Expenditure Amount: {amount}")
        if not expense_account[2]:
            print(f"Current Balance ({payment_method[1]}): {self._get_account_balance(payment_method[0])}")
    def generate_interest(self,date):
        
        current_balance = self._get_account_balance('1002')
        interest_rate = 0.000089
        account_interest = current_balance*interest_rate
        self._safe_update_account_balance('1222', account_interest, True)
        print(account_interest)
        transaction = {
            "id": self.generate_transaction_id(date, "Interest"),
            "type": 'Interest Receivables',
            'payment/receipt_status': 'Unpaid',
            "date": date,
            "amount": account_interest,
            'receive_method':'Interest receviable',
            'recorded_amount' : account_interest,
            'recorded_date' : date,
            
            
        }
        
        self.transactions.append(transaction)
        
        
        
    def simulate_sales(self, date=None):
        """
        Simulate a sales transaction with inventory and accounting checks
        
        Args:
            date (datetime, optional): Date of the sale. Defaults to current date.
        
        Returns:
            dict or None: A sales transaction or None if no sale is generated
        """
       
        if not date:
            date = self.current_date

        # Reduce sales generation probability
        if random.random() > 0.9:  # 30% chance of generating a sale
            return None

        # Filter products with sufficient inventory
        available_products = [
            p for p in self.inventory 
            if p.get("quantity", 0) > 0 and p.get("quantity", 0) >= 1
        ]

        if not available_products:
            return None  # No sellable products

        # Randomly select product and customer
        product = random.choice(available_products)
        customer = random.choice(self.customers)
        
        # Safe sales quantity calculation
        max_quantity = min(product.get("quantity", 0), INITIAL_sale_CONFIG['max_quantity'])  # Limit maximum sales quantity
        
        if max_quantity <= 0:
            return None
        
        quantity = random.randint(1, max_quantity)
        
        # Cost and pricing calculation
        cost_per_unit = product.get("cost", 0)
        
        # Conservative profit margin
        min_profit_margin = INITIAL_sale_CONFIG['min_profit_margin']  # Minimum profit margin 10%
        max_profit_margin = INITIAL_sale_CONFIG['max_profit_margin']   # Maximum profit margin 35%
        
        profit_margin = random.uniform(min_profit_margin, max_profit_margin)
        unit_price = round(cost_per_unit * (1 + profit_margin), 2)
        
        
        # Amount calculations
        amount = round(quantity * unit_price, 2)
        tax_rate = 0.05
        tax_amount = round(amount * tax_rate, 2)
        total_amount = round(amount - tax_amount, 2)
        total_cost = round(quantity * cost_per_unit, 2)

        # Safe inventory reduction function
        def safe_inventory_reduction(inventory, product_id, quantity):
            for item in inventory:
                if item["id"] == product_id:
                    # Ensure no negative inventory
                    if item.get("quantity", 0) >= quantity:
                        item["quantity"] -= quantity
                        return True
            return False

        # Execute inventory reduction
        if not safe_inventory_reduction(self.inventory, product["id"], quantity):
            return None  # Inventory reduction failed

        # Accounting entries
        entries = [
            {"account": "6001", "debit": 0, "credit": amount},        # Credit: Main Business Revenue
            {"account": "2221", "debit": 0, "credit": tax_amount},    # Credit: Taxes Payable
            {"account": "6401", "debit": total_cost, "credit": 0},    # Debit: Main Business Cost
            {"account": "1405", "debit": 0, "credit": total_cost}     # Credit: Inventory Goods
        ]

        # Update account balances
        for entry in entries:
            account = entry["account"]
            debit = entry["debit"]
            credit = entry["credit"]
            
            if debit > 0:
                self._safe_update_account_balance(account, debit, True)
            if credit > 0:
                self._safe_update_account_balance(account, credit, False)
        payment_method = random.choices(['cash', 'unpaid'], weights=INITIAL_sale_CONFIG['pay_weight'])[0]
        
        # Update current year profit
        net_profit_change = amount - total_cost - tax_amount 
        self._safe_update_account_balance("4104", abs(net_profit_change), net_profit_change > 0)  
        if payment_method == "cash":
            self._safe_update_account_balance("1001", total_amount+ tax_amount, True)

            entries.append({"account": "1001", "debit": 0, "credit": total_amount})  # 
            transaction = {
            "id": self.generate_transaction_id(date, "Sale"),
            "type": "Sale",
            'receive_method':'Cash',
            'payment/receipt_status': 'Paid',
            "date": date,
            'cost_per_unit': cost_per_unit,
            'recorded_date' : date,
            "customer_id": customer["id"],
            "product_id": product["id"],
            'unit_price':unit_price,
            'product_name':product["name"],
            "quantity": quantity,
            "amount": amount,
            'recorded_amount': amount,
            "tax_amount": tax_amount,
            "after_tax_amount": total_amount,
            "cost_amount": total_cost,
            "profit": amount - total_cost,
        }
        else:
            self._safe_update_account_balance("1221", total_amount+ tax_amount, True)  # 增加应付账款
            transaction = {
            "id": self.generate_transaction_id(date, "Sale"),
            "type": "Sale",
            'receive_method':'Account Receviable',
            'payment/receipt_status': 'Unpaid',
            'cost_per_unit': cost_per_unit,
            "date": date,
            'recorded_date' : date,
            "customer_id": customer["id"],
            "product_id": product["id"],
            'unit_price':unit_price,
            'product_name':product["name"],
            "quantity": quantity,
            "amount": amount,
            'recorded_amount': amount,
            "tax_amount": tax_amount,
            "after_tax_amount": total_amount,
            "cost_amount": total_cost,
            "profit": amount - total_cost,
        }
        self.transactions.append(transaction)
        return transaction




    def simulate_purchase(self, date=None):
        """Generate a Purchase Transaction"""
        if not date:
            date = self.current_date

        # 2% chance of generating a purchase

        # Basic information setup
        
        transaction_id = self.generate_transaction_id(date, "Purchase")
        supplier = random.choice(self.suppliers)
        product = random.choice(self.inventory)
       
        
        # Determine purchase quantity (based on current inventory)
        current_quantity = product.get("quantity", 0)
        print(current_quantity, 'sssssssssssssssssssssssssss')
        
        if random.random() > 0.9:
            return None
        
        if current_quantity > INITIAL_purchase_CONFIG['max_quantity']:  # Reduce purchase probability when inventory is sufficient
            return None
            
        base_quantity = random.randint(INITIAL_purchase_CONFIG['min_base_quantity'], INITIAL_purchase_CONFIG['max_base_quantity'])
        quantity = base_quantity
        approver = self._select_approver("Expense",quantity)
        preparer = self._select_preparer("Finance")
        # Price and amount calculation
        cost_per_unit = product.get("cost", 0)
        # Purchase price fluctuation ±5%
        purchase_price = round(cost_per_unit, 2)

        # Calculate total amount
        amount = round(quantity * purchase_price, 2)
        total_amount = round(amount , 2)

        # Risk handling
        risk_issues = []
        recorded_amount = total_amount
        recorded_date = date
        
  

        # Update inventory
        for item in self.inventory:
            if item["id"] == product["id"]:
                item["quantity"] += quantity
                break
        payment_method = random.choice(["cash", "bank_transfer", "unpaid"])
        payment_method = random.choices(['cash', 'bank_transfer','unpaid'], weights=INITIAL_purchase_CONFIG['payment_method'])[0]
        # Create accounting entries
        entries = [
            {"account": "1405", "debit": amount, "credit": 0}       # Inventory Goods
           
        ]

        # Update account balances
        self._safe_update_account_balance("1405", amount, True)       # Increase inventory
        if payment_method == "cash":
            self._safe_update_account_balance("1001", total_amount, False) 

            entries.append({"account": "1001", "debit": 0, "credit": total_amount})  # 
            transaction = {
            "id": transaction_id,
            "type": "Purchase",
            "date": date,
            'cost_per_unit': cost_per_unit,
            'approver': approver['position'],
            'preparer': preparer['position'],
            'payment/receipt_status': 'Paid',
            'payment_method': 'Cash',
            'cost_per_unit': purchase_price,
            "recorded_date": recorded_date,
            "supplier_id": supplier["id"],
            "supplier_name": supplier["name"],
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": purchase_price,
            "amount": amount,
            "recorded_amount": recorded_amount,
          
        }
        elif payment_method == "bank_transfer":
            self._safe_update_account_balance("1002", total_amount, False) 
            entries.append({"account": "1002", "debit": 0, "credit": total_amount})  # Bank Account
            transaction = {
            "id": transaction_id,
            "type": "Purchase",
            "date": date,
            'approver': approver['position'],
            'preparer': preparer['position'],
             'payment/receipt_status': 'Paid',
             'payment_method': 'Bank Transfer',
             'cost_per_unit': cost_per_unit,
            "recorded_date": recorded_date,
            "supplier_id": supplier["id"],
            "supplier_name": supplier["name"],
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": purchase_price,
            "amount": amount,
            "recorded_amount": recorded_amount,
           
        }
        else:
            self._safe_update_account_balance("2202", total_amount, False) 

            entries.append({"account": "2202", "debit": 0, "credit": total_amount})  # Accounts Payable
            transaction = {
            "id": transaction_id,
            "type": "Purchase",
            "date": date,
            'approver': approver['position'],
            'preparer': preparer['position'],
            'payment/receipt_status': 'Unpaid',
            'cost_per_unit': cost_per_unit,
             'payment_method': 'Account Payable',
            "recorded_date": recorded_date,
            "supplier_id": supplier["id"],
            "supplier_name": supplier["name"],
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": purchase_price,
            "amount": amount,
            "recorded_amount": recorded_amount,
            
        }
        

        # Create transaction record
        

        # Create journal entry record
        je_entry = {
            "id": f"JE{len(self.journal_entries) + 1:06d}",
            "date": recorded_date,
            "transaction_id": transaction_id,
            "description": f"Purchase {quantity} {product['name']} from {supplier['name']}",
            "entries": entries,
            "approver": random.choice([emp["name"] for emp in self.employees if emp["position"] in ["Manager", "Supervisor"]]),
            "preparer": random.choice([emp["name"] for emp in self.employees if emp["department"] == "Finance"]),
           
        }

        # Save records
        self.transactions.append(transaction)
        self.journal_entries.append(je_entry)

        return transaction


    def generate_fixed_asset_purchase(self, date=None):
        
        """Generate Fixed Asset Purchase Transaction"""
        if not date:
            date = self.current_date

        # 0.5% chance of generating a fixed asset purchase
        if random.random() > 0.05:
            return None

        # Basic information setup
        transaction_id = self.generate_transaction_id(date, "FixedAsset")
        supplier = random.choice(self.suppliers)
        
        # Fixed asset information
        asset_types = INITIAL_fix_asset_CONFIG['asset']
        
        asset_type = random.choice(asset_types)
        asset_name = f"{asset_type['name']}{len(self.fixed_assets) + 1}"
        amount = round(random.uniform(*asset_type["price_range"]), 2)
        
        # Calculate tax amount
        tax_rate = 0.05
        total_amount = round(amount , 2)

        # Risk handling

        recorded_amount = total_amount
        recorded_date = date

        # Create accounting entries
        entries = [
            {"account": "1601", "debit": amount, "credit": 0},       # Fixed Assets
            {"account": "1002", "debit": 0, "credit": total_amount}  # Bank Deposits
        ]

        # Update account balances
        self._safe_update_account_balance("1601", amount, True)       # Increase fixed assets
        self._safe_update_account_balance("1002", total_amount, False) # Decrease bank deposits

            
        # Add to fixed assets list
        asset = {
            "id": f"FA{len(self.fixed_assets) + 1:03d}",
            "name": asset_name,
            "type": asset_type["name"],
            "purchase_date": date,
            "cost": amount,
            "accumulated_depreciation": 0,
            "net_value": amount,  # Initial net value equals cost
            "useful_life": random.randint(3, 10),  # Useful life 3-10 years
            "salvage_value": round(amount * 0.05, 2),  # Salvage value 5%
            "depreciation_method": "straight_line"
        }
        self.fixed_assets.append(asset)

        # Create transaction record
        transaction = {
            "id": transaction_id,
            "type": "Fixed Assets Purchase",
            'payment_method': 'Bank Transfer',
            "date": date,
            'payment/receipt_status': 'Paid',
            "recorded_date": recorded_date,
            "supplier_id": supplier["id"],
            "supplier_name": supplier["name"],
            "asset_name": asset_name,
            "asset_type": asset_type["name"],
            "amount": amount,
            "recorded_amount": recorded_amount,

        }

        # Create journal entry record
        je_entry = {
            "id": f"JE{len(self.journal_entries) + 1:06d}",
            "date": recorded_date,
            "transaction_id": transaction_id,
            "description": f"Purchase {asset_name}",
            "entries": entries,
            "approver": random.choice([emp["name"] for emp in self.employees if emp["position"] in ["Manager", "Supervisor"]]),
            "preparer": random.choice([emp["name"] for emp in self.employees if emp["department"] == "Finance"]),

        }

        # Save records
        self.transactions.append(transaction)
        self.journal_entries.append(je_entry)

        return transaction

    def calculate_depreciation(self, date=None):
        """
        Calculate Fixed Asset Depreciation, Introducing Uncertainty Factors

        Sources of Uncertainty:
        1. Slight depreciation rate fluctuation
        2. Asset usage condition
        3. Seasonal factors
        4. Risk adjustments
        """
        if not date:
            date = self.current_date

        # Calculate last month's depreciation on the 1st of each month
        

        total_depreciation = 0
        for asset in self.fixed_assets:
            # Skip assets that have been fully depreciated
            if asset["net_value"] <= asset["salvage_value"]:
                continue

            # Introduce uncertainty factors
            def calculate_uncertain_depreciation(asset):
                # Basic depreciation calculation
                useful_life_months = asset["useful_life"] * 12
                base_depreciation = (asset["cost"] - asset["salvage_value"]) / useful_life_months

                # 1. Asset usage condition uncertainty
                usage_factor = {
                    "Good": random.uniform(0.9990, 1.0001),
                    "Average": random.uniform(0.9998, 1.0002),
                    "Poor": random.uniform(0.9995, 1.0005)
                }.get(asset.get("condition", "Average"), 1.0)

                # 2. Seasonal adjustment
                seasonal_factors = {
                    1: random.uniform(0.9998, 1.0002),   # Winter may have different wear
                    7: random.uniform(0.9999, 1.0001),   # Summer heat may affect
                }
                seasonal_factor = seasonal_factors.get(date.month, 1.0)

                # 3. Risk premium
                risk_premium = {
                    "Low Risk": random.uniform(0.9999, 1.0001),
                    "Medium Risk": random.uniform(0.9997, 1.0003),
                    "High Risk": random.uniform(0.9995, 1.0005)
                }.get(asset.get("risk_level", "Low Risk"), 1.0)

                # 4. Equipment age decay factor
                age_factor = max(0.995, 1 - (asset.get("age", 0) * 0.002))

                # Comprehensive uncertainty calculation
                uncertain_depreciation = base_depreciation * usage_factor * seasonal_factor * risk_premium * age_factor
                
                return round(uncertain_depreciation, 2)

            # Calculate monthly depreciation (with uncertainty)
            monthly_depreciation = calculate_uncertain_depreciation(asset)

            # Ensure not to depreciate below salvage value
            remaining_depreciable = asset["net_value"] - asset["salvage_value"]
            if monthly_depreciation > remaining_depreciable:
                monthly_depreciation = remaining_depreciable
           
            
            # Update asset book value
            asset["accumulated_depreciation"] += monthly_depreciation
            asset["net_value"] -= monthly_depreciation
            total_depreciation += monthly_depreciation

            # Record uncertainty information
            asset["last_depreciation_factors"] = {
                "date": date,
                "depreciation_amount": monthly_depreciation,
                "usage_condition": asset.get("condition", "Average"),
                "risk_level": asset.get("risk_level", "Low Risk")
            }

        if total_depreciation > 0:
            # Create depreciation accounting entry
            transaction_id = self.generate_transaction_id(date, "Depreciation")
            entries = [
               
                {"account": "1602", "debit": 0, "credit": total_depreciation}     # Accumulated Depreciation
            ]

            # Update account balances
            self._safe_update_account_balance("1602", total_depreciation, is_debit=False)

            # Create journal entry record
            je_entry = {
                "id": f"JE{len(self.journal_entries) + 1:06d}",
                "date": date,
                "transaction_id": transaction_id,
                "description": f"Fixed Asset Depreciation for {date.strftime('%Y-%m')}",
                "entries": entries,
                "approver": random.choice([emp["name"] for emp in self.employees if emp["position"] in ["Manager", "Supervisor"]]),
                "preparer": random.choice([emp["name"] for emp in self.employees if emp["department"] == "Finance"]),
                "uncertainty_metrics": {
                    "total_depreciation": total_depreciation,
                    "variation_range": f"{min(0.995, 1.005):.2%}"
                }
            }
            
            transaction = {
                "id": transaction_id,
                'type' : 'depreciation',
                "date": date,
                "description": f"Fixed Asset Depreciation for {date.strftime('%Y-%m')}",
                "entries": entries,
                "approver": random.choice([emp["name"] for emp in self.employees if emp["position"] in ["Manager", "Supervisor"]]),
                "preparer": random.choice([emp["name"] for emp in self.employees if emp["department"] == "Finance"]),
                "uncertainty_metrics": {
                    "total_depreciation": total_depreciation,
                    "variation_range": f"{min(0.995, 1.005):.2%}"
                }
            }
            transaction = {
            "id": transaction_id,
            "type": "Depreciation",
            "date": date,
            "recorded_date": date,
            "amount": total_depreciation,
            "recorded_amount": total_depreciation
        }
            self.journal_entries.append(je_entry)
            self.transactions.append(transaction)
        return total_depreciation






    def simulate_day(generator,self, date=None):
        print('ssss')
        """Simulate Business Operations for a Day"""
        if date is None:
            date = self.current_date
            
        try:
            # Check Initial Balance
            self.check_accounts_balance()
            
            # Simulate 10-40 Sales
            sales_count = random.randint(INITIAL_simulate_CONFIG['sale_count_min'], INITIAL_simulate_CONFIG['sale_count_max'])
            for i in range(sales_count):
                try:
                    self.simulate_sales(date)
                    self.check_accounts_balance()
                except ValueError as e:
                    print(f"Sales Transaction {i+1}/{sales_count} Encountered an Issue")
                    raise
            print('print(abs(self.chart_of_accounts["1601"]["balance"]))',abs(self.chart_of_accounts["1601"]["balance"]))
            # Simulate 1-3 Fixed Asset Purchases
            fixed_asset = random.randint(INITIAL_simulate_CONFIG['fixed_asset_min'], INITIAL_simulate_CONFIG['fixed_asset_max'])
            for i in range(fixed_asset):
                try:
                    self.generate_fixed_asset_purchase()
                except ValueError as e:
                    print(f"Fixed Asset Purchase Transaction {i+1}/{fixed_asset} Encountered an Issue")
                    raise
            
            # Simulate 10-40 Purchases
            purchase = random.randint(INITIAL_simulate_CONFIG['purchase_count_min'], INITIAL_simulate_CONFIG['purchase_count_max'])
            for i in range(purchase):
                generator.ensure_cash_balance(date)
                try:
                    self.simulate_purchase()
                except ValueError as e:
                    print(f"Purchase Transaction {i+1}/{purchase} Encountered an Issue")
                    raise
                    
            # Simulate 1-2 Expense Transactions
            expense_count = random.randint(INITIAL_simulate_CONFIG['expense_count_min'], INITIAL_simulate_CONFIG['expense_count_max'])
            for i in range(expense_count):
                generator.ensure_cash_balance(date)
                try:
                    self.simulate_expense(date)
                    self.check_accounts_balance()
                except ValueError as e:
                    print(f"Expense Transaction {i+1}/{expense_count} Encountered an Issue")
                    raise
                    
            # Calculate Depreciation on the First Day of the Month
            if date.day == 1:
                try:
                    generator.ensure_cash_balance(date)
                    self.simulate_fixed_asset_depreciation(date)
                    self.check_accounts_balance()
                except ValueError as e:
                    print("Depreciation Calculation Encountered an Issue")
                    raise
                        
        except ValueError as e:
            print(f"Business Simulation for Date {date.strftime('%Y-%m-%d')} Encountered an Issue")
            raise

