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
def convert_timestamps(issue_str):
        """
        Convert Timestamp objects to string format in the JSON-like string.
        """
        return issue_str.replace("Timestamp(", "").replace(")", "")
def convert_to_single_dict(data):
    if isinstance(data, dict):
        return data

    result = {}
    key_pairs = [
        ('Original category', 'Recorded category'),
        ('Original date', 'Recorded date'),
        ('Original payment/receipt_status', 'Recorded payment/receipt_status'),
        ('Original payment_method', 'Recorded payment_method'),
        ('Original quantity', 'Recorded quantity'),
        ('Original price', 'Recorded price'),
        ('Original receive_method', 'Recorded receive_method'),
        ('Original amount', 'Recorded amount'),
        ('Original tax', 'Recorded tax'),
        ('Original profit', 'Recorded profit'),
        ('Original Preparer', 'Recorded Preparer'),
        ('Original Approver', 'Recorded Approver')
    ]

    # Initialize all keys with None
    for original_key, recorded_key in key_pairs:
        result[original_key] = None
        result[recorded_key] = None

    for entry in data:
        if 'id' in entry:
            result['id'] = entry['id']
        for original_key, recorded_key in key_pairs:
            if original_key in entry:
                result[original_key] = entry[original_key]
            if recorded_key in entry:
                result[recorded_key] = entry[recorded_key]

    return result



np.set_printoptions(precision=2, suppress=True)

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Project root directory: {project_root}")

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
        json_save_path = os.path.join(json_seed_dir, 'data_auditing.json')

        # 初始化数据结构
        dataframes = {}
        paths = {}
        risk_issues_dict = {}

        # 遍历 1 到 35 的 CSV 文件
        for i in range(1, 36):
            # 定义 CSV 文件路径
            csv_path = os.path.join(data_seed_dir_save, f'audit{i}.csv')
            csv_path_file = os.path.join(data_seed_dir, f'audit{i}.csv')
            paths[f'df_audit{i}'] = csv_path_file

           
            # 读取 CSV 文件
            dataframes[f'df_audit{i}'] = pd.read_csv(csv_path)

            # 查找 'risk_issues' 列中非空的条目
            non_null_issues = dataframes[f'df_audit{i}']['risk_issues'].dropna()

            if len(non_null_issues) == 1:
                issue_str = non_null_issues.iloc[0]
                try:
                    # 转换时间戳为字符串（假设你有一个 convert_timestamps 函数）
                    issue_str = convert_timestamps(issue_str)

                    # 将字符串解析为字典
                    issue_dict = json.loads(issue_str.replace("'", "\""))  # 替换单引号为双引号以便 JSON 解析
                    print(f"Parsed risk issues for df_audit{i}: {issue_dict}")
                    risk_issues_dict[f'df_audit{i}'] = issue_dict
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for df_audit{i}: {e}")
                    print(f"Problematic string: {issue_str}")

            # 填充 NaN 值为 0
            dataframes[f'df_audit{i}'].fillna(0, inplace=True) 
    # Print results
    # if 'df_audit16' in risk_issues_dict:
    #     # print(risk_issues_dict['df_audit16'], len(risk_issues_dict))
        
    #     # Iterate and print key-value pairs in the dictionary
    #     issue = risk_issues_dict['df_audit16']
    #     if isinstance(issue, dict):
    #         for key, value in issue.items():
    #             print(f"{key}: {value}")
    #     else:
    #         print(f"Unexpected element type: {type(issue)}")
    # else:
    #     print("df_audit16 not found in risk_issues_dict")

        print(risk_issues_dict['df_audit5'])
        result_dict = {
        'task1': {
            'data': paths['df_audit1'],
            'task_type': 'Auditing',
            'task_number': 1,
            'task_name': 'Find Record Error - Transaction TYPE Record Error',
            'task_difficulty': (13,1,3),
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit1']),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task2': {
            'data': paths['df_audit2'],
            'task_type': 'Auditing',
            'task_number': 2,
            'task_name': 'Find Record Error - Transaction DATE Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit2']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task3': {
            'data': paths['df_audit3'],
            'task_type': 'Auditing',
            'task_number': 3,
            'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit3']),
            'task_difficulty':(13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task4': {
            'data': paths['df_audit4'],
            'task_type': 'Auditing',
            'task_number': 4,
            'task_name': 'Find Record Error - Transaction PAYMENT_METHOD Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit4']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task5': {
            'data': paths['df_audit5'],
            'task_type': 'Auditing',
            'task_number': 5,
            'task_name': 'Find Record Error - Transaction QUANTITY Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit5']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task6': {
            'data': paths['df_audit6'],
            'task_type': 'Auditing',
            'task_number': 6,
            'task_name': 'Find Record Error - Transaction UNIT_PRICE Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit6']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task7': {
            'data': paths['df_audit7'],
            'task_type': 'Auditing',
            'task_number': 7,
            'task_name': 'Find Record Error - Transaction RECEIVE_METHOD Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit7']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task8': {
            'data': paths['df_audit8'],
            'task_type': 'Auditing',
            'task_number': 8,
            'task_name': 'Find Calculation Error - Transaction AMOUNT Calculation Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit8']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task9': {
            'data': paths['df_audit9'],
            'task_type': 'Auditing',
            'task_number': 9,
            'task_name': 'Find Calculation Error - Transaction TAX_AMOUNT Calculation Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit9']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task10': {
            'data': paths['df_audit10'],
            'task_type': 'Auditing',
            'task_number': 10,
            'task_name': 'Find Calculation Error - Transaction PROFIT Calculation Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit10']),
            'task_difficulty': (13,1,3),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task11': {
            'data': paths['df_audit11'],
            'task_type': 'Auditing',
            'task_number': 11,
            'task_name': 'Find Transaction Approval Mismatch - Transaction Without PREPARER Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit11']),
            'task_difficulty': (13,1,2),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task12': {
            'data': paths['df_audit12'],
            'task_type': 'Auditing',
            'task_number': 12,
            'task_name': 'Find Transaction Approval Mismatch - Transaction Without APPROVER Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit12']),
            'task_difficulty': (13,1,2),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task13': {
            'data': paths['df_audit13'],
            'task_type': 'Auditing',
            'task_number': 13,
            'task_name': 'Find Transaction Approval Mismatch - Transaction Without APPROVER Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit13']),
            'task_difficulty': (13,1,4),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task14': {
            'data': paths['df_audit14'],
            'task_type': 'Auditing',
            'task_number': 14,
            'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Record Error - Transaction QUANTITY Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit14']),
            'task_difficulty': (13,1,4),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task15': {
            'data': paths['df_audit15'],
            'task_type': 'Auditing',
            'task_number': 15,
            'task_name': 'Find Record Error - Transaction QUANTITY Record Error & Record Error - Transaction TYPE Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit15']),
            'task_difficulty': (13,1,4),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task16': {
            'data': paths['df_audit16'],
            'task_type': 'Auditing',
            'task_number': 16,
            'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Calculation Error - Transaction AMOUNT Calculation Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit16']),
            'task_difficulty': (13,1,4),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task17': {
            'data': paths['df_audit17'],
            'task_type': 'Auditing',
            'task_number': 17,
            'task_name': 'Find Record Error - Transaction RECEIVE_METHOD Record Error & Record Error - Transaction TYPE Record Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit17']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task18': {
            'data': paths['df_audit18'],
            'task_type': 'Auditing',
            'task_number': 18,
            'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Record Error - Transaction QUANTITY Record Error & Calculation Error - Transaction PROFIT Calculation Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit18']),
            'task_difficulty': (13,1,7),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task19': {
            'data': paths['df_audit19'],
            'task_type': 'Auditing',
            'task_number': 19,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit19']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task20': {
            'data': paths['df_audit20'],
            'task_type': 'Auditing',
            'task_number': 20,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & PRICE ANOMALY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit20']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task21': {
            'data': paths['df_audit21'],
            'task_type': 'Auditing',
            'task_number': 21,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit21']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task22': {
            'data': paths['df_audit22'],
            'task_type': 'Auditing',
            'task_number': 22,
            'task_name': 'Find Error - RECORDING DELAY Error & PRICE ANOMALY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit22']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task23': {
            'data': paths['df_audit23'],
            'task_type': 'Auditing',
            'task_number': 23,
            'task_name': 'Find Error - RECORDING DELAY Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit23']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task24': {
            'data': paths['df_audit24'],
            'task_type': 'Auditing',
            'task_number': 24,
            'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit24']),
            'task_difficulty': (13,1,5),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task25': {
            'data': paths['df_audit25'],
            'task_type': 'Auditing',
            'task_number': 25,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error & PRICE ANOMALY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit25']),
            'task_difficulty': (13,1,7),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task26': {
            'data': paths['df_audit26'],
            'task_type': 'Auditing',
            'task_number': 26,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit26']),
            'task_difficulty': (13,1,7),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task27': {
            'data': paths['df_audit27'],
            'task_type': 'Auditing',
            'task_number': 27,
            'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit27']),
            'task_difficulty': (13,1,7),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task28': {
            'data': paths['df_audit28'],
            'task_type': 'Auditing',
            'task_number': 28,
            'task_name': 'Find Error - RECORDING DELAY Error & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit28']),
            'task_difficulty': (13,1,7),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task29': {
            'data': paths['df_audit29'],
            'task_type': 'Auditing',
            'task_number': 29,
            'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit29']),
            'task_difficulty': (13,1,9),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task30': {
            'data': paths['df_audit30'],
            'task_type': 'Auditing',
            'task_number': 30,
            'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & TYPE MISCLASSIFICATION Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit30']),
            'task_difficulty': (13,1,9),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task31': {
            'data': paths['df_audit31'],
            'task_type': 'Auditing',
            'task_number': 31,
            'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & QUANTITY MISMATCH Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit31']),
            'task_difficulty': (13,1,9),
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",

            'data_source': 'recorded transaction data',
            'seed': seed,
        },
        'task32': {
            'data': paths['df_audit32'],
            'task_type': 'Auditing',
            'task_number': 32,
            'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & QUANTITY MISMATCH Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit32']),
            'task_difficulty': (13,1,9),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task33': {
            'data': paths['df_audit33'],
            'task_type': 'Auditing',
            'task_number': 33,
            'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit33']),
            'task_difficulty': (13,1,11),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task34': {
            'data': paths['df_audit34'],
            'task_type': 'Auditing',
            'task_number': 34,
            'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error & QUANTITY MISMATCH Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit34']),
            'task_difficulty': (13,1,11),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        },
        'task35': {
            'data': paths['df_audit35'],
            'task_type': 'Auditing',
            'task_number': 35,
            'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error & QUANTITY MISMATCH Error',
            'task_answer': convert_to_single_dict(risk_issues_dict['df_audit35']),
            'task_difficulty': (13,1,11),
            'data_source': 'recorded transaction data',
            "task_description": " Analyze each transaction entry and identify any internal inconsistencies or errors in the recorded information. Some fields—such as invoice—are generally considered more reliable due to their standardized and regulated nature. For each inconsistency you find, output transaction ID, (the incorrect field(s),)their recorded values, and your best estimate of the correct value(s) based on the other fields in that row.",
            'seed': seed,
        }
    }
    
        
        
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
        for task_key, task_value in result_dict.items():
            task_answer = task_value['task_answer']
            
            if isinstance(task_answer, (int, float)):  
                task_value['task_answer'] = "{:.2f}".format(float(task_answer))
            elif isinstance(task_answer, dict): 
                formatted_values = {}
                for k, v in task_answer.items():
                    if v is None:
                        formatted_values[k] = None
                    elif isinstance(v, str):  
                        formatted_values[k] = v
                    else: 
                        formatted_values[k] = "{:.2f}".format(float(v))
                task_value['task_answer'] = formatted_values


        for task_key, task_value in result_dict.items():
            print(f"{task_key}: {task_value['task_answer']}" if task_value['task_answer'] is not None else f"{task_key}: None",len(task_value['task_answer']))
        
        with open(json_save_path, 'w', encoding='utf-8') as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=4)