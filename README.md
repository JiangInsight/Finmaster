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



## 🔄 FinSim Workflow

### 1. Initialization - 
- Configure simulator settings for specific company types 
- Set up business parameters and operational rules

### 2. Business Simulation
- Simulates core financial activities:
  - Assets Management
  - Purchase Management
  - Sales Management
- Generates comprehensive financial records:
  - Asset Data
  - Operational Data
  - Financial Data

### 3. Transaction Generation
- Creates both correct and incorrect transactions
- Incorporates realistic errors for auditing scenarios
- Simulates common business mistakes

### 4. Financial Statement Production
- **Income Statement**: Aggregates revenue and expense transactions
- **Balance Sheet**: Combines asset positions with liability and equity data
- **Cash Flow Statement**: Synthesizes cash transactions into:
  - Operating Activities
  - Investing Activities
  - Financing Activities

The simulation process runs iteratively to ensure comprehensive financial outputs and realistic market dynamics.

