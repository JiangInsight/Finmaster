finmaster_template = """
# <task_name> Task Description:
<task_description>

# Examples:
<in_context_examples>
# Problem to Solve: 
{"problem": <task_to_solve>}

# Instruction:
Now please solve the above task.  Reason step by step and present your answer in the "solution" field in the following json format:
```json
{"solution": <solution_template> }
```
"""

example_and_solution = """{"problem": <example_problem>}
{"solution": <example_solution>}
"""

task_descriptions = {
    "Calculate Total Assest": """Analyze the provided data and calculate total assets from the balance sheet. """,
}
