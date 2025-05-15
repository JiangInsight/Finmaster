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


