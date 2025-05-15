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
    for entry in data:
        if 'id' in entry and 'id' not in result:
            result['id'] = entry['id']
        for key, value in entry.items():
            if key != 'id':
                result[key] = value
    return result


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

    os.makedirs(json_seed_dir, exist_ok=True)
    json_save_path = os.path.join(json_seed_dir, 'data_auditing.json')
    dataframes = {}
    paths = {}
    risk_issues_dict = {}

    for i in range(1, 36):
        csv_path =  os.path.join(data_seed_dir_save, 'audit'+str(i)+'.csv')
        csv_path_file = os.path.join(data_seed_dir,  'audit'+str(i)+'.csv')
        paths[f'df_audit{i}'] = csv_path_file
        dataframes[f'df_audit{i}'] = pd.read_csv(csv_path)
        
        # Find non-null entries in the 'risk_issues' column
        non_null_issues = dataframes[f'df_audit{i}']['risk_issues'].dropna()
        
        if len(non_null_issues) == 1:
            issue_str = non_null_issues.iloc[0]
            try:
                # Convert timestamps to strings
                issue_str = convert_timestamps(issue_str)
                # Try to parse the string into a dictionary
                issue_dict = json.loads(issue_str.replace("'", "\""))  # Replace single quotes with double quotes for JSON parsing
                risk_issues_dict[f'df_audit{i}'] = issue_dict
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for df_audit{i}: {e}")
                print(f"Problematic string: {issue_str}")
        
        # Fill NaN values with 0
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
        'task_difficulty': 'easy',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit1']),
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction type matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect recorded type, and the correct type.',
        'seed': seed,
    },
    'task2': {
        'data': paths['df_audit2'],
        'task_type': 'Auditing',
        'task_number': 2,
        'task_name': 'Find Record Error - Transaction DATE Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit2']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction date matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect recorded date, and the correct date.',
        'seed': seed,
    },
    'task3': {
        'data': paths['df_audit3'],
        'task_type': 'Auditing',
        'task_number': 3,
        'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit3']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded payment/receipt status matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect status, and the correct status.',
        'seed': seed,
    },
    'task4': {
        'data': paths['df_audit4'],
        'task_type': 'Auditing',
        'task_number': 4,
        'task_name': 'Find Record Error - Transaction PAYMENT_METHOD Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit4']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded payment method matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect method, and the correct method.',
        'seed': seed,
    },
    'task5': {
        'data': paths['df_audit5'],
        'task_type': 'Auditing',
        'task_number': 5,
        'task_name': 'Find Record Error - Transaction QUANTITY Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit5']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded quantity matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect quantity, and the correct quantity.',
        'seed': seed,
    },
    'task6': {
        'data': paths['df_audit6'],
        'task_type': 'Auditing',
        'task_number': 6,
        'task_name': 'Find Record Error - Transaction UNIT_PRICE Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit6']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded unit price matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect unit price, and the correct unit price.',
        'seed': seed,
    },
    'task7': {
        'data': paths['df_audit7'],
        'task_type': 'Auditing',
        'task_number': 7,
        'task_name': 'Find Record Error - Transaction RECEIVE_METHOD Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit7']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded receive method matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect receive method, and the correct receive method.',
        'seed': seed,
    },
    'task8': {
        'data': paths['df_audit8'],
        'task_type': 'Auditing',
        'task_number': 8,
        'task_name': 'Find Calculation Error - Transaction AMOUNT Calculation Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit8']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded amount matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect amount, and the correct amount.',
        'seed': seed,
    },
    'task9': {
        'data': paths['df_audit9'],
        'task_type': 'Auditing',
        'task_number': 9,
        'task_name': 'Find Calculation Error - Transaction TAX_AMOUNT Calculation Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit9']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded tax amount matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect tax amount, and the correct tax amount.',
        'seed': seed,
    },
    'task10': {
        'data': paths['df_audit10'],
        'task_type': 'Auditing',
        'task_number': 10,
        'task_name': 'Find Calculation Error - Transaction PROFIT Calculation Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit10']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded profit matches the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect profit, and the correct profit.',
        'seed': seed,
    },
    'task11': {
        'data': paths['df_audit11'],
        'task_type': 'Auditing',
        'task_number': 11,
        'task_name': 'Find Transaction Approval Mismatch - Transaction Without PREPARER Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit11']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each approved transaction, verify if the recorded preparer matches the other recorded transaction data. If inconsistent, output the transaction ID and the correct preparer.',
        'seed': seed,
    },
    'task12': {
        'data': paths['df_audit12'],
        'task_type': 'Auditing',
        'task_number': 12,
        'task_name': 'Find Transaction Approval Mismatch - Transaction Without APPROVER Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit12']),
        'task_difficulty': 'easy',
        'data_source': 'recorded transaction data',
        'task_description': 'For each submitted transaction, verify if the recorded approver matches the other recorded transaction data. If inconsistent, output the transaction ID and the correct approver.',
        'seed': seed,
    },
    'task13': {
        'data': paths['df_audit13'],
        'task_type': 'Auditing',
        'task_number': 13,
        'task_name': 'Find Transaction Approval Mismatch - Transaction Without APPROVER Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit13']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each submitted transaction, verify if the recorded approver matches the actual data and the invoice. If inconsistent, output the transaction ID and the correct approver.',
        'seed': seed,
    },
    'task14': {
        'data': paths['df_audit14'],
        'task_type': 'Auditing',
        'task_number': 14,
        'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Record Error - Transaction QUANTITY Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit14']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record,check if the recorded transaction PAYMENT/RECEIPT_STATUS & recorded transaction QUANTITY match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task15': {
        'data': paths['df_audit15'],
        'task_type': 'Auditing',
        'task_number': 15,
        'task_name': 'Find Record Error - Transaction QUANTITY Record Error & Record Error - Transaction TYPE Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit15']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record,check if the recorded transaction QUANTITY & recorded transaction TYPE match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task16': {
        'data': paths['df_audit16'],
        'task_type': 'Auditing',
        'task_number': 16,
        'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Calculation Error - Transaction AMOUNT Calculation Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit16']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each submitted transaction, verify if the recorded transaction PAYMENT/RECEIPT_STATUS & recorded transaction AMOUNT Calculation match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task17': {
        'data': paths['df_audit17'],
        'task_type': 'Auditing',
        'task_number': 17,
        'task_name': 'Find Record Error - Transaction RECEIVE_METHOD Record Error & Record Error - Transaction TYPE Record Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit17']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each approved transaction, verify if the recorded transaction RECEIVE_METHOD & recorded transaction TYPE match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task18': {
        'data': paths['df_audit18'],
        'task_type': 'Auditing',
        'task_number': 18,
        'task_name': 'Find Record Error - Transaction PAYMENT/RECEIPT_STATUS Record Error & Record Error - Transaction QUANTITY Record Error & Calculation Error - Transaction PROFIT Calculation Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit18']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each submitted transaction, verify if the recorded transaction PAYMENT/RECEIPT_STATUS & recorded transaction QUANTITY & recorded transaction PROFIT Calculation match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task19': {
        'data': paths['df_audit19'],
        'task_type': 'Auditing',
        'task_number': 19,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit19']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each approved transaction, verify if the recorded transaction TYPE & recorded transaction Date match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task20': {
        'data': paths['df_audit20'],
        'task_type': 'Auditing',
        'task_number': 20,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & PRICE ANOMALY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit20']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each submitted transaction, verify if the recorded transaction TYPE MISCLASSIFICATION & recorded transaction PRICE  match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task21': {
        'data': paths['df_audit21'],
        'task_type': 'Auditing',
        'task_number': 21,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit21']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each approved transaction, verify if the recorded transaction TYPE MISCLASSIFICATION & recorded transaction AMOUNT DISCREPANCY match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task22': {
        'data': paths['df_audit22'],
        'task_type': 'Auditing',
        'task_number': 22,
        'task_name': 'Find Error - RECORDING DELAY Error & PRICE ANOMALY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit22']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction date and recorded unit price match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task23': {
        'data': paths['df_audit23'],
        'task_type': 'Auditing',
        'task_number': 23,
        'task_name': 'Find Error - RECORDING DELAY Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit23']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction date and recorded amount match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task24': {
        'data': paths['df_audit24'],
        'task_type': 'Auditing',
        'task_number': 24,
        'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit24']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded unit price and recorded amount match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task25': {
        'data': paths['df_audit25'],
        'task_type': 'Auditing',
        'task_number': 25,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error & PRICE ANOMALY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit25']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction type, recorded transaction date, and recorded unit price match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task26': {
        'data': paths['df_audit26'],
        'task_type': 'Auditing',
        'task_number': 26,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & RECORDING DELAY Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit26']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction type, recorded transaction date, and recorded amount match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task27': {
        'data': paths['df_audit27'],
        'task_type': 'Auditing',
        'task_number': 27,
        'task_name': 'Find Error - TYPE MISCLASSIFICATION Error & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit27']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction type, recorded unit price, and recorded amount match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task28': {
        'data': paths['df_audit28'],
        'task_type': 'Auditing',
        'task_number': 28,
        'task_name': 'Find Error - RECORDING DELAY Error & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit28']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded transaction date, recorded unit price, and recorded amount match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task29': {
        'data': paths['df_audit29'],
        'task_type': 'Auditing',
        'task_number': 29,
        'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit29']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded tax amount, recorded unit price, recorded amount, and recorded transaction date match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task30': {
        'data': paths['df_audit30'],
        'task_type': 'Auditing',
        'task_number': 30,
        'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & TYPE MISCLASSIFICATION Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit30']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded tax amount, recorded unit price, recorded amount, and recorded transaction type match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task31': {
        'data': paths['df_audit31'],
        'task_type': 'Auditing',
        'task_number': 31,
        'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & QUANTITY MISMATCH Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit31']),
        'task_difficulty': 'Medium',
        'task_description': 'For each transaction, check if the recorded transaction TAX & recorded transaction PRICE ANOMALY & recorded transaction AMOUNT DISCREPANCY & recorded transaction QUANTITY MISMATCH match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',

        'data_source': 'recorded transaction data',
        'seed': seed,
    },
    'task32': {
        'data': paths['df_audit32'],
        'task_type': 'Auditing',
        'task_number': 32,
        'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & QUANTITY MISMATCH Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit32']),
        'task_difficulty': 'Medium',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded unit price, recorded amount, recorded transaction date, and recorded quantity match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task33': {
        'data': paths['df_audit33'],
        'task_type': 'Auditing',
        'task_number': 33,
        'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit33']),
        'task_difficulty': 'Hard',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded tax amount, recorded unit price, recorded amount, recorded transaction date, and recorded transaction type match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task34': {
        'data': paths['df_audit34'],
        'task_type': 'Auditing',
        'task_number': 34,
        'task_name': 'Find Error - TAX ERROR & PRICE ANOMALY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error & QUANTITY MISMATCH Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit34']),
        'task_difficulty': 'Hard',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded tax amount, recorded unit price, recorded transaction date, recorded transaction type, and recorded quantity match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
        'seed': seed,
    },
    'task35': {
        'data': paths['df_audit35'],
        'task_type': 'Auditing',
        'task_number': 35,
        'task_name': 'Find Error - PRICE ANOMALY Error & AMOUNT DISCREPANCY Error & RECORDING DELAY Error & TYPE MISCLASSIFICATION Error & QUANTITY MISMATCH Error',
        'task_answer': convert_to_single_dict(risk_issues_dict['df_audit35']),
        'task_difficulty': 'Hard',
        'data_source': 'recorded transaction data',
        'task_description': 'For each transaction record, check if the recorded unit price, recorded amount, recorded transaction date, recorded transaction type, and recorded quantity match the other recorded transaction data. If inconsistent, output the transaction ID, the incorrect details, and the correct details.',
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
                if isinstance(v, str):  
                    formatted_values[k] = v
                else: 
                    formatted_values[k] = "{:.2f}".format(float(v))
            task_value['task_answer'] = formatted_values

    for task_key, task_value in result_dict.items():
        print(f"{task_key}: {task_value['task_answer']}" if task_value['task_answer'] is not None else f"{task_key}: None")
    
    with open(json_save_path, 'w', encoding='utf-8') as json_file:
        json.dump(result_dict, json_file, ensure_ascii=False, indent=4)