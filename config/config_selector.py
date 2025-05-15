# config_selector.py
import argparse
import os
from datetime import datetime
import importlib.util
import sys
import random

# Create argument parser
parser = argparse.ArgumentParser(description='Select configuration file and seed')
parser.add_argument('config', nargs='?', default=None,
                    choices=['config_chemistry', 'config_consulting', 
                            'config_hotel', 'config_sales', 
                            'config_big_manufactory'],
                    help='Configuration name')
# parser.add_argument('seed', nargs='?', type=int, default=None,
#                     help='Random seed value')

args = parser.parse_args()

# If no config specified in command line, use environment variable or default value
if args.config is None:
    CONFIG_NAME = os.environ.get('CONFIG_NAME', 'config_chemistry')
else:
    CONFIG_NAME = args.config

# Configuration mapping dictionary
CONFIG_MAPPING = {
    'config_chemistry': 'config_chemistry',
    'config_consulting': 'config_consulting',
    'config_hotel': 'config_hotel',
    'config_sales': 'config_sales',
    'config_big_manufactory': 'config_big_manufactory'
}

# Import corresponding configuration
module_name = CONFIG_MAPPING[CONFIG_NAME]
print("CONFIG_NAME:", CONFIG_NAME)
print("module_name:", module_name)
print("CONFIG_MAPPING:", CONFIG_MAPPING)

def dynamic_import(module_name):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the module
    module_path = os.path.join(current_dir, f"{module_name}.py")
    
    # Check if the file exists
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file {module_path} does not exist")
    
    # Dynamically import the module
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    # Import module attributes to the global namespace
    globals().update({k: v for k, v in module.__dict__.items() 
                      if not k.startswith('_')})

# Use dynamic import
module_name = CONFIG_MAPPING[CONFIG_NAME]
dynamic_import(module_name)

# Use command line seed if provided, otherwise use config seed
SEED = random.randint(1, 999)
# SEED = 210

# Create output directory path
BASE_DIR = './'
output_dir = os.path.join(BASE_DIR, f"{CONFIG_NAME}_{SEED}")

# Create the directory if it doesn't exist
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simulated_financial_data/' + str(CONFIG_NAME) +'/', f"{CONFIG_NAME}_{SEED}")

# Create directory
os.makedirs(output_dir, exist_ok=True)

print(f"Using config: {CONFIG_NAME}")
print(f"Using seed: {SEED}")
print(f"Output directory: {output_dir}")
