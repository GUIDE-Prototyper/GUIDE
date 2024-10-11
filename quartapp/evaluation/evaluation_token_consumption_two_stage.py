import json
import os

import pandas as pd

from quartapp.openai_conf import openai_client
from quartapp.recommendation.prompts import ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT
from quartapp.utils.gui2string import GUI2String
from quartapp.recommendation.recommendation import Recommendation
import asyncio


gui2string = GUI2String()
recommendation = Recommendation(openai_client=openai_client, gui2string=gui2string,
                                prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT)


data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/results/experiment_data.json"))
with open(data_path, 'r') as file:
    data = json.load(file)

loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
results = {}
for elem in data:
    result = loop.run_until_complete(recommendation.recommendation_no_prototype_text_two_stage_tokens(text=elem['prototype'], user_stories=elem['user_stories']))
    results.update(result)
print(results)

path_data = "../../data/"
path_results = path_data + 'results/'

with open(path_results + "two_stage_results.json", 'w') as file:
    json.dump(results, file, indent=4)

completion_tokens = []
prompt_tokens = []
total_tokens = []
fail_counter = 0
for id, elem in results.items():
    if elem.get('usage'):
        completion_tokens.append(elem['usage']["completion_tokens"])
        prompt_tokens.append(elem['usage']["prompt_tokens"])
        total_tokens.append(elem['usage']["total_tokens"])
    else:
        fail_counter += 1

print("Completion tokens: {}".format(completion_tokens))
print("Prompt tokens: {}".format(prompt_tokens))
print("Total tokens: {}".format(total_tokens))

data_completion_tokens = pd.Series(completion_tokens)
summary_completion_tokens = data_completion_tokens.describe()
print("--------------Completion tokens summary-----------------")
print(summary_completion_tokens)

print("--------------Prompt tokens summary-----------------")
data_prompt_tokens = pd.Series(prompt_tokens)
summary_prompt_tokens = data_prompt_tokens.describe()
print(summary_prompt_tokens)

print("--------------Total tokens summary-----------------")
data_total_tokens = pd.Series(total_tokens)
summary_total_tokens = data_total_tokens.describe()
print(summary_total_tokens)
print('Failed trials--------------')
print(fail_counter)