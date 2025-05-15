from datetime import datetime, timedelta
import random
import json
import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def format_numbers(x):
    if isinstance(x, (int, float)): 
        return f"{x:.2f}" 
    return x 
def generate_balance_sheet(self, date=None):
    """Generate Balance Sheet"""
    if not date:
        date = self.current_date

    # Define balance sheet date
    report_date = date.strftime("%Y-%m-%d")

    # Create data lists
    asset_items = []
    liability_and_equity_items = []

    # Current Assets
    current_assets = [
        ("Cash on Hand", round((self.chart_of_accounts["1001"]["balance"]),2)),
        ("Bank Deposits", round((self.chart_of_accounts["1002"]["balance"]),2)),
        ("Interest Receivable", round(abs(self.chart_of_accounts["1222"]["balance"]),2)),
        ("Accounts Receivable", round(abs(self.chart_of_accounts["1221"]["balance"]),2)),
        ("Inventory", round(abs(self.chart_of_accounts["1405"]["balance"]),2))
    ]
    print(abs(self.chart_of_accounts["1221"]["balance"]))
    total_current_assets = round(sum([item[1] for item in current_assets]),2)
    
    asset_items.extend(current_assets)
    asset_items.append(("Total Current Assets", total_current_assets))
    print(self.chart_of_accounts["1601"])
    # Non-current Assets
    fixed_assets = round(abs(self.chart_of_accounts["1601"]["balance"]),2)
    accumulated_depreciation = round(abs(self.chart_of_accounts["1602"]["balance"]),2)

    # Corrected calculation method
    total_fixed_assets = round(fixed_assets - accumulated_depreciation,2)

    non_current_assets = [
        ("Fixed Assets", round(fixed_assets,2)),
        ("Accumulated Depreciation", round(accumulated_depreciation,2)),
        ("Total Non-current Assets", round(abs(total_fixed_assets),2))
    ]
    asset_items.extend(non_current_assets)

    # Total Assets
    total_assets = round(total_current_assets + abs(total_fixed_assets),2)
    asset_items.append(("Total Assets", total_assets))

    # Current Liabilities
    current_liabilities = [
        ("Accounts Payable", round(abs(self.chart_of_accounts["2202"]["balance"]),2)),
        ("Taxes Payable", round(abs(self.chart_of_accounts["2221"]["balance"]),2))
    ]
    
    total_current_liabilities = round(abs(self.chart_of_accounts["2202"]["balance"]) + abs(self.chart_of_accounts["2221"]["balance"]),2)
    liability_and_equity_items.extend(current_liabilities)
    liability_and_equity_items.append(("Total Current Liabilities", total_current_liabilities))

    # Revenue calculation (for net profit)
    revenue_items = [
        ("Main Business Revenue", self.chart_of_accounts["6001"]["balance"]),
        # ("Other receviable", round(abs(self.chart_of_accounts["1221"]["balance"]),2)),
        ("Interest receviable", round(abs(self.chart_of_accounts["1222"]["balance"]),2))
    ]
    total_revenue = round(sum([item[1] for item in revenue_items]),2)

    # Cost calculation
    cost_items = [
        ("Main Business Cost", -abs(self.chart_of_accounts["6401"]["balance"]))
    ]
    total_costs = round(sum([item[1] for item in cost_items]),2)

    # Expense calculation
    expense_items = [
        ("Administrative Expenses", round(-abs(self.chart_of_accounts["6601"]["balance"]))),
        ("Sales Expenses", round(-abs(self.chart_of_accounts["6602"]["balance"]))),
        ("Financial Expenses", round(-abs(self.chart_of_accounts["6603"]["balance"]))),
        
        ("Accumulated Depreciation", round(-abs(self.chart_of_accounts["1602"]["balance"])))
        
    ]
    total_expenses = round(sum([item[1] for item in expense_items]),2)

    # Other gains and losses
    

    # Profit calculation
    operating_profit = round(total_revenue + total_costs + total_expenses,2)
    revenue_items = [
 ("Main Business Revenue", round(abs(self.chart_of_accounts["6001"]["balance"]),2))
]
    total_revenue = round(sum([item[1] for item in revenue_items]),2)
    cost_items = [
("Cost of Goods Sold", abs(self.chart_of_accounts["6401"]["balance"]))
]
    total_costs = round(sum([item[1] for item in cost_items]),2)
    expense_items = [
("Administrative Expenses", round(abs(self.chart_of_accounts["6601"]["balance"]),2)),
("Selling Expenses", round(abs(self.chart_of_accounts["6602"]["balance"]),2)),
 ("Depreciation", round(abs(self.chart_of_accounts["1602"]["balance"]),2))
]
    total_expenses = round(sum([item[1] for item in expense_items]) + round(abs(self.chart_of_accounts["6603"]["balance"]),2),2)
    operating_profit = round(total_revenue - total_costs - total_expenses +round(abs(self.chart_of_accounts["1222"]["balance"]),2),2)
    net_profit = operating_profit - self.chart_of_accounts["2221"]["balance"]
    # Owner's Equity
    equity = [
        ("Paid-in Capital", round(abs(self.chart_of_accounts["4001"]["balance"]))),
        ("Retained Earnings", round(net_profit,2))
    ]
    total_equity = round(sum([item[1] for item in equity]),2)
    liability_and_equity_items.extend(equity)
    liability_and_equity_items.append(("Total Owner's Equity", round(total_equity,2)))
    # Total Liabilities and Owner's Equity
    total_liabilities_and_equity = round(total_current_liabilities + total_equity,2)
    liability_and_equity_items.append(("Total Liabilities and Owner's Equity", round(total_liabilities_and_equity,2)))

    # Convert data to DataFrame
    assets_df = pd.DataFrame(asset_items, columns=["Account", "Amount"])
    liabilities_and_equity_df = pd.DataFrame(liability_and_equity_items, columns=["Account", "Amount"])

    # Add date
    assets_df["Date"] = report_date
    liabilities_and_equity_df["Date"] = report_date

    return assets_df, liabilities_and_equity_df

def generate_income_statement(self, end_date=None):
    """
    Generate Income Statement for the specified end_date.

    Args:
        end_date (datetime, optional): The end date of the income statement period.

    Returns:
        pd.DataFrame: A DataFrame representing the income statement.transaction
    """
    # Define the reporting period
    report_period = end_date.strftime("%Y-%m-%d") if end_date else self.current_date.strftime("%Y-%m-%d")

    # Initialize the list to store income statement items
    income_statement_items = []

    # Revenue section
    revenue_items = [
        ("Main Business Revenue", round(abs(self.chart_of_accounts["6001"]["balance"]),2))
    ]
    total_revenue = round(sum([item[1] for item in revenue_items]),2)
    income_statement_items.extend(revenue_items)
    income_statement_items.append(("Total Revenue", round(abs(self.chart_of_accounts["6001"]["balance"]),2)))

    # Cost section
    cost_items = [
        ("Cost of Goods Sold", abs(self.chart_of_accounts["6401"]["balance"]))
    ]
    total_costs = round(sum([item[1] for item in cost_items]),2)
    income_statement_items.extend(cost_items)
    income_statement_items.append(("Total Cost", total_costs))
    income_statement_items.append(("Gross Profit", round((total_revenue - total_costs),2)))
    # Expense section
    expense_items = [
        ("Administrative Expenses", round(abs(self.chart_of_accounts["6601"]["balance"]),2)),
        ("Selling Expenses", round(abs(self.chart_of_accounts["6602"]["balance"]),2)),
            ("Depreciation", round(abs(self.chart_of_accounts["1602"]["balance"]),2))
    ]
    income_statement_items.extend(expense_items)
    income_statement_items.append(("Financial Expenses", round(abs(self.chart_of_accounts["6603"]["balance"]),2)))

  
    total_expenses = round(sum([item[1] for item in expense_items]) + round(abs(self.chart_of_accounts["6603"]["balance"]),2),2)
    
    
    income_statement_items.append(("Total Expenses", total_expenses))
    income_statement_items.append(("Interest Income", round(abs(self.chart_of_accounts["1222"]["balance"]),2)))
    
    # Calculate operating profit
    operating_profit = round(total_revenue - total_costs - total_expenses +round(abs(self.chart_of_accounts["1222"]["balance"]),2),2)
    income_statement_items.append(("Profit Before Tax", round(operating_profit,2)))
    income_statement_items.append(("Tax Expense", round(abs(self.chart_of_accounts["2221"]["balance"]),2)))
    # Calculate net profit
    net_profit = operating_profit -  self.chart_of_accounts["2221"]["balance"] # Assuming no other gains/losses for simplicity
    income_statement_items.append(("Net Profit", net_profit))

    # Convert the list to a DataFrame
    income_statement_df = pd.DataFrame(income_statement_items, columns=["Account", "Amount"])

    # Add the report period to the DataFrame
    income_statement_df["Date"] = report_period

    return income_statement_df

def generate_daily_profit(self):
    income_statement_items = []
    revenue_items = [
        ("Main Business Revenue", abs(self.chart_of_accounts["6001"]["balance"])),
            ("Interest receviable", round(abs(self.chart_of_accounts["1222"]["balance"]),2))
    #   ("Other receviable", round(abs(self.chart_of_accounts["1221"]["balance"]),2))
    ]
    total_revenue = sum([item[1] for item in revenue_items])
    income_statement_items.extend(revenue_items)
    income_statement_items.append(("Total Revenue", round(total_revenue,2)))

    # Cost section
    cost_items = [
        ("Main Business Cost", abs(self.chart_of_accounts["6401"]["balance"]))
    ]
    total_costs = sum([item[1] for item in cost_items])
    income_statement_items.extend(cost_items)
    income_statement_items.append(("Total Cost", round(total_costs,2)))

    # Expense section
    expense_items = [
        ("Administrative Expenses", abs(self.chart_of_accounts["6601"]["balance"])),
        ("Sales Expenses", abs(self.chart_of_accounts["6602"]["balance"])),
        ("Financial Expenses", abs(self.chart_of_accounts["6603"]["balance"]))
    ]
    total_expenses = sum([item[1] for item in expense_items])
    income_statement_items.extend(expense_items)
    income_statement_items.append(("Total Expenses", round(total_expenses,2)))

    # Other gains and losses
    
    
    operating_profit = total_revenue - total_costs - total_expenses  # Operating Profit = Revenue - Cost - Expenses
    net_profit = operating_profit  # Net Profit = Operating Profit + Total Other Gains and Losses
    return net_profit
    
    
    
    
    
    

def generate_cash_flow_statement(self, date=None):
    """
    Generate Cash Flow Statement with detailed calculation logic
    
    Args:
        date (datetime, optional): Date for the cash flow statement. Defaults to the current date.
    Returns:
        pd.DataFrame: DataFrame containing the cash flow statement
    """
    if not date:
        date = self.current_date

    report_date = date.strftime("%Y-%m-%d")
    cash_flow_items = []

    
    
    revenue_items = [
        ("Main Business Revenue", round(abs(self.chart_of_accounts["6001"]["balance"]),2)),
            ("Interest income", round(abs(self.chart_of_accounts["1222"]["balance"]),2))
        
        
    ]
    total_revenue = round(sum([item[1] for item in revenue_items]),2)


    # Cost section
    cost_items = [
        ("Main Business Cost", abs(self.chart_of_accounts["6401"]["balance"]))
    ]
    total_costs = round(sum([item[1] for item in cost_items]),2)


    # Expense section
    expense_items = [
        ("Administrative Expenses", round(abs(self.chart_of_accounts["6601"]["balance"]),2)),
        ("Sales Expenses", round(abs(self.chart_of_accounts["6602"]["balance"]),2)),
        ("Financial Expenses",round( abs(self.chart_of_accounts["6603"]["balance"]),2)),
            ("Accumulated Depreciation", round(abs(self.chart_of_accounts["1602"]["balance"]),2))
    ]
    total_expenses = round(sum([item[1] for item in expense_items]),2)


    # Calculate operating profit
    operating_profit = round(total_revenue - total_costs - total_expenses,2)

    # Calculate net profit
    net_profit = operating_profit -  self.chart_of_accounts["2221"]["balance"] # Assuming no other gains/losses for simplicity
    
    
    cash_flow_items = [
    ["Cash Flow From Operating Activities", ""],
    ["Net Profit ", str(net_profit)],
    ["Depreciation ", str(round(abs(self.chart_of_accounts["1602"]["balance"]), 2))],
    ["(Increase) Decrease in Accounts Receivable ", -round(abs(self.chart_of_accounts["1221"]["balance"]), 2)],
    ["(Increase) Decrease in Interest Receivable ", -round(abs(self.chart_of_accounts["1222"]["balance"]), 2)],
    ["(Increase) Decrease in Inventory ", -round(abs(self.chart_of_accounts["1405"]["balance"]), 2)],
    ["Increase (Decrease) in Accounts Payable ", round(abs(self.chart_of_accounts["2202"]["balance"]), 2)],
    ["Increase (Decrease) in Tax Payable ", round(abs(self.chart_of_accounts["2221"]["balance"]), 2)],
    ["Net Cash Flow from Operating Activities ", round(
        net_profit + 
        abs(self.chart_of_accounts["1602"]["balance"]) - 
        abs(self.chart_of_accounts["1221"]["balance"]) - 
        abs(self.chart_of_accounts["1222"]["balance"]) - 
        abs(self.chart_of_accounts["1405"]["balance"]) + 
        abs(self.chart_of_accounts["2202"]["balance"]) + 
        abs(self.chart_of_accounts["2221"]["balance"]), 2)
    ],
    ["Cash Flow from Investing Activities", ""],
    ["Purchase of Fixed Assets ", round(-self.initial_fixed_asset + abs(self.chart_of_accounts["1601"]["balance"]), 2)],
    ["Net Cash Flow from Investing Activities ", round(-(-self.initial_fixed_asset + abs(self.chart_of_accounts["1601"]["balance"])), 2)],
    ["Cash and Cash Equivalents", ""],
    ["Beginning Balance ", round((self.initial_bank_deposit + self.initial_cash), 2)],
    ["Ending Balance ", round(self.chart_of_accounts["1001"]["balance"] + self.chart_of_accounts["1002"]["balance"], 2)],
    ["Net Increase ", round(
        self.chart_of_accounts["1001"]["balance"] + 
        self.chart_of_accounts["1002"]["balance"] - 
        self.initial_bank_deposit - 
        self.initial_cash, 2)
    ]
]
    cash_flow_df = pd.DataFrame(cash_flow_items, columns=["Account", "Amount"])
    pd.options.display.float_format = '{:.2f}'.format
    cash_flow_df['Date'] = date
    return cash_flow_df


def generate_unique_value(original_value, generator_func):
    modified_value = generator_func()
    while modified_value == original_value:
        modified_value = generator_func()
    return modified_value

def is_valid_value(value):
    return not (pd.isna(value) or 
                (isinstance(value, (list, np.ndarray)) and len(value) == 0) or 
                value is None)

def is_valid_row(row, required_fields):
    return all(field in row and is_valid_value(row[field]) for field in required_fields)

def generate_description(row):
    parts = []
    if pd.notnull(row['date']):
        parts.append(f"On {row['date'].strftime('%B %d, %Y')}, an invoice was issued for a")
    if pd.notnull(row['type']):
        parts.append(f"{row['type']},")
    if pd.notnull(row['quantity']) and pd.notnull(row['unit_price']):
        parts.append(f"consisting of {row['quantity']} units at a unit price of ${row['unit_price']:.2f},")
    if pd.notnull(row['amount']):
        parts.append(f"totaling ${row['amount']:.2f}.")
    if pd.notnull(row['cost_amount']):
        parts.append(f"The cost amount for this transaction was ${row['cost_amount']:.2f},")
    if pd.notnull(row['tax_amount']):
        parts.append(f"with a tax amount of ${row['tax_amount']:.2f},")
    if pd.notnull(row['after_tax_amount']):
        parts.append(f"leading to a total amount due of ${row['after_tax_amount']:.2f}.")
    if pd.notnull(row['receive_method']):
        parts.append(f"The receive_method of this transaction was {row['receive_method'].lower()},") 
    if pd.notnull(row['payment_method']):
        parts.append(f"The payment_method of this transaction was {row['payment_method'].lower()},") 
    if pd.notnull(row['payment/receipt_status']):
        parts.append(f"and this transaction was {row['payment/receipt_status'].lower()}.")       
    if pd.notnull(row['preparer']):
        parts.append(f"This transaction was prepared by {row['preparer']},")
    if pd.notnull(row['approver']):
        parts.append(f"and the approver is {row['approver']}.")
    if pd.notnull(row['supplier_id']):
        parts.append(f"The supplier ID is {row['supplier_id']},")
    if pd.notnull(row['supplier_name']):
        parts.append(f"and the supplier name is {row['supplier_name']}.")

    return " ".join(part.strip() for part in parts).strip() if parts else "No description available."

def extract_date(date_obj):

    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d")
    else:

        return date_obj
def create_risk_scenario(row, selected_error_types=None):
    modified_row = row.copy()
    

    if selected_error_types is None:
        risk_count = np.random.poisson(lam=0.8)
    else:
        risk_count = len(selected_error_types)
    
    if risk_count == 0:
        return modified_row
    risk_issues = []
    risk_scenarios = [
        {
            'condition': lambda row: is_valid_row(row, ['amount']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    float(row['amount']),
                    lambda: round(float(row['amount']) * (1 + random.uniform(0.05, 0.25)), 2)
                )),
                'type': 'amount discrepancy',
                'description':{
                    'Original amount': row['amount'],
                    'Recorded amount': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['after_tax_amount', 'tax_amount']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    float(row['tax_amount']),
                    lambda: round(float(row['after_tax_amount']) * random.uniform(0.8, 1.2), 2)
                )),
                'type': 'tax error',
                'description': {
                    'Original tax': row['tax_amount'],
                    'Recorded tax': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['quantity', 'unit_price']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    int(float(row['quantity'])),
                    lambda: int(float(row['quantity']) * random.uniform(0.7, 1.3))
                )),
                'type': 'quantity mismatch',
                'description': {
                    'Original quantity': row['quantity'],
                    'Recorded quantity': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['unit_price']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    float(row['unit_price']),
                    lambda: round(float(row['unit_price']) * random.uniform(0.8, 1.2), 2)
                )),
                'type': 'price anomaly',
                'description': {
                    'Original price': row['unit_price'],
                    'Recorded price': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['profit']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    float(row['profit']),
                    lambda: round(float(row['profit']) * random.uniform(0.7, 1.3), 2)
                )),
                'type': 'profit irregularity',
                'description': {
                    'Original profit': row['profit'],
                    'Recorded profit': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['preparer']) and  is_valid_row(row, ['approver']),
            'generator': lambda row: {
                'value': '',
                'type': 'unapproved transaction',
                'description':{
                    'Original Approver': row['approver'],
                    'Recorded Approver': 'None',
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['approver']) and  is_valid_row(row, ['preparer']),
            'generator': lambda row: {
                'value': '',
                'type': 'approval without_preparer',
                'description': {
                    'Original Preparer': row['preparer'],
                    'Recorded Preparer': 'None',
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['date']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    row['date'],
                    lambda: (pd.to_datetime(row['date']) + pd.Timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
                )),
                'type': 'recording delay',
                'description': {
                    'Original date': extract_date(row['date']),
                    'Recorded date': extract_date(modified_value),
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['receive_method']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    row.get('receive_method', ''),
                    lambda: random.choice([
                        type_val for type_val in ['Interest receivable', 'Cash', 'Account Receivable'] 
                        if type_val != row.get('receive_method', '')
                    ])
                )),
                'type': 'receive_method misclassification',
                'description': {
                    'Original receive_method': row.get('receive_method', 'N/A'),
                    'Recorded receive_method': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['payment_method']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    row.get('payment_method', ''),
                    lambda: random.choice([
                        type_val for type_val in ['Bank Transfer', 'Account Payable', 'Cash'] 
                        if type_val != row.get('payment_method', '')
                    ])
                )),
                'type': 'payment_method misclassification',
                'description': {
                    'Original payment_method': row.get('payment_method', 'N/A'),
                    'Recorded payment_method': modified_value,
                    'id': row['id']
                }
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['payment/receipt_status']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    row.get('payment/receipt_status', ''),
                    lambda: random.choice([
                        type_val for type_val in ['Paid', 'Unpaid'] 
                        if type_val != row.get('payment/receipt_status', '')
                    ])
                )),
                'type': 'payment/receipt_status misclassification',
                'description':{'Recorded payment/receipt_status' :modified_value, 'Original payment/receipt_status': row.get('payment/receipt_status', 'N/A'),
                    'id': row['id']}
            }
        },
        {
            'condition': lambda row: is_valid_row(row, ['type']),
            'generator': lambda row: {
                'value': (modified_value := generate_unique_value(
                    row.get('type', ''),
                    lambda: random.choice([
                        type_val for type_val in ['Sale', 'Purchase', 'Depreciation', 'Sales Expenses', 'Financial Expenses', 'Administrative Expenses'] 
                        if type_val != row.get('type', '')
                    ])
                )),
                'type': 'type misclassification',
                'description':{
                    'Original category': row.get('type', 'N/A'),
                    'Recorded category': modified_value,
                    'id': row['id']
                }
            }
        }
    ]

    available_scenarios = [
        scenario for scenario in risk_scenarios 
        if scenario['condition'](row) and (selected_error_types is None or scenario['generator'](row)['type'] in selected_error_types)
    ]

    if not available_scenarios:
        return modified_row

    risk_count = min(risk_count, len(available_scenarios))
    selected_scenarios = random.sample(available_scenarios, risk_count)
    risk_issues = []
    
    count = 0
    for scenario in selected_scenarios:
        
        try:
            risk_detail = scenario['generator'](row)
            if risk_detail['type'] == 'amount discrepancy':
                modified_row['amount'] = risk_detail['value']
            elif risk_detail['type'] == 'tax error':
                modified_row['tax_amount'] = risk_detail['value']
            elif risk_detail['type'] == 'payment/receipt_status misclassification':
                modified_row['payment/receipt_status'] = risk_detail['value']
            elif risk_detail['type'] == 'payment_method misclassification':
                modified_row['payment_method'] = risk_detail['value']
            elif risk_detail['type'] == 'receive_method misclassification':
                modified_row['receive_method'] = risk_detail['value']
            elif risk_detail['type'] == 'quantity mismatch':
                modified_row['quantity'] = risk_detail['value']
                modified_row['amount'] = round(risk_detail['value'] * float(row['unit_price']), 2)
            elif risk_detail['type'] == 'price anomaly':
                modified_row['unit_price'] = risk_detail['value']
            elif risk_detail['type'] == 'profit irregularity':
                modified_row['profit'] = risk_detail['value']
            elif risk_detail['type'] == 'recording delay':
                modified_row['date'] = risk_detail['value']
            elif risk_detail['type'] == 'type misclassification':
                modified_row['type'] = risk_detail['value']
            elif risk_detail['type'] == 'unapproved transaction':
                modified_row['approver'] = ''
            elif risk_detail['type'] == 'approval without_preparer':
                modified_row['preparer'] = ''

            risk_issues.append(risk_detail['description'])
        
        except Exception as e:
            print(f"Error processing risk scenario: {e}")
    count = len(risk_issues)
    print(count)
    if risk_issues:
        

        modified_row['risk_issues'] = str(risk_issues)
        modified_row['count'] = count

    return modified_row

def apply_error_once(df, selected_errors):
    error_generated = False
    while not error_generated:
        random_index = random.randint(0, len(df) - 1)
        row = df.iloc[random_index]
        modified_row = create_risk_scenario(row, selected_errors)
        if modified_row is not None and not modified_row.equals(row) and modified_row['count'] == len(selected_errors):
            for column in modified_row.index:
                df.at[random_index, column] = modified_row[column]
            error_generated = True

    
    print(modified_row['risk_issues'])        
    return df


def generate_auditable_risk_transactions(transactions_df,task_path,selected_errors):
    transactions_df_incorrect = transactions_df.copy().round(2)
    transactions_df_incorrect['invoice'] = transactions_df_incorrect.apply(generate_description, axis=1)
    
    # selected_errors = ['amount discrepancy','receive_method misclassification','payment/receipt_status misclassification' ]
    transactions_df_incorrect = apply_error_once(transactions_df_incorrect, selected_errors)
    transactions_df_incorrect = transactions_df_incorrect.drop(columns=['count'])
    columns_to_rename = [
        col for col in ['amount', 'date', 'tax_amount', 'quantity', 'unit_price', 'profit', 'customer_id', 'type', 'approver', 'preparer','payment/receipt_status','cost_per_unit','payment_method','after_tax_amount','product_name','cost_amount','receive_method']
        if col in transactions_df_incorrect.columns
    ]
    transactions_df_incorrect.rename(columns={col: f'recorded_{col}' for col in columns_to_rename}, inplace=True)
    transactions_df_incorrect = transactions_df_incorrect.loc[:, ~transactions_df_incorrect.columns.duplicated()]
    transactions_df_incorrect.to_csv(task_path, index=False)
    return transactions_df_incorrect




def export_to_csv(self,end_date,output_dir="C:/Users/34956/Desktop/nips/output2"):
    """Export Data to CSV Files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export Transaction Records
    transactions_df = pd.DataFrame(self.transactions)
    transactions_df.to_csv(os.path.join(output_dir, "transactions.csv"), index=False)
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit1.csv"),['type misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit2.csv"),['recording delay'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit3.csv"),['payment/receipt_status misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit4.csv"),['payment_method misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit5.csv"),['quantity mismatch'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit6.csv"),['price anomaly'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit7.csv"),['receive_method misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit8.csv"),['amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit9.csv"),['tax error'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit10.csv"),['profit irregularity'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit11.csv"),['approval without_preparer'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit12.csv"),['unapproved transaction'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit13.csv"),['type misclassification','tax error'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit14.csv"),['payment/receipt_status misclassification','quantity mismatch'])
    
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit15.csv"),['type misclassification','quantity mismatch'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit16.csv"),['payment/receipt_status misclassification','amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit17.csv"),['receive_method misclassification','type misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit18.csv"),['payment/receipt_status misclassification','quantity mismatch','profit irregularity'])

    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit19.csv"),['type misclassification', 'recording delay'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit20.csv"),['type misclassification', 'price anomaly'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit21.csv"),['type misclassification', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit22.csv"),['recording delay', 'price anomaly'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit23.csv"),['recording delay', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit24.csv"),['price anomaly', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit25.csv"),['type misclassification', 'recording delay', 'price anomaly'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit26.csv"),['type misclassification', 'recording delay', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit27.csv"),['type misclassification', 'price anomaly', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit28.csv"),['recording delay', 'price anomaly', 'amount discrepancy'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit29.csv"),['tax error', 'price anomaly', 'amount discrepancy', 'recording delay'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit30.csv"),['tax error', 'price anomaly', 'amount discrepancy', 'type misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit31.csv"),['tax error', 'price anomaly', 'amount discrepancy', 'quantity mismatch'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit32.csv"),['price anomaly', 'amount discrepancy', 'recording delay', 'quantity mismatch'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit33.csv"),['tax error', 'price anomaly', 'amount discrepancy', 'recording delay', 'type misclassification'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit34.csv"),['tax error', 'price anomaly', 'recording delay', 'type misclassification', 'quantity mismatch'])
    generate_auditable_risk_transactions(transactions_df, os.path.join(output_dir, "./audit35.csv"),['price anomaly', 'amount discrepancy', 'recording delay', 'type misclassification', 'quantity mismatch'])


    # transactions_df_incorrect = generate_auditable_risk_transactions(transactions_df)
    # transactions_df_incorrect.to_csv(os.path.join(output_dir, "transactions_incorrect.csv"), index=False)
    # Export Journal Entries
    # journal_entries_df.to_csv(os.path.join(output_dir, "journal_entries.csv"), index=False)

    # Export Chart of Accounts
    accounts_data = []
    for code, account in self.chart_of_accounts.items():
        accounts_data.append({
            "code": code,
            "name": account["name"],
            "type": account["type"],
            "balance": account["balance"]
        })
    # accounts_df = pd.DataFrame(accounts_data)
    # # accounts_df.to_csv(os.path.join(output_dir, "account_balances.csv"), index=False)

    # # Export Balance Sheet
    # assets_df, liabilities_and_equity_df = generate_balance_sheet(self)
    # assets_df.to_csv(os.path.join(output_dir, "balance_sheet_assets.csv"), index=False)
    # liabilities_and_equity_df.to_csv(os.path.join(output_dir, "balance_sheet_liabilities_and_equity.csv"), index=False)

    # Export Income Statement
    income_statement_df = generate_income_statement(self,end_date)
    income_statement_df['Amount'] = income_statement_df['Amount'].apply(
    lambda x: '{:.2f}'.format(float(x)) if pd.notna(x) and x != '' else ''
)
    income_statement_df.to_csv(os.path.join(output_dir, "income_statement.csv"), index=False,float_format='%.2f')
    
    # Export Cash Flow Statement
    cash_flow_df = generate_cash_flow_statement(self,end_date)
    

    cash_flow_df['Amount'] = cash_flow_df['Amount'].apply(
    lambda x: '{:.2f}'.format(float(x)) if pd.notna(x) and x != '' else ''
)
    cash_flow_df.to_csv(os.path.join(output_dir, "cash_flow_statement.csv"), index=False,float_format='%.2f')
    print(cash_flow_df)


