import pandas as pd
import csv
import json
import math
import numpy as np
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

config_name = {
    'config_chemistry': ['240', '249', '293', '330', '678', '54'],
    'config_consulting': ['171', '348', '380', '538', '565', '590'],
    'config_hotel': ['66', '173', '174', '226', '644', '713'],
    'config_sales': ['111', '245', '511', '589', '660', '706'],
    'config_big_manufactory': ['226', '263', '716', '827', '849', '908']
}


# 设置 NumPy 打印选项
np.set_printoptions(precision=2, suppress=True)

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Project root directory: {project_root}")

# 遍历每个配置和种子值
for config, seeds in config_name.items():
    for seed in seeds:
        print(f"Processing config: {config}, seed: {seed}")

        # 定义路径
        json_dir = os.path.join(project_root, 'strctured_data', config)
        data_dir = os.path.join(project_root, 'simulated_financial_data', config)
        json_seed_dir = os.path.join(json_dir, f'{config}_{seed}')
        data_seed_dir_save = os.path.join(data_dir, f'{config}_{seed}')
        data_seed_dir = os.path.join('.\\simulated_financial_data\\' + str(config), f'{config}_{seed}')

        # 打印路径并创建目录
        print(f"JSON Seed Directory: {json_seed_dir}")
        os.makedirs(json_seed_dir, exist_ok=True)

        # 定义 JSON 保存路径
        json_save_path = os.path.join(json_seed_dir, 'data_consulting.json')

        # 定义 CSV 文件路径
        csv_path_balance_sheet = os.path.join(data_seed_dir, 'balance_sheet.csv')
        csv_path_income_statement = os.path.join(data_seed_dir, 'income_statement.csv')
        csv_path_cash_flow_statement = os.path.join(data_seed_dir, 'cash_flow_statement.csv')
        csv_path_transaction = os.path.join(data_seed_dir, 'transactions.csv')

        # 读取 CSV 文件
        try:
            df_balance_sheet = pd.read_csv(data_seed_dir_save + '/balance_sheet.csv')
            df_income_statement = pd.read_csv(data_seed_dir_save + '/income_statement.csv')
            df_cash_flow_statement = pd.read_csv(data_seed_dir_save + '/cash_flow_statement.csv')
            df_cash_transaction = pd.read_csv(data_seed_dir_save + '/transactions.csv')
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

        # 数据清理
        df_balance_sheet.fillna(0, inplace=True)
        df_income_statement.fillna(0, inplace=True)
        df_cash_flow_statement.fillna(0, inplace=True)
        df_cash_transaction.fillna(0, inplace=True)
        df_cash_flow_statement['Account'] = df_cash_flow_statement['Account'].str.strip()

        # 打印数据框的基本信息（可选，用于调试）
        print("\nDataFrame Information:")
        print(f"Balance Sheet: {df_balance_sheet.shape}")
        print(f"Income Statement: {df_income_statement.shape}")
        print(f"Cash Flow Statement: {df_cash_flow_statement.shape}")
        print(f"Transactions: {df_cash_transaction.shape}")
        print(df_cash_flow_statement)
        result_dict = {
        'task1': {
        'data': csv_path_balance_sheet,
        'task_type': ' consulting',
        'task_number': 1,
        'task_name': 'Analyze Balance Sheet-Calculate Current Ratio',
        "task_description": "Based on the balance sheet, calculate the Current Ratio as of the end of the reporting period",
        'task_answer': {
        
    'Current Ratio': "{:.2f}".format(
                    df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] / 
                    df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0]
                )
            },
            'task_difficulty': (2,1,1),
            'data_source': 'balance_sheet',
            'seed': seed
        },

        'task2': {
            'data': csv_path_balance_sheet,
            'task_type': 'consulting',
            'task_number': 2,
            'task_name': 'Analyze Balance Sheet-Calculate Quick Ratio',
            "task_description": "Based on the balance sheet, calculate the Quick Ratio as of the end of the reporting period",
            'task_answer': {
    'Quick Ratio': "{:.2f}".format(
        (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0]
    )


            },
            'task_difficulty': (6,1,1),
            'data_source': 'balance_sheet',
            'seed': seed
        },
        'task3': {
            'data': csv_path_balance_sheet,
            'task_type': 'consulting',
            'task_number': 3,
            'task_name': 'Analyze Balance Sheet-Calculate Debt to Asset Ratio',
            "task_description": "Based on the balance sheet, calculate the Debt to Asset Ratio as of the end of the reporting period",
            'task_answer': {
            
    'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0]
    )


            },
            'task_difficulty':(2,1,1),
            'data_source': 'balance_sheet',
            'seed': seed
        },
        'task4': {
            'data': csv_path_balance_sheet,
            'task_type': 'consulting',
            'task_number': 4,
            'task_name': 'Analyze Balance Sheet-Calculate Debt to Equity Ratio',
            "task_description": "Based on the balance sheet, calculate the Debt to Equity Ratio as of the end of the reporting period",
            'task_answer': {
        
    'Debt to Equity Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0]
    )


            },
            'task_difficulty': (2,1,1),
            'data_source': 'balance_sheet',
            'seed': seed
        },


        'task5': {
            'data': csv_path_income_statement,
            'task_type': 'consulting',
            'task_number': 5,
            'task_name': 'Analyze Income Statement-Gross Profit Margin',
            "task_description": "Based on the income statement, calculate the Gross Profit Margin",
            'task_answer': {
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0]*100
        ) + '%'
    )

            },
            'task_difficulty': (2,1,1),
            'data_source': 'income_statement',
            'seed': seed
        },

        'task6': {
            'data': csv_path_income_statement,
            'task_type': 'consulting',
            'task_number': 6,
            'task_name': 'Analyze Income Statement-Net Profit Margin',
            "task_description": "Based on the income statement, calculate the Net Profit Margin",
            'task_answer': {
                'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
            },
            'task_difficulty': (2,1,1),
            'data_source': 'income_statement',
            'seed': seed
        },

        'task7': {
            'data': csv_path_cash_flow_statement,
            'task_type': 'consulting',
            'task_number': 7,
            'task_name': 'Analyze Cash Flow Statement-FCF',
            "task_description": "Based on the cash flow statement, calculate the FCF",
            'task_answer': {
                'Free Cash Flow (FCF)': "{:.2f}".format(
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] -
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0], 2
    )
    ,
            },
            'task_difficulty': (2,1,1),
            'data_source': 'cash_flow_statement',
            'seed': seed
        },
        'task8': {
            'data': csv_path_cash_flow_statement,
            'task_type': 'consulting',
            'task_number': 8,
            'task_name': 'Analyze Cash Flow Statement-Operating Cash Flow to Net Income Ratio',
            "task_description": "Based on the cash flow statement, calculate the Operating Cash Flow to Net Income Ratio",
            'task_answer': {
                'Operating Cash Flow to Net Income Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0], 2
        )
    ,
            },
            'task_difficulty': (2,1,1),
            'data_source': 'cash_flow_statement',
            'seed': seed
        },
    'task9': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 9,
            'task_name': 'Analyze Cash Flow Statement-Cash to Current Debt Ratio',
            "task_description": "Based on the three financial statements, calculate the Cash to Current Debt Ratio",
            'task_answer': {
                'Cash to Current Debt Ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0], 2
            ),
            },
            'task_difficulty': (2,1,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task10': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 10,
            'task_name': 'Analyze Cash Flow Statement-Operating Cash Flow to Current Liabilities Ratio',
            "task_description": "Based on the three financial statements, calculate the Operating Cash Flow to Current Liabilities Ratio",
            'task_answer': {
                'operating cash flow to current liabilities ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
                2
            ),
            },
            'task_difficulty': (2,1,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
    'task11': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 11,
            'task_name': 'Analyze Financial Statement-ROA',"task_description": "Based on the three financial statements, calculate the ROA",
            'task_answer': {
                'Return on Assets (ROA)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0]  + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0]) *2 * 100 , 2
            )
        ) + '%'
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task12': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 12,
            'task_name': 'Analyze Financial Statement-ROE',
            "task_description": "Based on the three financial statements, calculate the ROE",
            'task_answer': {
            'Return on Equity (ROE)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0] + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0])
                *2 * 100, 2
            )
        ) + '%'
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task13': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 13,
            'task_name': 'Analyze Financial Statement-Inventory Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Inventory Turnover Ratio",
            'task_answer': {
                'Inventory Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0] /2),
            2
        )
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task14': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 14,
            'task_name': 'Analyze Financial Statement-Accounts Receivable Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Accounts Receivable Turnover Ratio",
            'task_answer': {
                'Accounts Receivable Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0] / 2),
            2
        )
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task15': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 15,
            'task_name': 'Analyze Financial Statement-Current Assets Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Current Assets Turnover Ratio",
            'task_answer': {
            'Current Assets Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            ((df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0]+df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0])/2),
            2
        )
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task16': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 16,
            'task_name': 'Analyze Financial Statement-Total Asset Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Total Asset Turnover Ratio",
            'task_answer': {
                'Total Asset Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0] + 
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0])*2, 2
        )
    ,
            },
            'task_difficulty': (3,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },

    'task17': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 17,
            'task_name': 'Analyze Financial Statement-Cash Flow to Debt Ratio',
            "task_description": "Based on the three financial statements, calculate the Cash Flow to Debt Ratio",
            'task_answer': {
                'Cash Flow to Debt Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
        )
    ,
            },
            'task_difficulty': (2,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task18': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 18,
            'task_name': 'Analyze Financial Statement-Operating Cash Flow Ratio',
            "task_description": "Based on the three financial statements, calculate the Operating Cash Flow Ratio",
            'task_answer': {
                'Operating Cash Flow Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
        )
    ,
            },
            'task_difficulty': (2,3,1),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task19': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 19,
            'task_name': 'Analyze Financial Statement-Current Ratio & Inventory Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Current Ratio and Inventory Turnover Ratio",
            'task_answer': {
                
        'Current Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] / 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
        'Inventory Turnover Ratio': 
            "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0] /2),
            2
        ),
            },
            'task_difficulty': (5,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task20': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 20,
            'task_name': 'Analyze Financial Statement-Gross Profit Margin & Operating Cash Flow Ratio',
            "task_description": "Based on the three financial statements, calculate the Gross Profit Margin and Operating Cash Flow Ratio",
            'task_answer': {
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
            'Operating Cash Flow Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
        ),
            },
            'task_difficulty': (4,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task21': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 21,
            'task_name': 'Analyze Financial Statement-FCF & Current Assets Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the FCF and Current Assets Turnover Ratio",
            'task_answer': {
                'Free Cash Flow (FCF)': "{:.2f}".format(
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] -
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0], 2
    ),
                'Current Assets Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            ((df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0]+df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0])/2),
            2
        ),
            },
            'task_difficulty': (5,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task22': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 22,
            'task_name': 'Analyze Financial Statement-Quick Ratio & Net Profit Margin',
            "task_description": "Based on the three financial statements, calculate the Quick Ratio and Net Profit Margin",
            'task_answer': {
                'Quick Ratio': "{:.2f}".format(
        (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
    ),
                'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
            },
            'task_difficulty': (8,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },


    'task23': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 23,
            'task_name': 'Analyze Financial Statement-Gross Profit Margin & Cash Flow to Debt Ratio',
            "task_description": "Based on the three financial statements, calculate the Gross Profit Margin and Cash Flow to Debt Ratio",
            'task_answer': {
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
                'Cash Flow to Debt Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0], 2
        ),
            },
            'task_difficulty': (4,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task24': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 24,
            'task_name': 'Analyze Financial Statement-Debt to Asset Ratio & Operating Cash Flow to Net Income Ratio',
            "task_description": "Based on the three financial statements, calculate the Debt to Asset Ratio and Operating Cash Flow to Net Income Ratio",
            'task_answer': {
            'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0], 2
    )
    ,
                'Operating Cash Flow to Net Income Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0], 2
        ),
            },
            'task_difficulty': (4,3,2),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task25': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 25,
            'task_name': 'Analyze Financial Statement-Debt to Equity Ratio & Net Profit Margin & Operating Cash Flow to Current Liabilities Ratio',
            "task_description": "Based on the three financial statements, calculate the Debt to Equity Ratio, Net Profit Margin and Operating Cash Flow to Current Liabilities Ratio",
            'task_answer': {
            'Debt to Equity Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0], 2
    ),
            
                'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
            'operating cash flow to current liabilities ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
                2
            ),
            },
            'task_difficulty': (6,3,3),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task26': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 26,
            'task_name': 'Analyze Financial Statement-ROE & Debt to Asset Ratio & Gross Profit Margin',
            "task_description": "Based on the three financial statements, calculate the ROE, Debt to Asset Ratio and Gross Profit Margin",
            'task_answer': {
            'Return on Equity (ROE)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0] + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0])
                *2 * 100, 2
            )
        ) + '%',
            'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0], 2
    ),
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
            },
            'task_difficulty': (7,3,3),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task27': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 27,
            'task_name': 'Analyze Financial Statement-Operating Cash Flow to Net Income Ratio & Turnover Ratio & Quick Ratio',
            "task_description": "Based on the three financial statements, calculate the Operating Cash Flow to Net Income Ratio, Turnover Ratio and Quick Ratio",
            'task_answer': {
                'Operating Cash Flow to Net Income Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0], 2
        ),
                'Current Assets Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            ((df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'Initial_amount'].values[0]+df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0])/2),
            2
        ),
                'Quick Ratio': "{:.2f}".format(
        (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
    ),
            },
            'task_difficulty': (11,3,3),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task28': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 28,
            'task_name': 'Analyze Financial Statement-Debt to Asset Ratio & Gross Profit Margin & Operating Cash Flow Ratio',
            "task_description": "Based on the three financial statements, calculate the Debt to Asset Ratio, Gross Profit Margin and Operating Cash Flow Ratio",
            'task_answer': {
                'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0], 2
    ),
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
                'Operating Cash Flow Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
        ),
            },
            'task_difficulty': (6,3,3),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task29': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 29,
            'task_name': 'Analyze Financial Statement-Debt to Equity Ratio & Net Profit Margin & ROA & Accounts Receivable Turnover Ratio',
            "task_description": "Based on the three financial statements, calculate the Debt to Equity Ratio, Net Profit Margin, ROA and Accounts Receivable Turnover Ratio",
            'task_answer': {
                'Debt to Equity Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0], 2
    ),
                'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
                'Return on Assets (ROA)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0]  + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0]) *2 * 100 , 2
            )
        ) + '%',
            
                'Accounts Receivable Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0] / 2),
            2
        ),
            },
            'task_difficulty': (10,3,4),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task30': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 30,
            'task_name': 'Analyze Financial Statement-Current Ratio & Quick Ratio & Debt to Asset Ratio & Debt to Equity Ratio & Cash Flow to Debt Ratio',
            "task_description": "Based on the three financial statements, calculate the Current Ratio, Quick Ratio, Debt to Asset Ratio, Debt to Equity Ratio, Cash Flow to Debt Ratio",
            'task_answer': {
                'Current Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] / 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
                
                'Quick Ratio': "{:.2f}".format(
        (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
    ),
                'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0], 2
    ),
            'Debt to Equity Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0], 2
    ),
                'Cash Flow to Debt Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0], 2
        ),
            },
            'task_difficulty': (14,3,5),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task31': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 31,
            'task_name': 'Analyze Financial Statement-Accounts Receivable Turnover Ratio & Operating Cash Flow to Current Liabilities Ratio & Operating Cash Flow Ratio & Total Asset Turnover Ratio & Debt to Equity Ratio',
            'task_description':' Based on the three financial statements, calculate the Accounts Receivable Turnover Ratio, Operating Cash Flow to Current Liabilities Ratio, Operating Cash Flow Ratio, Total Asset Turnover Ratio and Debt to Equity Ratio',
            'task_answer': {
            'Accounts Receivable Turnover Ratio': 
            "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0] / 2),
            2
        ),
        'operating cash flow ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
                2
            ),
    'operating cash flow to current liabilities ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
                2
            ),
        'Total Asset Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0] + 
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0])*2, 2
        ),
        'Debt to Equity Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
                2
            )
            },
            'task_difficulty': (12,3,5),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task32': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 32,
            'task_name': 'Analyze Financial Statement-FCF & ROA & ROE & Operating Cash Flow to Net Income Ratio & Net Profit Margin & Gross Profit Margin',
            'task_description':'Based on the three financial statements, calculate the FCF, ROA, ROE, Operating Cash Flow to Net Income Ratio, Net Profit Margin and Gross Profit Margin',
            'task_answer': {
                'Free Cash Flow (FCF)': "{:.2f}".format(
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] -
        df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0], 2
    ),
                'Return on Assets (ROA)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0]  + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0]) *2 * 100 , 2
            )
        ) + '%',
            'Return on Equity (ROE)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0] + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0])
                *2 * 100, 2
            )
        ) + '%',
                'Operating Cash Flow to Net Income Ratio': 
        "{:.2f}".format(
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
            df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Profit', 'Amount'].values[0], 2
        ),
            'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
            'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
            },
            'task_difficulty': (14,3,6),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task33': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 33,
            'task_description':'Based on the three financial statements, calculate the Operating Cash Flow Ratio, Cash Flow to Debt Ratio, Inventory Turnover Ratio, Debt to Equity Ratio, Quick Ratio and Current Ratio',
            'task_name': 'Analyze Financial Statement-Operating Cash Flow Ratio & Cash Flow to Debt Ratio & Inventory Turnover Ratio & Debt to Equity Ratio & Quick Ratio & Current Ratio',
            'task_answer': {
                    'Operating Cash Flow Ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
        'Cash Flow to Debt Ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
        'Inventory Turnover Ratio': 
            "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0] /2),
            2
        ),
        'Debt to Equity Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
                2
            ),
        'Quick Ratio': 
            "{:.2f}".format(
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
        'Current Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            )
            },
            'task_difficulty': (17,3,6),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task34': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 34,
            'task_description': 'Based on the three financial statements, calculate the Operating Cash Flow to Current Liabilities Ratio, Debt to Equity Ratio, Total Asset Turnover Ratio, Quick Ratio, Operating Cash Flow Ratio, ROE and Accounts Receivable Turnover Ratio',
            'task_name': 'Analyze Financial Statement-Operating Cash Flow to Current Liabilities Ratio & Debt to Equity Ratio & Total Asset Turnover Ratio & Quick Ratio & Operating Cash Flow Ratio & ROE & Accounts Receivable Turnover Ratio',
            'task_answer': {
            'operating cash flow to current liabilities ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0],
                2
            ),
        'Debt to Equity Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0],
                2
            ),
        'Total Asset Turnover Ratio': 
        "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0] + 
            df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0])*2, 2
        ),
        'Quick Ratio': 
            "{:.2f}".format(
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] -
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Inventory', 'End_amount'].values[0]) /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
        'Operating Cash Flow Ratio': 
            "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
            'Return on Equity (ROE)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'End_amount'].values[0] + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Owner's Equity", 'Initial_amount'].values[0])
                *2 * 100, 2
            )
        ) + '%',
                'Accounts Receivable Turnover Ratio': 
            "{:.2f}".format(
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] /
            (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Accounts Receivable', 'End_amount'].values[0] / 2),
            2
        ),
            },
            'task_difficulty': (21,3,7),
            'data_source': 'all_financial_statements',
            'seed': seed
        },
        'task35': {
            'data': {
                'balance sheet': csv_path_balance_sheet,
                'cash flow': csv_path_cash_flow_statement,
                'income statement': csv_path_income_statement
            },
            'task_type': 'consulting',
            'task_number': 35,
            'task_name': 'Analyze Financial Statement-Current Ratio & Gross Profit Margin & Debt to Asset Ratio & Net Profit Margin & Cash to Current Debt Ratio & FCF & ROA',
            'task_description': 'Based on the three financial statements, calculate the Current Ratio, Gross Profit Margin, Debt to Asset Ratio, Net Profit Margin, Cash to Current Debt Ratio, FCF and ROA',
            'task_answer': {
            'Current Ratio': 
            "{:.2f}".format(
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Assets', 'End_amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0],
                2
            ),
                'Gross Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] - 
            df_income_statement.loc[df_income_statement['Account'] == 'Cost of Goods Sold', 'Amount'].values[0]) /
            df_income_statement.loc[df_income_statement['Account'] == 'Total Revenue', 'Amount'].values[0] * 100, 2
        )
    ) + '%',
                'Debt to Asset Ratio': "{:.2f}".format(
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Current Liabilities', 'End_amount'].values[0] /
        df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0], 2
    ),
            'Net Profit Margin': str(
        "{:.2f}".format(
            (df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
            df_income_statement.loc[df_income_statement['Account'] == 'Main Business Revenue', 'Amount'].values[0]) * 100, 2
        )
    ) + '%',
                'Cash to Current Debt Ratio': "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Ending Balance', 'Amount'].values[0] /
                df_balance_sheet.loc[df_balance_sheet['Account'] == "Total Current Liabilities", 'End_amount'].values[0], 2
            
            ),
                'Free Cash Flow (FCF)': "{:.2f}".format(
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Net Cash Flow from Operating Activities', 'Amount'].values[0] -
                df_cash_flow_statement.loc[df_cash_flow_statement['Account'] == 'Purchase of Fixed Assets', 'Amount'].values[0],
                2
            ),
            'Return on Assets (ROA)': 
        str(
            "{:.2f}".format(
                df_income_statement.loc[df_income_statement['Account'] == 'Net Profit', 'Amount'].values[0] /
                (df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'End_amount'].values[0]  + 
                df_balance_sheet.loc[df_balance_sheet['Account'] == 'Total Assets', 'Initial_amount'].values[0]) *2 * 100 , 2
            )
        ) + '%',
            },
            'task_difficulty': (15,3,7),
            'data_source': 'all_financial_statements',
            'seed': seed
        }

        
    }
        print(result_dict['task5'])
        
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
        def format_number(value):
            """强行保留两位小数的函数"""
            return "{:.2f}".format(value) if isinstance(value, (int, float)) else value

        # 假设 result_dict 已经定义
        
            # 其他类型的值保持不变

        # 输出结果
        

        result_dict = replace_infinity_and_nan(result_dict)
        
        
        
        # 将字典保存为 JSON 文件
        with open(json_save_path, 'w', encoding='utf-8') as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=4)