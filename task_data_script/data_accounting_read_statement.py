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
        json_save_path = os.path.join(json_seed_dir, 'data_accounting_read_statement.json')

        # 定义 CSV 文件路径
        csv_path_balance_sheet = os.path.join(data_seed_dir, 'balance_sheet.csv')
        csv_path_income_statement = os.path.join(data_seed_dir, 'income_statement.csv')
        csv_path_cash_flow_statement = os.path.join(data_seed_dir, 'cash_flow_statement.csv')
        csv_path_transaction = os.path.join(data_seed_dir, 'transactions.csv')

        try:
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
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 1,
                'task_name': 'understand balance sheet-cash on hand',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of cash held by an entity that is available for use in its day-to-day operations, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {'initial value':df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'Initial_amount'].values[0], 'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'End_amount'].values[0]},
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task2': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 2,
                'task_name': 'understand balance sheet-bank deposits',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of funds deposit into a bank, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task3': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 3,
                'task_name': 'understand balance sheet-accounts receivable',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of amounts owed to the entity for goods or services sold or provided on credit,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task4': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 4,
                'task_name': 'understand balance sheet-interest receivable',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of amounts of interest accrued but not yet received,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task5': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 5,
                'task_name': 'understand balance sheet-inventory',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of assets held for sale in the ordinary course of business, in production for such sale, or in the process of being manufactured,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task6': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 6,
                'task_name': 'understand balance sheet-fixed assets',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of tangible items that are held for use in the production or supply of goods or services, for rental to others, or for administrative purposes,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task7': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 7,
                'task_name': 'understand balance sheet-accumulated depreciation',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of expense in the statement of profit or loss and other comprehensive income,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task8': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 8,
                'task_name': 'understand balance sheet-accounts payable',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of the amounts owed by the entity for goods or services received or purchased on credit,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task9': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 9,
                'task_name': 'understand balance sheet-tax payable',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of tax accrued but not yet paid,including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task10': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of capital contributed by shareholders in exchange for shares,including initial and final value",
                'task_number': 10,
                'task_name': 'understand balance sheet-paid-in capital',
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task11': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 11,
                'task_name': 'understand balance sheet-retained earnings',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of profit or loss retained in the entity, rather than being distributed to shareholders, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Retained Earnings', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task12': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 12,
                'task_name': 'understand balance sheet-current assets',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of total assets that are expected to be realised or intended for sale or consumption in the normal course of the entity's operating cycle, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task13': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 13,
                'task_name': 'understand balance sheet-non-current assets',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of total assets that are not expected to be realised or intended for sale or consumption in the normal course of the entity's operating cycle, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Non-current Assets', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task14': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 14,
                'task_name': 'understand balance sheet-current liabilities',
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of total amount of liabilities that are expected to be settled in the normal course of the entity's operating cycle, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task15': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 15,
                'task_name': "understand balance sheet-owner's equity",
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of total amount of equity recognised in the statement of financial position, including initial and final value",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task16': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 16,
                'task_name': "understand balance sheet-total liabilities and owner's equity",
                "task_description": "Based on the balance sheet, identify and extract the specific line items and value of the total amount of liabilities and equity recognised in the statement of financial position,along with the relevant financial data involved in the calculation, including initial and final value. In addition, decompose this item into 2 component sub-items, all of which must also originate from the input statement. For each sub-item, output its initial and final values.",
                'task_difficulty': (5,1,5),
                'task_answer': {
                    "initial value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'Initial_amount'].values[0],
                    "end value": df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Liabilities and Owner's Equity", 'End_amount'].values[0],
                    'sub_items': {
                    'initial sub_item value1' : df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'Initial_amount'].values[0],
                    'end sub_item value1' :df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                    'initial sub_item value2' :df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0],
                    'end sub_item value2' :df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
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
                "task_description": "Based on the balance sheet, identify and extract the two specific line items and value of amounts owed to the entity for goods or services sold or provided on credit and the amounts owed by the entity for goods or services received or purchased on credit,including initial and final value. For multiple outputs, maintain the original line item order as shown in the input statement. ",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'initial value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'Initial_amount'].values[0],
                    'end valu1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0],
                    'initial value2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
                    'end valu2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task18': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 18,
                'task_name': 'understand balance sheet-cash on hand & fixed assets & tax payable',
                "task_description": "Based on the balance sheet, identify and extract the three specific line items and value of cash held by an entity that is available for use in its day-to-day operations, tangible items that are held for use in the production or supply of goods or services, for rental to others, or for administrative purposes and the amounts of tax accrued but not yet paid,including initial and final value. For multiple outputs, maintain the original line item order as shown in the input statement. ",
                'task_difficulty': (3,1,3),
                'task_answer': {
                    'initial value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'Initial_amount'].values[0],
                    'end valu1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Cash on Hand', 'End_amount'].values[0],
                    'initial value2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'Initial_amount'].values[0],
                    'end valu2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Fixed Assets', 'End_amount'].values[0],
                    'initial value3': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
                    'end valu3': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task19': {
                'data': csv_path_balance_sheet,
                'task_type': 'accounting_read statement',
                'task_number': 19,
                'task_name': 'understand balance sheet-interest receivable & accumulated depreciation & tax payable & paid-in capital',
                "task_description": "Based on the balance sheet, identify and extract the four specific line items and value of amounts of interest accrued but not yet received, accumulated the systematic allocation of the depreciable amount of an asset over its useful life, tax payable and capital contributed by shareholders in exchange for shares,including initial and final value. For multiple outputs, maintain the original line item order as shown in the input statement. ",
                'task_difficulty': (4,1,4),
                'task_answer': {
                    'initial value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
                    'end valu1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
                    'initial value2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'Initial_amount'].values[0],
                    'end valu2': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accumulated Depreciation', 'End_amount'].values[0],
                    'initial value3': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'Initial_amount'].values[0],
                    'end valu3': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0],
                    'initial value4': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
                    'end valu4': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
                },
                'data_source': 'balance_sheet',
                'seed': seed,
            },
            'task20': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 20,
                'task_name': 'understand income statement-cost of goods sold',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of carrying amount of inventories sold during the reporting period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
                }, 
                'data_source': 'income statement',
                'seed': seed,
            },
            'task21': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 21,
                'task_name': 'understand income statement-main business revenue',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of income arising in the course of the entity's core operating activities ",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]
                },  
                'data_source': 'income statement',
                'seed': seed,
            },
            'task22': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 22,
                'task_name': 'understand income statement-gross profit',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of difference between revenue and cost",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Gross Profit', 'Amount'].values[0]
                }, 
                'data_source': 'income statement',
                'seed': seed,
            },
            'task23': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 23,
                'task_name': 'understand income statement-interest income',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of income earned by an entity from financial assets ",
                'task_difficulty':(1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task24': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 24,
                'task_name': 'understand income statement-administrative expenses',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of costs of general management and administration of the entity as a whole ",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task25': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 25,
                'task_name': 'understand income statement-selling expenses',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of costs incurred to secure customer orders and to deliver the goods and services to customers ",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task26': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 26,
                'task_name': 'understand income statement-financial expenses',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of financing costs incurred by an enterprise to raise funds needed for production and operation ",
                'task_difficulty': (1,1,1),
                'task_answer': {
                
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0]
                }, 
                'data_source': 'income statement',
                'seed': seed,
            },
            'task27': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 27,
                'task_name': 'understand income statement-accumulated depreciation',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of accumulated the systematic allocation of the depreciable amount of an asset over its useful life",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task28': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 28,
                'task_name': 'understand income statement-tax expense',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of total amount of tax an entity is expected to pay or recover during a reporting period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task29': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 29,
                'task_name': 'understand income statement-total revenue',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of total income arising in the course of an entity’s ordinary activities, along with the values and names of its constituent line items. In addition, decompose this item into 1 component sub-items, all of which must also originate from the input statement. For each sub-item, output its initial and final values. ",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]
                    }
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task30': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 30,
                'task_name': 'understand income statement-total expenses',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of the total amount of expenses incurred by an entity during a reporting period, along with the relevant financial data involved in the calculation. In addition, decompose this item into 4 component sub-items, all of which must also originate from the input statement. For each sub-item, output its initial and final values.",
                'task_difficulty': (5,1,5),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value1': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0],
                        'sub_item value2': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
                        'sub_item value3': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                        'sub_item value4': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0]
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
                "task_description": "Based on the income statement, identify and extract the specific line items and value of profit or loss for a period before deducting tax expense, along with the relevant financial data involved in the calculation. In addition, decompose this item into 4 component sub-items, all of which must also originate from the input statement. For each sub-item, output its initial and final values.",
                'task_difficulty': (5,1,5),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0],
                    'sub_items': {
                        
                        'sub_item value1': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                        'sub_item value2': df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0],
                        'sub_item value3': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
                        'sub_item value4': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
                        
                    }
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task32': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                "task_description": "Based on the income statement, identify and extract the specific line items and value of the amount of profit an entity retains after all expenses, including operating costs, interest, tax, depreciation, and amortization, have been deducted from total revenue, along with the relevant financial data involved in the calculation. In addition, decompose this item into 5 component sub-items, all of which must also originate from the input statement. For each sub-item, output its initial and final values. ",
                'task_number': 32,
                'task_name': 'understand income statement-net profit',
                'task_difficulty': (6,1,6),
                'task_answer': {
                    'value': df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value1': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                        'sub_item value2': df_income_statement.loc[df_income_statement['Account'] == 'Total Cost', 'Amount'].values[0],
                        'sub_item value3': df_income_statement.loc[df_income_statement['Account'] == 'Total Expenses', 'Amount'].values[0],
                        'sub_item value4': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0],
                        'sub_item value5': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
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
                "task_description": "Based on the income statement, identify and extract the two specific line items and value of income arising in the course of the entity's core operating activities and carrying amount of inventories sold during the reporting period. For multiple outputs, maintain the original line item order as shown in the input statement. ",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'value1': df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0],
                    'value2': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task34': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 34,
                'task_name': 'understand income statement-total revenue & Cost of Goods Sold & administrative expenses',
                "task_description": "Based on the income statement, identify and extract the three specific line items and value of total income arising in the course of an entity’s ordinary activities, carrying amount of inventories sold during the reporting period, and costs of general management and administration of the entity as a whole. For multiple outputs, maintain the original line item order as shown in the input statement.",
                'task_difficulty': (3,1,3),
                'task_answer': {
                    'value1': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                    'value2': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0],
                    'value3': df_income_statement.loc[df_income_statement['Account'] == 'Administrative Expenses', 'Amount'].values[0]
                }, 
                'data_source': 'income statement',
                'seed': seed,
            },
            'task35': {
                'data': csv_path_income_statement,
                'task_type': 'accounting_read statement',
                'task_number': 35,
                'task_name': 'understand income statement-selling expenses & depreciation & financial expenses & tax expense',
                "task_description": "Based on the income statement, identify and extract the four specific line items and value of costs incurred to secure customer orders and to deliver the goods and services to customers, financing costs incurred by an enterprise to raise funds needed for production and operation, the systematic allocation of the depreciable amount of an asset over its useful life, and total amount of taxes an entity is expected to pay or recover during a reporting period. For multiple outputs, maintain the original line item order as shown in the input statement.",
                'task_difficulty': (4,1,4),
                'task_answer': {
                    'value1': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
                    'value2': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                    'value3': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0],
                    'value4': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
                },
                'data_source': 'income statement',
                'seed': seed,
            },
            'task36': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 36,
                'task_name': 'understand cash flow statement-net profit',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of the amount of profit an entity retains after all expenses, including operating costs, interest, tax, depreciation, and amortization, have been deducted from total revenue",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task37': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 37,
                'task_name': 'understand cash flow statement-depreciation',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of the systematic allocation of the depreciable amount of an asset over its useful life",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task38': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 38,
                'task_name': 'understand cash flow statement-decrease in accounts receivable',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of decrease in amounts owed to the entity for goods or services sold or provided on credit during the period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task39': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 39,
                'task_name': 'understand cash flow statement-decrease in inventory',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of reduction in the amount of assets held for sale in the ordinary course of business, in production for such sale, or in the process of being manufactured during the period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task40': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 40,
                'task_name': 'understand cash flow statement-increase in accounts payable',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of the addition in the amount owed by the entity for goods or services received or purchased on credit during the period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task41': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 41,
                'task_name': 'understand cash flow statement-increase in tax payable',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of increase in the amounts of tax accrued but not yet paid",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task42': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 42,
                'task_name': 'understand cash flow statement-Purchase of fixed assets',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of cash payments to acquire property, plant and equipment and other long-term assets",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task43': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 43,
                'task_name': 'understand cash flow statement-Beginning Cash and Cash Equivalents Balance',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of cash and cash equivalents at the beginning of the period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task44': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 44,
                'task_name': 'understand cash flow statement-Ending Cash and Cash Equivalents Balance',
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of cash and cash equivalents at the end of the period",
                'task_difficulty': (1,1,1),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task45': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 45,
                'task_name': 'understand cash flow statement-net cash flow from operating activities',
                "task_description": "Based on the net cash flow statement, identify and extract the specific line items and value of net amount of cash and cash equivalents generated from an entity's activities that are the principal revenue-producing activities of the entity and other activities that are not investing or financing activities, along with the relevant financial data involved in the calculation. In addition, decompose this item into 7 component sub-items, all of which must also originate from the input statement. For each sub-item, output its final value.",
                'task_difficulty': (7,1,7),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value1': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0],
                        'sub_item value2':df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                        'sub_item value3': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Accounts Receivable', 'Amount'].values[0],
                        'sub_item value4': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Interest Receivable', 'Amount'].values[0],
                        'sub_item value5': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0],
                        'sub_item value6': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0],
                        'sub_item value7': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Tax Payable', 'Amount'].values[0]
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
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of net amount of cash and cash equivalents generated from an entity's activities that are the acquisition and disposal of long-term assets and other investments not included in cash equivalents and the receipt of interest and dividends, along with the relevant financial data involved in the calculation. In addition, decompose this item into 1 component sub-items, all of which must also originate from the input statement. For each sub-item, output its final value.",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
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
                "task_description": "Based on the cash flow statement, identify and extract the specific line items and value of net addition in the amount of cash and cash equivalents during the period, along with the relevant financial data involved in the calculation. In addition, decompose this item into 2 component sub-items, all of which must also originate from the input statement. For each sub-item, output its final value.",
                'task_difficulty': (3,1,3),
                'task_answer': {
                    'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0],
                    'sub_items': {
                        'sub_item value1': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0],
                        'sub_item value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0]
                    }
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
                'task48': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 48,
                'task_name': 'understand cash flow statement-net profit & purchase of fixed assets',
                "task_description": "Based on the cash flow statement, identify and extract the two specific line items and value of the amount of profit an entity retains after all expenses, including operating costs, interest, tax, depreciation, and amortization, have been deducted from total revenue and cash payments to acquire property, plant and equipment and other long-term assets. For multiple outputs, maintain the original line item order as shown in the input statement.",
                'task_difficulty': (2,1,2),
                'task_answer': {
                    'value1': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0],
                    'value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task49': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 49,
                'task_name': 'understand cash flow statement-increase in accounts payable & purchase of fixed assets & beginning cash and cash equivalents balance',
                "task_description": "Based on the cash flow statement, identify and extract the three specific line items and value of the addition in the amount owed by the entity for goods or services received or purchased on credit during the period, acquisition of property, plant and equipment, and cash and cash equivalents at the beginning of the period. For multiple outputs, maintain the original line item order as shown in the input statement.",
                'task_difficulty': (3,1,3),
                'task_answer': {
                    'value1': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Increase (Decrease) in Accounts Payable', 'Amount'].values[0],
                    'value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0],
                    'value3': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
                },
                'data_source': 'cash flow statement',
                'seed': seed,
            },
            'task50': {
                'data': csv_path_cash_flow_statement,
                'task_type': 'accounting_read statement',
                'task_number': 50,
                'task_name': 'understand cash flow statement-depreciation & decrease in inventory & net cash flow from investing activities & net increase',
                "task_description": "Based on the cash flow statement, identify and extract the four specific line items and value of the systematic allocation of the depreciable amount of an asset over its useful life, reduction in the amount of assets held for sale in the ordinary course of business, in production for such sale, or in the process of being manufactured during the period, net amount of cash and cash equivalents generated from an entity's activities that are the acquisition and disposal of long-term assets and other investments not included in cash equivalents and the receipt of interest and dividends, and net addition in the amount of cash and cash equivalents during the period. For multiple outputs, maintain the original line item order as shown in the input statement.",
                'task_difficulty': (4,1,4),
                'task_answer': {
                    'value1': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Depreciation', 'Amount'].values[0],
                    'value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == '(Increase) Decrease in Inventory', 'Amount'].values[0],
                    'value3': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Investing Activities', 'Amount'].values[0],
                    'value4': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]
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
                "task_description": "Based on the all financial statements, identify and extract the specific line items and value of amounts of interest accrued but not yet received,including initial and final value",
                'task_difficulty': (1,3,1),
                'task_answer': {
                    'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'Initial_amount'].values[0],
                    'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
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
            "task_description": 'Based on the financial statement, identify and extract the specific line items and value of capital contributed by shareholders in exchange for shares,including initial and final value',
            'task_number': 52,
            'task_name': 'understand financial statement-paid-in capital',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'initial value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'Initial_amount'].values[0],
                'end value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0]
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
            "task_description": 'Based on the financial statement, identify and extract the specific line items and value of carrying amount of inventories sold during the reporting period',
            'task_name': 'understand financial statement-cost of goods sold',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]
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
            "task_description":'Based on the financial statement, identify and extract the specific line item and value of costs incurred to secure customer orders and to deliver the goods and services to customers' ,
            'task_number': 54,
            'task_name': 'understand financial statement-selling expenses',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0]
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
            "task_description": 'Based on the financial statement, identify and extract the specific line items and value of total amount of tax an entity is expected to pay or recover during a reporting period',
            'task_number': 55,
            'task_name': 'understand financial statement-tax expense',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_income_statement.loc[df_income_statement['Account'] == 'Tax Expense', 'Amount'].values[0]
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
            "task_description": 'Based on the financial statement, identify and extract the specific line items and value of the systematic allocation of the depreciable amount of an asset over its useful life',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_income_statement.loc[df_income_statement['Account'] == 'Depreciation', 'Amount'].values[0]
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
            "task_description": 'Based on the financial statement, identify and extract the specific line items and value of the addition in the amount owed by the entity for goods or services received or purchased on credit during the period',
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0]
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
            "task_description":'Based on the financial statement, identify and extract the specific line items and value of cash and cash equivalents at the beginning of the period' ,
            'task_difficulty': (1,3,1),
            'task_answer': {
                'value': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Beginning Balance', 'Amount'].values[0]
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
            "task_description": "Based on the all financial statements, identify and extract the two specific line items and end value of amounts of interest accrued but not yet received, and net addition in the amount of cash and cash equivalents during the period. For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.",
            'task_difficulty': (2,3,2),
            'task_answer': {
                    'value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Interest Receivable', 'End_amount'].values[0],
                'value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Increase', 'Amount'].values[0]
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
            "task_description": 'Based on the all financial statements, identify and extract the two specific line items and end value of funds deposit into a bank, and income earned by an entity from financial assets. For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.',
            'task_difficulty': (2,3,2),
            'task_answer': {
                'value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Bank Deposits', 'End_amount'].values[0],
                'value2': df_income_statement.loc[df_income_statement['Account'] == 'Interest Income', 'Amount'].values[0]
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
            "task_description": 'Based on the all financial statements, identify and extract the two specific line items and value of costs incurred to secure customer orders and to deliver the goods and services to customers, and cash payments to acquire property, plant and equipment and other long-term assets. For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.',
            'task_difficulty': (2,3,2),
            'task_answer': {
                'value1': df_income_statement.loc[df_income_statement['Account'] == 'Selling Expenses', 'Amount'].values[0],
                'value2': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
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
            "task_description":'Based on the all financial statements, identify and extract the three specific line items and end value of amounts owed to the entity for goods or services sold or provided on credit, financing costs incurred by an enterprise to raise funds needed for production and operation, and cash payments to acquire property, plant and equipment and other long-term assets. For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.' ,
            'task_difficulty': (3,3,3),
            'task_answer': {
                'value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0],
                'value2': df_income_statement.loc[df_income_statement['Account'] == 'Financial Expenses', 'Amount'].values[0],
                'value3': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0]
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
            'task_name': 'understand financial statement-tax payable & total revenue & net cash flow from operating activities',
            "task_description": "Based on the all financial statements, identify and extract the three specific line items and end value of net amount of cash and cash equivalents generated from an entity's activities that are the principal revenue-producing activities of the entity and other activities that are not investing or financing activities, the amounts of taxes accrued but not yet paid, and total income arising in the course of an entity’s ordinary activities . For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.",
            'task_difficulty': (3,3,3),
            'task_answer': {
                'value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Taxes Payable', 'End_amount'].values[0],
                'value2': df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0],
                'value3': df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0]        
                
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
            'task_name': 'understand financial statement- paid-in capital & profit before tax & increase in accounts payable',
            "task_description":'Based on the all financial statements, identify and extract the three specific line items and end value of profit or loss for a period before deducting tax expense, the addition in the amount owed by the entity for goods or services received or purchased on credit during the period, and capital contributed by shareholders in exchange for shares. For multiple outputs, group them by financial statement in the following order: 1.Balance Sheet 2.Income Statement 3.Cash Flow Statement. Within each group, maintain the original line item order as shown in the input statement.',
            'task_difficulty': (3,3,3),
            'task_answer': {
                'value1': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Paid-in Capital', 'End_amount'].values[0],
                'value2': df_income_statement.loc[df_income_statement['Account'] == 'Profit Before Tax', 'Amount'].values[0],
                'value3': df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'End_amount'].values[0] - df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Payable', 'Initial_amount'].values[0],
                },
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
        except FileNotFoundError as e:
            print(f"File not found for config: {config}, seed: {seed}. Error: {e}")
        except Exception as e:
            print(f"An error occurred for config: {config}, seed: {seed}. Error: {e}")