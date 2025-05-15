# FinMaster: A Holistic Benchmark for Mastering Full-Pipeline Financial Workflows with LLMs
<div align="center">
<img align="center" src="figure/finmaster.png" width="80%"/>
</div>

***
Existing benchmarks are limited by their reliance on static datasets, narrow task scope, and inability to capture the dynamic, multi-faceted nature of real-world financial workflows.
To address these issues, we present **FinMaster**, a holistic benchmark for mastering full-pipeline financial workflows with LLMs. 

Our work introduces three key components:

1. **FinSim**: a financial data simulator generating synthetic datasets that mirror real-world market dynamics;
2. **FinSuite**: a comprehensive task collection covering accounting, auditing, and consulting scenarios;
3. **FinEval**: a unified evaluation framework for systematic assessment of LLMs' financial capabilities.
   
To the best of our knowledge, **FinMaster** is the first benchmark that comprehensively covers full-pipeline financial workflows with challenging and realistic tasks.



## 🔄 FinSim

FinSim is a financial simulator with three main stages:

1. **Data Generation**
   - Configures company-specific settings
   - Simulates business operations (assets, purchase, sales)
   - Produces comprehensive financial records

2. **Transaction Processing**
   - Generates realistic transactions
   - Incorporates deliberate errors for auditing scenarios

3. **Financial Reporting**
   - Income Statement: revenue and expense aggregation
   - Balance Sheet: assets, liabilities, and equity
   - Cash Flow Statement: operating, investing, and financing activities

### 📁 Project Structure

```python
simulator/
    ├── business_logic.py    # Core business operations and financial rules
    ├── data_generate.py     # Data generation and transaction simulation
    └── main.py             # Entry point and main program logic
```


# 🎯 FinSuite

A financial task generation framework creating evaluation scenarios across accounting, auditing, and consulting domains.

## 🔨 Task Categories

### Financial Literacy Tasks
- Definition-matching queries on financial reports
- Progressive complexity levels for terminology, reasoning, and data processing

### Accounting Tasks
- **Tier 1**: Disclosure item generation (elementary & cross-transaction operations)
- **Tier 2**: Financial statement synthesis with standard compliance

### Auditing Tasks
- Invoice-format transaction data generation
- Systematic error embedding (12 types, 3 categories)
- Single & multi-error analysis levels

### Consulting Tasks
18 key indicators across profitability, operational efficiency, liquidity, solvency, and cash flow quality

```python
task_data_script/
├── data_accounting_read_statement.py     # Statement reading and parsing
├── data_accounting_statement_generation.py    # Financial statement generation
├── data_auditing.py                     # Audit task simulation
└── data_consulting.py                   # Financial consulting scenarios
```

# 📋 Prompt Template Structure

## Overview
The prompt template provides a standardized framework for guiding LLMs in financial task solving, ensuring consistency across accounting, auditing, and consulting modules.

## ⚙️ Core Components

### 1. Task Description
- **Name**: Task identifier
- **Description**: Task objectives
- **Module**: Accounting/Auditing/Consulting

### 2. Examples
- **Input**: Sample data, parameters
- **Output**: Solution format, demonstration
- **Context**: Explanation and reasoning

### 3. Problem Definition
- **Task**: Problem statement
- **Input**: Required data
- **Output**: Expected deliverables

### 4. Output Format
- **JSON Structure**: Solution, validation
- **Required Fields**: Response format
- **Rules**: Format guidelines

## Features
- Generic cross-module framework
- No task-specific knowledge
- Standardized formats
- Clear validation rules












