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



## 🔄 FinSim Overview

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

A financial task generation framework that creates diverse evaluation scenarios across accounting, auditing, and consulting domains.

## 🔍 Core Task Categories

### 1. Financial Literacy Tasks
Evaluates fundamental financial knowledge using simulator-generated reports:
- Definition-matching query methodology
- Progressive complexity evaluation
- Focus areas:
  - Terminology comprehension
  - Logical reasoning
  - Complex data processing

### 2. Accounting Tasks
Financial statement generation through a two-tiered framework:
- **Tier 1**: Disclosure item generation
  - Elementary computational operations
  - Cross-transaction analysis
- **Tier 2**: Financial statement synthesis
  - Standardized value generation
  - Multi-source data integration
  - Accounting standard compliance

### 3. Auditing Tasks
Transaction record verification with dual components:
- **Component 1**: Invoice-format transaction data generation
- **Component 2**: Systematic error embedding
  - 12 distinct error types in 3 categories
  - Two analysis levels:
    - Single-error analysis
    - Multi-error analysis

### 4. Consulting Tasks
Financial performance analysis framework:
- 18 key indicators across 5 dimensions:
  - Profitability
  - Operational efficiency
  - Liquidity
  - Solvency
  - Cash flow quality

