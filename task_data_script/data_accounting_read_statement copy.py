import pandas as pd
import csv
import math
import json
import numpy as np
from decimal import Decimal
import argparse
import os

def csv_to_table(csv_file_path: str) -> str:

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = [cell.replace('|', '\\|') for cell in next(reader)]
        rows = [
            [cell.replace('|', '\\|') for cell in row]
            for row in reader
        ]

    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]

    for row in rows:
        table.append("| " + " | ".join(row) + " |")

    return "\n".join(table)

if __name__ == "__main__":
    np.set_printoptions(precision=2, suppress=True)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(project_root)
    parser = argparse.ArgumentParser(description='Select configuration and seed')

    parser.add_argument('--config', type=str, default='config_example', 
                        help='Configuration name (default: config_example)')

    parser.add_argument('--seed', type=int, default=676, 
                        help='Random seed value (default: 676)')

    args = parser.parse_args()
    # python your_script.py --config config_chemistry --seed 42
    config_name = args.config
    seed = args.seed
    
    json_dir = os.path.join(project_root, 'strctured_data')
    json_dir = os.path.join(json_dir,config_name)
    data_dir = os.path.join(project_root, 'simulated_financial_data')
    data_dir = os.path.join(data_dir, config_name)
    json_seed_dir = os.path.join(json_dir, f'{config_name}_{seed}')
    data_seed_dir_save = os.path.join(data_dir, f'{config_name}_{seed}')
    data_seed_dir = os.path.join('.\\simulated_financial_data\\' +str(config_name), f'{config_name}_{seed}')


    print(json_seed_dir)
    os.makedirs(json_seed_dir, exist_ok=True)
    json_save_path = os.path.join(json_seed_dir, 'data_accounting_read_statement.json')
    
    csv_path_balance_sheet = os.path.join(data_seed_dir, 'balance_sheet.csv')
    csv_path_income_statement = os.path.join(data_seed_dir, 'income_statement.csv')
    csv_path_cash_flow_statement = os.path.join(data_seed_dir, 'cash_flow_statement.csv')
    csv_path_transaction = os.path.join(data_seed_dir, 'transactions.csv')
    df_balance_sheet = pd.read_csv(data_seed_dir_save + '/balance_sheet.csv')
    # df_balance_sheet['Amount'] = df_balance_sheet['Amount'].fillna(0)

    df_income_statement = pd.read_csv(data_seed_dir_save +'/income_statement.csv')
    # df_income_statement['Amount'] = df_income_statement['Amount'].fillna(0)

    df_cash_flow_statement = pd.read_csv(data_seed_dir_save +'/cash_flow_statement.csv')
    df_cash_transaction = pd.read_csv(data_seed_dir_save + '/transactions.csv')
    df_cash_flow_statement['Account'] = df_cash_flow_statement['Account'].str.strip()
    df_balance_sheet.fillna(0, inplace=True)
    df_income_statement.fillna(0, inplace=True)
    df_cash_flow_statement.fillna(0, inplace=True)
    df_cash_transaction.fillna(0, inplace=True)

    print(df_cash_flow_statement)
    
    result_dict = {
    'task1': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 1,
        'task_name': 'understand balance sheet-cash on hand',
        "task_description": "based on the balance sheet, extract and output the value of cash on hand, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {'initial cash on hand':df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'Initial_amount'].values[0], 'end cash on hand': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'End_amount'].values[0]},
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task2': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 2,
        'task_name': 'understand balance sheet-bank deposits',
        "task_description": "based on the balance sheet, extract and output the value of bank deposits, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial bank deposits': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'Initial_amount'].values[0],
            'end bank deposits': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task3': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 3,
        'task_name': 'understand balance sheet-accounts receivable',
        "task_description": "based on the balance sheet, extract and output the value of accounts receivable, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial accounts receivable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'Initial_amount'].values[0],
            'end accounts receivable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task4': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 4,
        'task_name': 'understand balance sheet-interest receivable',
        "task_description": "based on the balance sheet, extract and output the value of interest receivable, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial interest receivable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
            'end interest receivable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task5': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 5,
        'task_name': 'understand balance sheet-inventory',
        "task_description": "based on the balance sheet, extract and output the value of inventory, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial inventory': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'Initial_amount'].values[0],
            'end inventory': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task6': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 6,
        'task_name': 'understand balance sheet-fixed assets',
         "task_description": "based on the balance sheet, extract and output the value of fixed assets, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial fixed assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'Initial_amount'].values[0],
            'end fixed assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task7': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 7,
        'task_name': 'understand balance sheet-accumulated depreciation',
        "task_description": "based on the balance sheet, extract and output the value of accumulated depreciation, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial accumulated depreciation': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'Initial_amount'].values[0],
            'end accumulated depreciation': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task8': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 8,
        'task_name': 'understand balance sheet-accounts payable',
         "task_description": "based on the balance sheet, extract and output the value of accounts payable, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial accounts payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
            'end accounts payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task9': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 9,
        'task_name': 'understand balance sheet-taxes payable',
        "task_description": "based on the balance sheet, extract and output the value of taxes payable, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial taxes payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
            'end taxes payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task10': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        "task_description": "based on the balance sheet, extract and output the value of paid-in capital, including initial and final value",
        'task_number': 10,
        'task_name': 'understand balance sheet-paid-in capital',
        'task_difficulty': 'easy',
        'task_answer': {
            'initial paid-in capital': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
            'end paid-in capital': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task11': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 11,
        'task_name': 'understand balance sheet-retained earnings',
         "task_description": "based on the balance sheet, extract and output the value of retained earnings, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial retained earnings': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'Initial_amount'].values[0],
            'end retained earnings': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task12': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 12,
        'task_name': 'understand balance sheet-current assets',
        "task_description": "based on the balance sheet, extract and output the value of current assets, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial current assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0],
            'end current assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task13': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 13,
        'task_name': 'understand balance sheet-non-current assets',
        "task_description": "based on the balance sheet, extract and output the value of non-current assets, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial non-current assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'Initial_amount'].values[0],
            'end non-current assets': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task14': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 14,
        'task_name': 'understand balance sheet-current liabilities',
        "task_description": "based on the balance sheet, extract and output the value of current liabilities, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial current liabilities': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'Initial_amount'].values[0],
            'end current liabilities': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task15': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 15,
        'task_name': "understand balance sheet-owner's equity",
        "task_description": "based on the balance sheet, extract and output the value of owner's equity, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'initial owner equity': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
            'end owner equity': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task16': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 16,
        'task_name': "understand balance sheet-total liabilities and owner's equity",
        "task_description": "based on the balance sheet, extract and output the value of total liabilities and owner's equity along with the values and names of its core constituent line items, including initial and final value",
        'task_difficulty': 'medium',
        'task_answer': {
            "initial total liabilities and owner's equity": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'Initial_amount'].values[0],
            "end total liabilities and owner's equity": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'End_amount'].values[0],
            'sub_items': {
            'initial total liabilities' : df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'Initial_amount'].values[0],
            'end total liabilities' :df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
            'initial total owners equity' :df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
            'end total owners equity' :df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
            }
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task17': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 17,
        'task_name': 'understand balance sheet-accounts receivable & accounts payable',
        "task_description": "based on the balance sheet, extract and output the value of accounts receivable and accounts payable, including initial and final value",
        'task_difficulty': 'medium',
        'task_answer': {
            'accounts_receivable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'Initial_amount'].values[0],
            'accounts_receivable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0],
            'accounts_payable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
            'accounts_payable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task18': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 18,
        'task_name': 'understand balance sheet-cash on hand & fixed assets & taxes payable',
        "task_description": "based on the balance sheet, extract and output the value of cash on hand, fixed assets and taxes payable, including initial and final value",
        'task_difficulty': 'medium',
        'task_answer': {
            'cash_on_hand_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'Initial_amount'].values[0],
            'cash_on_hand_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'End_amount'].values[0],
            'fixed_assets_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'Initial_amount'].values[0],
            'fixed_assets_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0],
            'taxes_payable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
            'taxes_payable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task19': {
        'data': csv_path_balance_sheet,
        'task_type': 'accounting_read statement',
        'task_number': 19,
        'task_name': 'understand balance sheet-interest receivable & accumulated depreciation & tax payable & paid-in capital',
        "task_description": "based on the balance sheet, extract and output the value of interest receivable, accumulated depreciation, tax payable and paid-in capital, including initial and final value",
        'task_difficulty': 'medium',
        'task_answer': {
            'interest_receivable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
            'interest_receivable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
            'accumulated_depreciation_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'Initial_amount'].values[0],
            'accumulated_depreciation_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'End_amount'].values[0],
            'taxes_payable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
            'taxes_payable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0],
            'paid_in_capital_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
            'paid_in_capital_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
        },
        'data_source': 'balance_sheet',
        'seed': seed,
    },
    'task20': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 20,
        'task_name': 'understand income statement-cost of goods sold',
        "task_description": "based on the income statement, extract and output the value of cost of goods sold",
        'task_difficulty': 'easy',
        'task_answer': {
            'Cost of Goods Sold': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
        }, 
        'data_source': 'income statement',
        'seed': seed,
    },
    'task21': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 21,
        'task_name': 'understand income statement-main business revenue',
         "task_description": "based on the income statement, extract and output the value of main business revenue",
        'task_difficulty': 'easy',
        'task_answer': {
            'Main Business Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]
        },  
        'data_source': 'income statement',
        'seed': seed,
    },
    'task22': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 22,
        'task_name': 'understand income statement-gross profit',
         "task_description": "based on the income statement, extract and output the value of gross profit",
        'task_difficulty': 'easy',
        'task_answer': {
            'gross profit': df_income_statement.loc[df_income_statement['Account'] == 'Gross Profit', 'Amount'].values[0]
        }, 
        'data_source': 'income statement',
        'seed': seed,
    },
    'task23': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 23,
        'task_name': 'understand income statement-interest income',
        "task_description": "based on the income statement, extract and output the value of interest income",
        'task_difficulty': 'easy',
        'task_answer': {
            'Interest Income': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task24': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 24,
        'task_name': 'understand income statement-administrative expenses',
        "task_description": "based on the income statement, extract and output the value of administrative expenses",
        'task_difficulty': 'easy',
        'task_answer': {
            'Administrative Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task25': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 25,
        'task_name': 'understand income statement-selling expenses',
        "task_description": "based on the income statement, extract and output the value of selling expenses",
        'task_difficulty': 'easy',
        'task_answer': {
            'Selling Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task26': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 26,
        'task_name': 'understand income statement-financial expenses',
         "task_description": "based on the income statement, extract and output the value of financial expenses",
        'task_difficulty': 'easy',
        'task_answer': {
           
            'Financial Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0]
        }, 
        'data_source': 'income statement',
        'seed': seed,
    },
    'task27': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 27,
        'task_name': 'understand income statement-accumulated depreciation',
         "task_description": "based on the income statement, extract and output the value of accumulated depreciation",
        'task_difficulty': 'easy',
        'task_answer': {
             'Depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task28': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 28,
        'task_name': 'understand income statement-tax expense',
         "task_description": "based on the income statement, extract and output the value of tax expense",
        'task_difficulty': 'easy',
        'task_answer': {
            'Tax Expense': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task29': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 29,
        'task_name': 'understand income statement-total revenue',
         "task_description": "based on the income statement, extract and output the value of total revenue",
        'task_difficulty': 'medium',
        'task_answer': {
            'Total Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
            'sub_items': {
                'Main Business Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]
            }
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task30': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 30,
        'task_name': 'understand income statement-operating expenses',
        "task_description": "based on the income statement, extract and output the value of operating expenses along with the relevant financial data involved in the calculation",
        'task_difficulty': 'medium',
        'task_answer': {
            'Total Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
            'sub_items': {
                'Administrative Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0],
                'Selling Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
                'Depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                'Financial Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0]
            }
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task31': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 31,
        'task_name': 'understand income statement-profit before tax',
        "task_description": "based on the income statement, extract and output the value of profit before tax along with the relevant financial data involved in the calculation",
        'task_difficulty': 'medium',
        'task_answer': {
            'Profit Before Tax': df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0],
            'sub_items': {
                \
                'Total Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                'Total Cost': df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0],
                'Total Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
                'Interest Income': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
                
            }
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task32': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
         "task_description": "based on the income statement, extract and output the value of net profit along with the relevant financial data involved in the calculation",
        'task_number': 32,
        'task_name': 'understand income statement-net profit',
        'task_difficulty': 'medium',
        'task_answer': {
            'Net Profit': df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0],
            'sub_items': {
                'Total Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                'Total Cost': df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0],
                'Total Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
                'Interest Income': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0],
                'Tax Expense': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
            }
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task33': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 33,
        'task_name': 'understand income statement-main business revenue & cost of goods sold',
        "task_description": "based on the income statement, extract and output the value of main business revenue and cost of goods sold",
        'task_difficulty': 'medium',
        'task_answer': {
            'main_business_revenue': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0],
            'cost_of_goods_sold': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task34': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 34,
        'task_name': 'understand income statement-total revenue & Cost of Goods Sold & administrative expenses',
         "task_description": "based on the income statement, extract and output the value of total revenue, cost of materials and administrative expenses",
        'task_difficulty': 'medium',
        'task_answer': {
            'total_revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
            'cost_of_goods sold': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0],
            'administrative expenses': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0]
        }, 
        'data_source': 'income statement',
        'seed': seed,
    },
    'task35': {
        'data': csv_path_income_statement,
        'task_type': 'accounting_read statement',
        'task_number': 35,
        'task_name': 'understand income statement-financial expenses & selling expense & depreciation & tax expense',
        "task_description": "based on the income statement, extract and output the value of financial expenses, selling expense, depreciation and tax expense",
        'task_difficulty': 'medium',
        'task_answer': {
            'financial expenses': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0],
            'selling_expense': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
            'depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0],
            'tax_expense': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
        },
        'data_source': 'income statement',
        'seed': seed,
    },
    'task36': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 36,
        'task_name': 'understand cash flow statement-net profit',
         "task_description": "based on the cash flow statement, extract and output the value of net profit",
        'task_difficulty': 'easy',
        'task_answer': {
            'Net Profit': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task37': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 37,
        'task_name': 'understand cash flow statement-depreciation',
        "task_description": "based on the cash flow statement, extract and output the value of depreciation",
        'task_difficulty': 'easy',
        'task_answer': {
            'Depreciation': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task38': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 38,
        'task_name': 'understand cash flow statement-decrease in accounts receivable',
        "task_description": "based on the cash flow statement, extract and output the value of decrease in accounts receivable",
        'task_difficulty': 'easy',
        'task_answer': {
            '(Increase) Decrease in Accounts Receivable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task39': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 39,
        'task_name': 'understand cash flow statement-decrease in inventory',
        "task_description": "based on the cash flow statement, extract and output the value of decrease in inventory",
        'task_difficulty': 'easy',
        'task_answer': {
            '(Increase) Decrease in Inventory': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task40': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 40,
        'task_name': 'understand cash flow statement-increase in accounts payable',
        "task_description": "based on the cash flow statement, extract and output the value of increase in accounts payable",
        'task_difficulty': 'easy',
        'task_answer': {
            'Increase (Decrease) in Accounts Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task41': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 41,
        'task_name': 'understand cash flow statement-increase in taxes payable',
        "task_description": "based on the cash flow statement, extract and output the value of increase in taxes payable",
        'task_difficulty': 'easy',
        'task_answer': {
            'Increase (Decrease) in Tax Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task42': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 42,
        'task_name': 'understand cash flow statement-Purchase of fixed assets',
        "task_description": "based on the cash flow statement, extract and output the value of Purchase of fixed assets",
        'task_difficulty': 'easy',
        'task_answer': {
            'Purchase of Fixed Assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task43': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 43,
        'task_name': 'understand cash flow statement-Beginning Cash and Cash Equivalents Balance',
        "task_description": "based on the cash flow statement, extract and output the value of Beginning Cash and Cash Equivalents Balance",
        'task_difficulty': 'easy',
        'task_answer': {
            'Beginning Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task44': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 44,
        'task_name': 'understand cash flow statement-Ending Cash and Cash Equivalents Balance',
        "task_description": "based on the cash flow statement, extract and output the value of Ending Cash and Cash Equivalents Balance",
        'task_difficulty': 'easy',
        'task_answer': {
            'Ending Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task45': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 45,
        'task_name': 'understand cash flow statement-net cash flow from operating activities',
        "task_description": "based on the net cash flow statement, extract and output the value of net cash flow from operating activities along with the relevant financial data involved in the calculation",
        'task_difficulty': 'medium',
        'task_answer': {
            'Net Cash Flow from Operating Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0],
             'sub_items': {
                'Net Profit': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0],
                'Depreciation':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                '(Increase) Decrease in Accounts Receivable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0],
                '(Increase) Decrease in Interest Receivable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Interest Receivable', 'Amount'].values[0],
                '(Increase) Decrease in Inventory': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0],
                'Increase (Decrease) in Accounts Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0],
                'Increase (Decrease) in Tax Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0]
            }
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
     'task46': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 46,
        'task_name': 'understand cash flow statement-net cash flow from investing activities',
        "task_description": "based on the cash flow statement, extract and output the value of net cash flow from investing activities along with the relevant financial data involved in the calculation",
        'task_difficulty': 'medium',
        'task_answer': {
            'Net Cash Flow from Investing Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0],
            'sub_items': {
                'Purchase of Fixed Assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
            }
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task47': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 47,
        'task_name': 'understand cash flow statement-net increase in cash and cash equivalents',
         "task_description": "based on the cash flow statement, extract and output the value of net increase in cash and cash equivalents along with the relevant financial data involved in the calculation",
        'task_difficulty': 'medium',
        'task_answer': {
            'Net Increase': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0],
            'sub_items': {
                'Beginning Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0],
                'Ending Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0]
            }
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
        'task48': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 48,
        'task_name': 'understand cash flow statement-net profit & Purchase in fixed assets',
        "task_description": "based on the cash flow statement, extract and output the value of net profit and Purchase in fixed assets",
        'task_difficulty': 'medium',
        'task_answer': {
            'net_profit': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0],
            'Purchase_of_fixed_assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task49': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 49,
        'task_name': 'understand cash flow statement-increase in accounts payable & Purchase of fixed assets & beginning cash and cash equivalents balance',
        "task_description": "based on the cash flow statement, extract and output the value of increase in accounts payable, Purchase of fixed assets and beginning cash and cash equivalents balance",
        'task_difficulty': 'medium',
        'task_answer': {
            'increase_in_accounts_payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0],
            'Purchase_of_fixed_assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0],
            'beginning_cash_balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task50': {
        'data': csv_path_cash_flow_statement,
        'task_type': 'accounting_read statement',
        'task_number': 50,
        'task_name': 'understand cash flow statement-depreciation & decrease in inventory & net cash flow from investing activities & net increase',
        "task_description": "based on the cash flow statement, extract and output the value of depreciation, decrease in inventory, net cash flow from investing activities and net increase",
        'task_difficulty': 'medium',
        'task_answer': {
            'depreciation': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0],
            'decrease_in_inventory': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0],
            'net_cash_flow_from_investing': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0],
            'net_increase': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]
        },
        'data_source': 'cash flow statement',
        'seed': seed,
    },
    'task51': {
        'data': {
            'balance sheet': csv_path_balance_sheet, 
            'cash flow': csv_path_cash_flow_statement, 
            'income statement': csv_path_income_statement
        },
        'task_type': 'accounting_read statement',
        'task_number': 51,
        'task_name': 'understand financial statement-interest receivable',
        "task_description": "based on the all financial statements, extract and output the value of interest receivable, including initial and final value",
        'task_difficulty': 'easy',
        'task_answer': {
            'interest_receivable_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
            'interest_receivable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
        },
        'data_source': 'all financial statements',
        'seed': seed,
    },

'task52': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
     "task_description": 'based on the financial statement, extract and output the value of paid-in capital, including initial and final value',
    'task_number': 52,
    'task_name': 'understand financial statement-paid-in capital',
    'task_difficulty': 'easy',
    'task_answer': {
        'paid_in_capital_initial': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
        'paid_in_capital_final': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task53': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 53,
    "task_description": 'based on the financial statement, extract and output the value of cost of goods sold',
    'task_name': 'understand financial statement-cost of goods sold',
    'task_difficulty': 'easy',
    'task_answer': {
        'cost of goods sold': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task54': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    "task_description":'based on the financial statement, extract and output the value of selling expenses' ,
    'task_number': 54,
    'task_name': 'understand financial statement-selling expenses',
    'task_difficulty': 'easy',
    'task_answer': {
        'selling_expenses': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task55': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    "task_description": 'based on the financial statement, extract and output the value of tax expense',
    'task_number': 55,
    'task_name': 'understand financial statement-tax expense',
    'task_difficulty': 'easy',
    'task_answer': {
        'tax expense': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task56': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 56,
    'task_name': 'understand financial statement-depreciation',
    "task_description": 'based on the financial statement, extract and output the value of depreciation',
    'task_difficulty': 'easy',
    'task_answer': {
        'depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task57': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 57,
    'task_name': 'understand financial statement-increase in accounts payable',
    "task_description": 'based on the financial statement, extract and output the value of increase in accounts payable',
    'task_difficulty': 'easy',
    'task_answer': {
        'increase_in_accounts_payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task58': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 58,
    'task_name': 'understand financial statement-Beginning Cash and Cash Equivalents Balance',
    "task_description":'based on the financial statement, extract and output the value of Beginning Cash and Cash Equivalents Balance' ,
    'task_difficulty': 'easy',
    'task_answer': {
        'beginning_cash_equivalents_balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
    },

    'data_source': 'all financial statements',
    'seed': seed,
},
'task59': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 59,
    'task_name': 'understand financial statement-interest receivable & net increase of cash and cash equivalents',
     "task_description": "based on the all financial statements, extract and output the end value of interest receivable and net increase of cash and cash equivalents",
    'task_difficulty': 'hard',
    'task_answer': {
            'interest_receivable_end': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
        'net_increase_cash_equivalents': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},
'task60': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 60,
    'task_name': 'understand financial statement-bank deposits & interest income',
    "task_description": 'based on the all financial statements, extract and output the end value of bank deposits and interest income',
    'task_difficulty': 'hard',
    'task_answer': {
        'bank_deposits': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'End_amount'].values[0],
        'interest_income': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task61': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 61,
    'task_name': 'understand financial statement-selling expenses & Purchase of fixed assets',
    "task_description": 'based on the all financial statements, extract and output the value of selling expenses and Purchase of fixed assets',
    'task_difficulty': 'hard',
    'task_answer': {
        'selling_expenses': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
        'Purchase of fixed assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task62': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 62,
    'task_name': 'understand financial statement-accounts receivable & financial expenses & purchase of fixed assets',
    "task_description":'based on the all financial statements, extract and output the end value of accounts receivable, financial expenses and purchase of fixed assets' ,
    'task_difficulty': 'hard',
    'task_answer': {
        'accounts_receivable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0],
        'financial_expenses': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0],
        'purchase_of_fixed_assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task63': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 63,
    'task_name': 'understand financial statement-net cash flow from operating activities & taxes payable & total revenue',
    "task_description": 'based on the all financial statements, extract and output the end value of net cash flow from operating activities, taxes payable and total revenue',
    'task_difficulty': 'hard',
    'task_answer': {
        'net_cash_flow_operating': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0],
        'taxes_payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0],
        'total_revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0]
    },
    'data_source': 'all financial statements',
    'seed': seed,
},

'task64': {
    'data': {
        'balance sheet': csv_path_balance_sheet, 
        'cash flow': csv_path_cash_flow_statement, 
        'income statement': csv_path_income_statement
    },
    'task_type': 'accounting_read statement',
    'task_number': 64,
    'task_name': 'understand financial statement-profit before tax & increase in accounts payable & paid-in capital',
    "task_description":'based on the all financial statements, extract and output the end value of profit before tax, increase in accounts payable and paid-in capital',
    'task_difficulty': 'hard',
    'task_answer': {
        'profit_before_tax': df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0],
        'increase_in_accounts_payable': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0] - df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
        'paid_in_capital': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]},
    'data_source': 'all financial statements',
    'seed': seed,
} 
}
    print(result_dict['task1'])
    
    
    
    
    def replace_infinity_and_nan(obj):
        if isinstance(obj, dict):
            return {k: replace_infinity_and_nan(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_infinity_and_nan(v) for v in obj]
        elif isinstance(obj, float):
            if math.isinf(obj) or math.isnan(obj):
                return 0
            else:
                return obj
        else:
            return obj

    result_dict = replace_infinity_and_nan(result_dict)
   
    def convert_numpy_types(obj):
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(v) for v in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return obj
    result_dict = convert_numpy_types(result_dict)
    def format_nested_values(value):
        if isinstance(value, dict):
            return {k: format_nested_values(v) for k, v in value.items()}
        elif isinstance(value, (int, float)):
            return f"{value:.2f}"
        elif isinstance(value, str):
            try:
                float_val = float(value.replace(',', ''))
                return f"{float_val:.2f}"
            except ValueError:
                return value
        else:
            return value

    for task_key, task_value in result_dict.items():
        task_value['task_answer'] = format_nested_values(task_value['task_answer'])
    for task_key, task_value in result_dict.items():
        print(f"{task_key}: {task_value['task_answer']}" if task_value['task_answer'] is not None else f"{task_key}: None")

    with open(json_save_path, 'w', encoding='utf-8') as json_file:
        json.dump(result_dict, json_file, ensure_ascii=False, indent=4)