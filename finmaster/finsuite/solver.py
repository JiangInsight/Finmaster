import asyncio
import json
import os
import re
from litellm import batch_completion
from openai import AsyncOpenAI
from huggingface_hub import snapshot_download

from finsuite import MODELS
from finsuite.prompt import finmaster_template, example_and_solution, task_descriptions


def generate_prompt(args, problem_data, example_data, task_descriptions,solution_template):
    prompt = finmaster_template.replace(
    "<task_name>", args.task_name
).replace(
    "<task_description>", task_descriptions[args.task_name]
).replace(
    "<solution_template>", solution_template
)


    demos = example_and_solution.replace(
        "<example_problem>", "{}".format(str(example_data["data"]))
    ).replace("<example_solution>", str(example_data["task_answer"]))
    
    
    # print(demos)
    prompt = prompt.replace("<in_context_examples>", demos)
    prompt = prompt.replace("<task_to_solve>", str(problem_data["data"]))

    return prompt


def extract_solution_from_response(response):
    # find the json code
    match = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)
    if match:
        json_str = match[-1]
        try:
            # remove the single line comment
            json_str = re.sub(r"//.*$", "", json_str, flags=re.MULTILINE)
            # remove the multiple line comment
            json_str = re.sub(r"/\*[\s\S]*?\*/", "", json_str)
            data = json.loads(json_str)
            answer = data["solution"]
            return answer, None
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            # return None
            return None, f"Error parsing JSON or answer field: {e}"
    else:
        print("No JSON found in the text.")
        # return None
        return None, "JSON Error: No JSON found in the text."

class FinSuite:
    def __init__(self, problem_name, model_name, seed):
        if model_name in MODELS["online"].keys():
            self.is_online = True
        else:
            raise NotImplementedError

        self.model_name = model_name
        self.problem_name = problem_name

        self.local_llm = None
        self.sampling_params = None

        self.client = None

        if self.is_online and model_name.startswith("deepseek"):
            self.client = AsyncOpenAI(
                api_key=os.environ.get("ARK_API_KEY"),
                base_url="https://ark.cn-beijing.volces.com/api/v3",
            )
        if self.is_online and model_name.startswith("maas"):
            self.client = AsyncOpenAI(
                api_key=os.environ.get("MAAS_API_KEY"),
                base_url="https://genaiapi.cloudsway.net/v1/ai/RpGtTVMGiAYxmInr",
            )

    async def async_evaluate_llm(self, contents):
        assert self.client is not None

        async def call_gpt(prompt):
            response = await self.client.chat.completions.create(
                model=MODELS["online"][self.model_name],
                messages=[{"role": "user", "content": prompt}],
            )
            return response

        return await asyncio.gather(*[call_gpt(content) for content in contents])

    def get_batch_outputs_from_api(self, contents):
        try:
            print("Starting the batch calling of LLM")
            messages = [[{"role": "user", "content": content}] for content in contents]
            if self.is_online and (
                    self.model_name.startswith("deepseek")
                    or self.model_name.startswith("maas")
            ):
                responses = asyncio.run(self.async_evaluate_llm(contents))
            else:
                responses = batch_completion(
                    messages=messages, model=MODELS["online"][self.model_name]
                )
            print("End of calling LLM")
            # outputs = []
            # for idx, response in enumerate(responses):
            #     token_numbers = {
            #         "prompt": response.usage.prompt_tokens,
            #         "completion": response.usage.completion_tokens,
            #     }
            #     prediction = response.choices[0].message.content
            #     predicted_solution, json_error_message = extract_solution_from_response(
            #         prediction
            #     )
            #
            #     output = {
            #         "response": prediction,
            #         "solution": predicted_solution,
            #         "tokens": token_numbers,
            #         "error_msg": {"llm": None, "json": json_error_message},
            #     }
                # print(result)
                # outputs.append(output)
            return responses
        except Exception as e:
            # return None
            outputs = [
                {
                    "solution": None,
                    "error_msg": {"llm": f"LLM error: {e}", "json": None},
                }
                for _ in range(len(contents))
            ]

            return outputs



