import os
import argparse
from finsuite.solver import FinSuite, extract_solution_from_response
import csv
import pandas as pd
from typing import Union, Dict
from finsuite.prompt import finmaster_template, example_and_solution, task_descriptions
from finsuite.solver import generate_prompt
def seed_everything(seed=42):
    import torch
    import numpy as np
    import random

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)
def csv_to_table(csv_input: Union[str, Dict[str, str]]) -> str:
    def process_csv(file_path: str, file_name: str = None) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = [cell.replace('|', '\\|') for cell in next(reader)]
            rows = [
                [cell.replace('|', '\\|') for cell in row]
                for row in reader
            ]

        table = []
        if file_name:
            table.append(f"### {file_name}")  # Add file name as a header if provided
        table.extend([
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |"
        ])

        for row in rows:
            table.append("| " + " | ".join(row) + " |")

        return "\n".join(table)

    if isinstance(csv_input, str):
        # Assume it's a file path
        csv_input = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + csv_input[1:]
        csv_input =  csv_input.replace('\\', '/')
        return process_csv(csv_input)
    elif isinstance(csv_input, dict):
        # Process each file in the dictionary
        tables = []
        for file_name, file_path in csv_input.items():
            file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + file_path[1:]
            file_path = file_path.replace('\\', '/')
            tables.append(process_csv(file_path, file_name))
        return "\n\n".join(tables)
    else:
        raise ValueError("Input must be a file path or a dictionary of file paths.")

def set_api_keys():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    with open(project_root+ "/finmaster/api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open(project_root+ "/finmaster/api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()
    with open(project_root+ "/finmaster/api_keys/claude_api_key.txt", "r") as file:
        claude_api_key = file.read().strip()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
    os.environ["ANTHROPIC_API_KEY"] = claude_api_key

    with open(project_root+ "/finmaster/api_keys/huoshan_api_key.txt", "r") as file:
        huoshan_api_key = file.read().strip()
    os.environ["ARK_API_KEY"] = huoshan_api_key



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=42,
        help="seed",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        default="gpt-4.1",
        help="name for LLM",
    )
    parser.add_argument(
        "--task_name",
        type=str,
        required=False,
        default="Calculate Total Assest",
        help="task name",
    )
    return parser.parse_args()

def ordered_common_keys(dict1, dict2):
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())
    
    common_keys = [key for key in keys1 if key in dict2]
    
    return common_keys
def flatten_dict_keys(d, parent_key='', sep='_'):
    keys = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            keys.update(flatten_dict_keys(v, new_key, sep=sep))
        else:
            keys[new_key] = '______'  
    return keys

def main(args):
    config_name = {
                  'config_consulting':[ '565']}
#    config_name = {
#                   
#                   'config_sales':['660', '706'],
#                   'config_big_manufactory':['827', '849', '908']}
    # config_name = {
    #                'config_sales':[ '660', '706'],
    #                'config_big_manufactory':['827','849','908']
    #                }
    json_file = ['data_consulting.json','data_auditing.json','data_accounting_statement_generation.json']
    # python your_script.py --config config_chemistry --seed 42
    config_example = 'example'
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_dir_main = os.path.join(project_root, 'strctured_data')
    example_path_main = os.path.join(json_dir_main, 'example\\config_example_676')
    for key_iterate, values_iterate in config_name.items():
        print(f"Key: {key_iterate}")
        for value in values_iterate:
            print(f"  Value: {value}")
            json_dir = os.path.join(json_dir_main,key_iterate)
            json_dir = os.path.join(json_dir, f'{key_iterate}_{value}')
            for json_iterate in json_file:
                data_path = os.path.join(json_dir, json_iterate)
                example_path = os.path.join(example_path_main , json_iterate)
                example_path = example_path.replace('\\', '/')
                data_path = data_path.replace('\\', '/')
                with open(example_path, 'r', encoding='utf-8') as file:
                    example_path = json.load(file)
                with open(data_path, 'r', encoding='utf-8') as file:
                    data_path = json.load(file)
                
                
                # common_keys = set(example_path.keys()) & set(data_path.keys())
#                /root/nips_code/response/gpt-4.1/config_chemistry/config_chemistry_240/data_accounting_read_statement.json/task1.json
                common_keys = ordered_common_keys(example_path, data_path)
                print((common_keys))
                # 迭代共同的 key
                for key in common_keys:

                    folder_path = os.path.join(project_root, 'response', "gpt-4.1",key_iterate, f'{key_iterate}_{value}', json_iterate)
                    os.makedirs(folder_path, exist_ok=True)
                    print('dddd',folder_path)
                    file_path = os.path.join(folder_path, f'{key}.json')
                    
                    if not os.path.exists(folder_path):
                        try:
                            os.makedirs(folder_path)
                            print("Directory created successfully.")
                        except OSError as e:
                            print(f"Error creating directory: {e}")
                    else:
                        print("Directory already exists.")

                    print(key)
                    example = example_path[key]
                    real = data_path[key]
                    # print(example,real)
                    print('sss')
                    print(example['data'])
                    # problem_data= pd.read_csv(example['data'])
                    example_data_path = example['data']
        
                    problem_data_path = real['data']
           
                    example_data= csv_to_table(example_data_path)
                    # example_data = pd.read_csv(real['data'])
                    problem_data = csv_to_table(problem_data_path)
                    
                    
                    example_data = {
                        "data":  example_data,
                        "task_answer": example['task_answer'],
                        "task_description": example['task_description']
                    }
                    problem_data = {
                        "data": problem_data,
                        "task_answer": real['task_answer'],
                        "task_description": real['task_description']
                    }
                    task_descriptions = {real['task_name']: real['task_description']}
                    solution_template = flatten_dict_keys(real['task_answer'])

                
                    
                    
                    args.task_name = real['task_name']
                    contents = generate_prompt(args, problem_data, example_data, task_descriptions,str(solution_template) ) 
                    print(contents)
                    
                    
                    solver = FinSuite(problem_name=args.task_name, model_name=args.model, seed=args.seed)
                    response = solver.get_batch_outputs_from_api([contents])
                    data = {"task": key, "response": [item.to_dict() for item in response]}

                    print("Response:", response)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(file_path)
                    
                    # if isinstance(response, list) and len(response) > 0:
                   
                    #     if 'choices' in response[0]:
                    #         prediction = response[0]['choices'][0]['message']['content']
                    #         print("Prediction:", prediction)
                    #     else:
                    #         print("Unexpected structure in response[0]:", response[0])
                    # else:
                    #     print("Response is empty or not a list.")

                    
                    # if isinstance(response, list) and len(response) > 0:
                    #     for item in response:
                    #         if hasattr(item, 'choices') and len(item.choices) > 0:
                    #             prediction = item.choices[0].message.content
                    #             print("Prediction:", prediction)
                    #         else:
                    #             print("Item does not have 'choices' attribute or is empty:", item)
                    # else:
                    #     print("Response is empty or not a list.")
                            
                    # prediction_str = json.dumps(prediction)

                    # numbers = re.findall(r'\d+\.\d+|\d+', prediction_str)
                    # answer = float(numbers[-1]) if numbers else None

                    # return answer
                    # Extract Solution
                    # predicted_solution, json_error_message = extract_solution_from_response(
                    #     prediction
                    # )
                    # print(predicted_solution)
import json
import re
if __name__ == "__main__":
    set_api_keys()

    args = get_parser()
    # seed_everything(args.seed)




    answer = main(args)
    