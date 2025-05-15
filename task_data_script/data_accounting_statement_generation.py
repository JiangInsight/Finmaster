import pandas as pd
import csv
import json
import numpy as np
import argparse
import math
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

np.set_printoptions(precision=2, suppress=True)

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义配置和种子值
config_name = {
    'config_chemistry': ['240', '249', '293', '330', '678', '54'],
    'config_consulting': ['171', '348', '380', '538', '565', '590'],
    'config_hotel': ['66', '173', '174', '226', '644', '713'],
    'config_sales': ['111', '245', '511', '589', '660', '706'],
    'config_big_manufactory': ['226', '263', '716', '827', '849', '908']
}

# 遍历每个配置和种子值
for config, seeds in config_name.items():
    for seed in seeds:
        # 打印当前配置和种子值
        print(f"Processing config: {config}, seed: {seed}")

        # 定义路径
        json_dir = os.path.join(project_root, 'strctured_data', config)
        data_dir = os.path.join(project_root, 'simulated_financial_data', config)
        json_seed_dir = os.path.join(json_dir, f'{config}_{seed}')
        data_seed_dir_save = os.path.join(data_dir, f'{config}_{seed}')
        data_seed_dir = os.path.join('.\\simulated_financial_data\\' + str(config), f'{config}_{seed}')

        # 创建目录
        os.makedirs(json_seed_dir, exist_ok=True)
        json_save_path = os.path.join(json_seed_dir, 'data_accounting_statement_generation.json')

        # 定义 CSV 文件路径
        csv_path_balance_sheet = os.path.join(data_seed_dir, 'balance_sheet.csv')
        csv_path_income_statement = os.path.join(data_seed_dir, 'income_statement.csv')
        csv_path_cash_flow_statement = os.path.join(data_seed_dir, 'cash_flow_statement.csv')
        csv_path_transaction = os.path.join(data_seed_dir, 'transactions.csv')

      
            # 读取 CSV 文件
        df_balance_sheet = pd.read_csv(os.path.join(data_seed_dir_save, 'balance_sheet.csv'))
        df_income_statement = pd.read_csv(os.path.join(data_seed_dir_save, 'income_statement.csv'))
        df_cash_flow_statement = pd.read_csv(os.path.join(data_seed_dir_save, 'cash_flow_statement.csv'))
        df_cash_transaction = pd.read_csv(os.path.join(data_seed_dir_save, 'transactions.csv'))

        # 数据清洗
        df_cash_flow_statement['Account'] = df_cash_flow_statement['Account'].str.strip()
        df_balance_sheet.fillna(0, inplace=True)
        df_income_statement.fillna(0, inplace=True)
        df_cash_flow_statement.fillna(0, inplace=True)
        df_cash_transaction.fillna(0, inplace=True)

        # 打印清洗后的数据
        print(f"Cleaned Cash Flow Statement for config: {config}, seed: {seed}")
        print(df_cash_flow_statement)

        result_dict = {
        'task1': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Cash on Hand',
            "task_description": "Based on transactions data, calculate the total amount of cash on hand item in the balance sheet, including both the initial and final amounts.",
            'task_number': 1,
            'data': csv_path_transaction,
            'task_answer':  
                {
            'Cash on Hand Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Cash on Hand", 'Initial_amount'].values[0],
            'Cash on Hand End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Cash on Hand", 'End_amount'].values[0],
        },
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task2': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Bank Deposits',
            "task_description": "Based on transactions data, calculate the bank deposits item in the balance sheet, including both the initial and final amounts.",
            'task_number': 2,
            'task_answer': 
    {
            'Bank Deposits Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Bank Deposits", 'Initial_amount'].values[0],
            'Bank Deposits End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Bank Deposits", 'End_amount'].values[0],
        },
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task3': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Inventory',
            "task_description": "Based on transactions data, calculate the inventory item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Inventory Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Inventory", 'Initial_amount'].values[0],
            'Inventory End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Inventory", 'End_amount'].values[0],
        },
            'task_number': 3,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task4': {
            'task_type': 'financial statement generation',
            'task_difficulty':(1,1,2),
            'task_name': 'Balance Sheet-Accounts Receivable',
            "task_description": "Based on transactions data, calculate the accounts receivable item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Accounts Receivable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Accounts Receivable", 'Initial_amount'].values[0],
            'Accounts Receivable End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Accounts Receivable", 'End_amount'].values[0],
        },
            'task_number': 4,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task5': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Interest Receivable',
            "task_description": "Based on transactions data, calculate the interest receivable item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Interest Receivable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Interest Receivable", 'Initial_amount'].values[0],
            'Interest Receivable End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Interest Receivable", 'End_amount'].values[0],
        },
            'task_number': 5,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task6': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Current Assets',
            "task_description": "Based on transactions data, calculate the current assets item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Total Current Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Assets", 'Initial_amount'].values[0],
            'Total Current Assets End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Assets", 'End_amount'].values[0],
        },
            'task_number': 6,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task7': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Fixed Assets',
            "task_description": "Based on transactions data, calculate the fixed assets item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Fixed Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Fixed Assets", 'Initial_amount'].values[0],
            'Fixed Assets End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Fixed Assets", 'End_amount'].values[0],
        },
            'task_number': 7,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task8': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Accumulated Depreciation',
            "task_description": "Based on transactions data, calculate the accumulated depreciation item in the balance sheet, including both the initial and final amounts.",
            'task_number': 8,
            'data': csv_path_transaction,
            'task_answer':  
            {
            'Accumulated Depreciation Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Accumulated Depreciation", 'Initial_amount'].values[0],
            'Accumulated Depreciation End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Accumulated Depreciation", 'End_amount'].values[0],
        },
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task9': {
            'task_type': 'financial statement generation',
            'task_difficulty': (2,1,2),
            'task_name': 'Balance Sheet-Fixed Assets net',
            "task_description": "Based on transactions data, calculate the fixed assets net item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'fixed assets net Initial Value': round(float(df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Non-current Assets", 'Initial_amount'].values[0]), 2),
        'fixed assets net End Value': round(float(df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Non-current Assets", 'End_amount'].values[0]), 2)
        },
            'task_number': 9,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task10': {
            'task_type': 'financial statement generation',
            'task_difficulty':  (2,1,2),
            'task_name': 'Balance Sheet-Non-current Assets',
            "task_description": "Based on transactions data, calculate the property, plant and non-current assets item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Total Non-current Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Non-current Assets", 'Initial_amount'].values[0],
            'Total Non-current Assets End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Non-current Assets", 'End_amount'].values[0],
        },
            'task_number': 10,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task11': {
            'task_type': 'financial statement generation',
            'task_difficulty':  (7,1,2),
            'task_name': 'Balance Sheet-Total Assets',
            "task_description": "Based on transactions data, calculate the total assets item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Total Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Assets", 'Initial_amount'].values[0],
            'Total Assets End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Assets", 'End_amount'].values[0],
        },
            'task_number': 11,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task12': {
            'task_type': 'financial statement generation',
            'task_difficulty':  (1,1,2),
            'task_name': 'Balance Sheet-Accounts Payable',
            "task_description": "Based on transactions data, calculate the accounts payable item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Accounts Payable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Accounts Payable", 'Initial_amount'].values[0],
            'Accounts Payable End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Accounts Payable", 'End_amount'].values[0],
        },
            'task_number': 12,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
        'task13': {
            'task_type': 'financial statement generation',
            'task_difficulty':(1,1,2),
            'task_name': 'Balance Sheet-Taxes Payable',
            "task_description": "Based on transactions data, calculate the taxes payable item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Taxes Payable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Taxes Payable", 'Initial_amount'].values[0],
            'Taxes Payable End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Taxes Payable", 'End_amount'].values[0],
        },
            'task_number': 13,
            'data': csv_path_transaction,
            'data_source': 'all transactions data',
            'seed': seed
        },
    'task14': {
            'task_type': 'financial statement generation',
            'task_difficulty': (2,1,2),
            'task_name': 'Balance Sheet-Current Liabilities',
            "task_description": "Based on transactions data, calculate the current liabilities item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Total Current Liabilities Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'Initial_amount'].values[0],
            'Total Current Liabilities End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
        },
            'task_number': 14,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task15': {
            'task_type': 'financial statement generation',
            'task_difficulty': (2,1,2),
            'task_name': 'Balance Sheet-Total Liabilities',
            "task_description": "Based on transactions data, calculate the total liabilities item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Total Liabilities Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'Initial_amount'].values[0],
            'Total Liabilities End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
        },
            'task_number': 15,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task16': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Paid-in Capital',
            "task_description": "Based on transactions data, calculate the paid-in capital item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Paid-in Capital Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Paid-in Capital", 'Initial_amount'].values[0],
            'Paid-in Capital End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Paid-in Capital", 'End_amount'].values[0],
        },
            'task_number': 16,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed    
            },
        'task17': {
            'task_type': 'financial statement generation',
            'task_difficulty': (1,1,2),
            'task_name': 'Balance Sheet-Retained Earnings',
            "task_description": "Based on transactions data, calculate the retained earnings item in the balance sheet, including both the initial and final amounts.",
            'task_answer':  
            {
            'Retained Earnings Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Retained Earnings", 'Initial_amount'].values[0],
            'Retained Earnings End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Retained Earnings", 'End_amount'].values[0],
        },
            'task_number': 17,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task18': {
            'task_type': 'financial statement generation',
            'task_difficulty': (2,1,2),
            'task_name': "Balance Sheet-Total Owner's Equity",
            "task_description": "Based on transactions data, calculate the total owner's equity item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Total Owners Equity Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
            'Total Owners Equity End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
        },
            'task_number': 18,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task19': {
            'task_type': 'financial statement generation',
            'task_difficulty': (4,1,2),
            'task_name': "Balance Sheet-Total Liabilities and Owner's Equity",
            "task_description": "Based on transactions data, calculate the total liabilities and owner's equity item in the balance sheet, including both the initial and final amounts.",
            'task_answer': 
            {
            'Total Liabilities and Owners Equity Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'Initial_amount'].values[0],
            'Total Liabilities and Owners Equity End Value':df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'End_amount'].values[0],
        },
            'task_number': 19,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task20': {
            'task_type': 'financial statement generation',
            'task_difficulty': (37,1,2),
            'task_name': 'Balance Sheet-Balance Sheet',
            "task_description": "Based on transactions data, directly generate a complete balance sheet, including both the initial and final amounts.",
            'task_answer':{
                'Cash on Hand Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'Initial_amount'].values[0],
        'Bank Deposits Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'Initial_amount'].values[0],
        'Interest Receivable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
        'Accounts Receivable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'Initial_amount'].values[0],
        'Inventory Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'Initial_amount'].values[0],
        'Total Current Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0],
        'Fixed Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0],
        'Accumulated Depreciation Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'Initial_amount'].values[0],
        'Total Non-current Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'Initial_amount'].values[0],
        'Total Assets Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0],
        'Accounts Payable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
        'Taxes Payable Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
        'Total Current Liabilities Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'Initial_amount'].values[0],
        'Paid-in Capital Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
        'Retained Earnings Initial Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'Initial_amount'].values[0],
        "Total Owner's Equity Initial Value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
        "Total Liabilities and Owner's Equity Initial Value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'Initial_amount'].values[0],
        'Cash on Hand End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'End_amount'].values[0],
        'Bank Deposits End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'End_amount'].values[0],
        'Interest Receivable End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
        'Accounts Receivable End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0],
        'Inventory End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0],
        'Total Current Assets End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0],
        'Fixed Assets End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0],
        'Accumulated Depreciation End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'End_amount'].values[0],
        'Total Non-current Assets End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'End_amount'].values[0],
        'Total Assets End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0],
        'Accounts Payable End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0],
        'Taxes Payable End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0],
        'Total Current Liabilities End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
        'Paid-in Capital End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0],
        'Retained Earnings End Value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'End_amount'].values[0],
        "Total Owner's Equity End Value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
        "Total Liabilities and Owner's Equity End Value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'End_amount'].values[0]
    },
            'task_number': 20,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task21': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Main Business Revenue',
            "task_description": "Based on transactions data, calculate the final main business revenue item in the income statement.",
            'task_answer': {'Main Business Revenue':df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]},
            'task_number': 21,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed    
            },
        'task22': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Total Revenue',
            "task_description": "Based on transactions data, calculate the final total revenue item in the income statement.",
            'task_answer': {'Total Revenue':df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0]},
            'task_number': 22,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task23': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Cost of Goods Sold',
            "task_description": "Based on transactions data, calculate the final cost of goods sold item in the income statement.",
            'task_answer': {'Cost of Goods Sold':df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]},
            'task_number': 23,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task24': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Total Cost',
            "task_description": "Based on transactions data, calculate the final total cost item in the income statement.",
            'task_answer': {'Total Cost':df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0]},
            'task_number': 24,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task25': {
            'task_type': 'income statement generation',
            'task_difficulty':(1,1,1),
            'task_name': 'Income Statement-Gross Profit',
            "task_description": "Based on transactions data, calculate the final gross profit item in the income statement.",
            'task_answer': 
                {'Gross Profit': (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
                    df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0])},
            'task_number': 25,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task26': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Depreciation',
            "task_description": "Based on transactions data, calculate the final depreciation item in the income statement.",
            'task_answer':{'Depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0]},
            'task_number': 26,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task27': {
            'task_type': 'income statement generation',
            'task_difficulty':(1,1,1),
            'task_name': 'Income Statement-Administrative Expenses',
            "task_description": "Based on transactions data, calculate the final administrative expenses item in the income statement.",
            'task_answer':{'Administrative Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0]},
            'task_number': 27,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed    
            },
        'task28': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Sales Expenses',
            "task_description": "Based on transactions data, calculate the final sales expenses item in the income statement.",
            'task_answer': {'Selling Expenses':df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0]},
            'task_number': 28,
            'data_source': 'all transactions data',
            'output': "The final total value of Sales Expenses",
            'data': csv_path_transaction,
            'seed': seed
        },
        'task29': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Financial Expenses',
            "task_description": "Based on transactions data, calculate the final financial expenses item in the income statement.",
            'task_answer': {'Financial Expenses':df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0]},
            'task_number': 29,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task30': {
            'task_type': 'income statement generation',
            'task_difficulty': (4,1,1),
            'task_name': 'Income Statement-Total Expenses',
            "task_description": "Based on transactions data, calculate the final total expenses item in the income statement.",
            'task_answer': {'Total Expenses':df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0]},
            'task_number': 30,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task31': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Interest Income',
            "task_description": "Based on transactions data, calculate the final interest income item in the income statement.",
            'task_answer': {'Interest Income':df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]},
            'task_number': 31,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task32': {
            'task_type': 'income statement generation',
            'task_difficulty': (7,1,1),
            'task_name': 'Income Statement-Profit Before Tax',
            "task_description": "Based on transactions data, calculate the final profit before tax item in the income statement.",
            'task_answer': {'Profit Before Tax':df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0]},
            'task_number': 32,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task33': {
            'task_type': 'income statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Income Statement-Tax Expense',
            "task_description": "Based on transactions data, calculate the final tax expense item in the income statement.",
            'task_answer': {'Tax Expense':df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]},
            'task_number': 33,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task34': {
            'task_type': 'income statement generation',
            'task_difficulty': (8,1,1),
            'task_name': 'Income Statement-Net Profit',
            "task_description": "Based on transactions data, calculate the final net profit item in the income statement.",
            'task_answer': {'Net Profit':df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0]},
            'task_number': 34,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task35': {
            'task_type': 'income statement generation',
            'task_difficulty': (31,1,1),
            'task_name': 'Income Statement-Income Statement',
            "task_description": "Based on transactions data, directly generate a complete income statement.",
            'task_answer': {
        'Main Business Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0],
        'Total Revenue': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
        'Cost of Goods Sold': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0],
        'Total Cost': df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0],
        'Gross Profit': df_income_statement.loc[df_income_statement['Account'] == 'Gross Profit', 'Amount'].values[0],
        'Administrative Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0],
        'Selling Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
        'Depreciation': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0],
        'Financial Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0],
        'Total Expenses': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
        'Interest Income': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0],
        'Profit Before Tax': df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0],
        'Tax Expense': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0],
        'Net Profit': df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0]
    },
            'task_number': 35,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task36': {
            'task_type': 'cash flow statement generation',
            'task_difficulty':(8,1,1),
            'task_name': 'Cash Flow Statement-Net profit',
            "task_description": "Based on transactions data, calculate the final net profit item in the cash flow statement.",
            'task_answer':{'Net Profit': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0]},
            'task_number': 36,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task37': {
            'task_type': 'cash flow statement generation',
            'task_difficulty':(1,1,1),
            'task_name': 'Cash Flow Statement-Depreciation',
            "task_description": "Based on transactions data, calculate the final depreciation item in the cash flow statement.",
            'task_answer': {'Depreciation':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0]},
            'task_number': 37,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task38': {
            'task_type': 'cash flow statement generation',
            'task_difficulty':(1,1,1),
            'task_name': 'Cash Flow Statement-Accounts Receivable',
            "task_description": "Based on transactions data, calculate the final accounts receivable item in the cash flow statement.",
            'task_answer': {'(Increase) Decrease in Accounts Receivable':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0]},
            'task_number': 38,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task39': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Cash Flow Statement-Interest Receivable',
            "task_description": "Based on transactions data, calculate the final interest receivable item in the cash flow statement.",
            'task_answer': {'(Increase) Decrease in Interest Receivable':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Interest Receivable', 'Amount'].values[0]},
            'task_number': 39,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task40': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Cash Flow Statement-Inventory',
            "task_description": "Based on transactions data, calculate the final inventory item in the cash flow statement.",
            'task_answer': {'(Increase) Decrease in Inventory':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0]},
            'task_number': 40,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task41': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Cash Flow Statement-Accounts Payable',
            "task_description": "Based on transactions data, calculate the final accounts payable item in the cash flow statement.",
            'task_answer': {'Increase (Decrease) in Accounts Payable':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0]},
            'task_number': 41,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task42': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Cash Flow Statement-Tax Payable',
            "task_description": "Based on transactions data, calculate the final tax payable item in the cash flow statement.",
            'task_answer': {'Increase (Decrease) in Tax Payable':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0]},
            'task_number': 42,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task43': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (14,1,1),
            'task_name': 'Cash Flow Statement-Net Cash Flow from Operating Activities',
            
            "task_description": "Based on transactions data, calculate the final net cash flow from operating activities in the cash flow statement.",
            'task_answer': {'Net Cash Flow from Operating Activities':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0]},
            'task_number': 43,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task44': {
            'task_type': 'cash flow statement generation',
            'task_difficulty':(1,1,1) ,
            'task_name': 'Cash Flow Statement-Purchase of Fixed Assets',
            "task_description": "Based on transactions data, calculate the final purchase of fixed assets in the cash flow statement.",
            'task_answer': {'Purchase of Fixed Assets':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]},
            'task_number': 44,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task45': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (1,1,1),
            'task_name': 'Cash Flow Statement-Net Cash Flows from Investing Activities',
            "task_description": "Based on transactions data, calculate the final net cash flows from investing activities in the cash flow statement.",
            'task_answer': {'Net Cash Flow from Investing Activities':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0]},
            'task_number': 45,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task46': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (2,1,1),
            'task_name': 'Cash Flow Statement-Beginning Cash and Cash Equivalents Balance',
            "task_description": "Based on transactions data, calculate the final beginning cash and cash equivalents balance in the cash flow statement.",
            'task_answer': {'Beginning Balance':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]},
            'task_number': 46,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task47': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (2,1,1),
            'task_name': 'Cash Flow Statement-Ending Cash and Cash Equivalents Balance',
            "task_description": "Based on transactions data, calculate the final ending cash and cash equivalents balance in the cash flow statement.",
            'task_answer': {'Ending Balance':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0]},
            'task_number': 47,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task48': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (4,1,1),
            'task_name': 'Cash Flow Statement-Net Increase',
            "task_description": "Based on transactions data, calculate the final net increase in cash and cash equivalents in the cash flow statement.",
            'task_answer': {'Net Increase':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]},
            'task_number': 48,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        },
        'task49': {
            'task_type': 'cash flow statement generation',
            'task_difficulty': (38,1,1),
            'task_name': 'Cash Flow Statement-Cash Flow Statement',
            "task_description": "Based on transactions data, directly generate a complete cash flow statement.",
            'task_answer': {
        'Cash Flow From Operating Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Cash Flow From Operating Activities', 'Amount'].values[0],
        'Net Profit': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0],
        'Depreciation': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0],
        '(Increase) Decrease in Accounts Receivable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0],
        '(Increase) Decrease in Interest Receivable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Interest Receivable', 'Amount'].values[0],
        '(Increase) Decrease in Inventory': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0],
        'Increase (Decrease) in Accounts Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0],
        'Increase (Decrease) in Tax Payable': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0],
        'Net Cash Flow from Operating Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0],
        'Cash Flow from Investing Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Cash Flow from Investing Activities', 'Amount'].values[0],
        'Purchase of Fixed Assets': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0],
        'Net Cash Flow from Investing Activities': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0],
        'Cash and Cash Equivalents': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Cash and Cash Equivalents', 'Amount'].values[0],
        'Beginning Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0],
        'Ending Balance': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0],
        'Net Increase': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]
    },
            'task_number': 49,
            'data_source': 'all transactions data',
            'data': csv_path_transaction,
            'seed': seed
        }
        
    }
        print(result_dict['task25'])
        
        
    
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