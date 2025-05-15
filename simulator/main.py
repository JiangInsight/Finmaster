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
    export_to_csv
)
from business_logic import FinancialStatementGenerator
if __name__ == "__main__":
    pd.options.display.float_format = '{:.2f}'.format
    daily_profit = []
    daily_cost = []
    date_draw = []
    # Create Generator Instance
    generator = FinancialStatementGenerator(
        start_date=datetime(2023, 12, 31), 
        random_seed=SEED  # You can change this seed to get different but reproducible results
    )
    
    try:
        # Check Initial Balance
        print("Checking Initial Balance...")
        generator.check_accounts_balance()
        print("Initial Balance is Balanced")
        
        # Set Simulation Date Range
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2025, 2,5)
        
        print("\nStarting Business Simulation...")
        current_date = start_date
        while current_date <= end_date and len(generator.transactions)<INITIAL_transaction_CONFIG['transaction']:
            
            print(f"Simulating Date: {current_date.strftime('%Y-%m-%d')}")
            generator.simulate_day(generator,current_date)
            generator.generate_interest(current_date)
            profit = generate_daily_profit(generator)
            daily_profit.append(profit)
            date_draw.append(current_date)
            
            try:
                generator.check_accounts_balance()
            except ValueError as e:
                
                print(f"Issue on Date {current_date.strftime('%Y-%m-%d')}: {e}")
                raise
            current_date += timedelta(days=1)
        end_date = current_date - timedelta(days=1)
        # Generate Reports
        trial_balance_df = generator.generate_trial_balance()
        income_statement_df = generate_income_statement(generator,end_date)
        assets_df, liabilities_and_equity_df = generate_balance_sheet(generator,end_date)
        combined_df = pd.concat([assets_df, liabilities_and_equity_df], ignore_index=True)
        combined_df = combined_df.rename(columns={'Amount': 'End_amount', 'Date': 'End_date'})

        initial_amount = [generator.initial_cash,generator.initial_bank_deposit,0,0,0,generator.initial_bank_deposit+generator.initial_cash,generator.initial_fixed_asset,0,generator.initial_fixed_asset,
                          generator.initial_fixed_asset+generator.initial_bank_deposit+generator.initial_cash,0,0,0,
                          generator.initial_fixed_asset+generator.initial_bank_deposit+generator.initial_cash
                          ,0,generator.initial_fixed_asset+generator.initial_bank_deposit+generator.initial_cash,generator.initial_fixed_asset+generator.initial_bank_deposit+generator.initial_cash]
        print(initial_amount)
        combined_df.insert(1, 'Initial_amount', initial_amount)
        initial_date = datetime(2023, 12, 31)
        combined_df.insert(2, 'Initial_date', initial_date)
        combined_df['End_amount'] = combined_df['End_amount'].apply(
    lambda x: '{:.2f}'.format(float(x)) if pd.notna(x) and x != '' else ''
)
     
        combined_df['Initial_amount'] = combined_df['Initial_amount'].apply(
    lambda x: '{:.2f}'.format(float(x)) if pd.notna(x) and x != '' else ''
)
        # Export Data
        # output_dir = 'C:/Users/34956/Desktop/nips/output2'
        
        combined_df.to_csv(os.path.join(output_dir, "balance_sheet.csv"), index=False)
        export_to_csv(generator,end_date,output_dir)
        print(f"Data Exported to {output_dir}")
        
        # Print Reports
        print("\n=== Trial Balance ===")
        print(trial_balance_df)
        
        print("\n=== Income Statement ===")
        print(income_statement_df)
        
        print("\n=== Balance Sheet (Assets Section) ===")
        print(assets_df)
        
        print("\n=== Balance Sheet (Liabilities and Owners' Equity Section) ===")
        print(liabilities_and_equity_df)
        print(combined_df)
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nCurrent Account Balances:")
        total_debit = 0
        total_credit = 0
        print("\nDebit Accounts:")
        for code, account in generator.chart_of_accounts.items():
            if account["type"] in ["asset", "expense"] and account["balance"] != 0:
                print(f"{code} - {account['name']}: {account['balance']}")
                total_debit += account["balance"]
        
        print("\nCredit Accounts:")
        for code, account in generator.chart_of_accounts.items():
            if account["type"] in ["liability", "equity", "income"] and account["balance"] != 0:
                print(f"{code} - {account['name']}: {account['balance']}")
                total_credit += account["balance"]
        
        print(f"\nTotal Debit: {total_debit}")
        print(f"Total Credit: {total_credit}")
        print(f"Difference: {total_debit - total_credit}")
        