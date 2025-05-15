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

A financial data simulator for generating synthetic business data and financial statements.

### 📁 Project Structure

```python
simulator/
    ├── business_logic.py    # Core business operations and financial rules
    ├── data_generate.py     # Data generation and transaction simulation
    └── main.py             # Entry point and main program logic




