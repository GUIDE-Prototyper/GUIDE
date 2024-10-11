import ast
import json
from collections import deque
from typing import Dict, Any, List, Set

from openai import AsyncOpenAI
from quartapp.generation.prompts import ZS_TEMPLATE_SINGLE_GENERATION_1, ZS_GENERATION_SINGLE_TEMPALTES, \
    PLACEHOLDER_GUI, ZS_TEMPLATE_FEATURE_GENERATION_1, PLACEHOLDER_GUI_TEXT, ZS_GENERATION_FEATURE_TEMPLATES
from quartapp.logger_conf import logger
from quartapp.openai_conf import base_model, base_temperature, base_n
from quartapp.utils.gui2string import GUI2String
from quartapp.utils.openai_utils import create_completion


class Generation(object):

    def __init__(self, openai_client: AsyncOpenAI, gui2string: GUI2String,
                 prompt_template: str = ZS_TEMPLATE_SINGLE_GENERATION_1,
                 model: str = base_model, temperature: float = base_temperature, n: int = base_n,
                 max_retries: int = 3):
        self.openai_client = openai_client
        self.gui2string = gui2string
        self.type = type
        self.prompt_template = prompt_template
        self.model = model
        self.temperature = temperature
        self.n = n
        self.max_retries = max_retries

    @staticmethod
    def generate_idx_mapping(prototype: Dict[str, Any]):
        idx_mapping = {}
        curr_idx = 1
        for ui_comp in prototype['ui_comps']:
            queue = deque()
            queue.append(ui_comp)
            while queue:
                # For each component generate the id and mapping
                curr_comp = queue.popleft()
                curr_comp['idx'] = str(curr_idx)
                idx_mapping[str(curr_idx)] = curr_comp['generalAttributes']['id']
                cp_attributes = curr_comp['attributes']
                curr_idx += 1
                # Search the attributes for complex components that also require ids
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append(list_item)
                    if isinstance(attr_value, dict):
                        queue.append(attr_value)
        # Create a new index for each component group which is unique for all comps and groups
        num_ui_comps = len(prototype['ui_comps'])
        for idx, ui_group in enumerate(prototype['ui_groups'], num_ui_comps+1):
            ui_group['idx'] = str(idx)
            idx_mapping[str(idx)] = ui_group['id']
        return idx_mapping

    async def generation_entire_gui(self, prototype: Dict[str, Any]) -> List[Dict[str, Any]]:
        idx_mapping_comps = Generation.generate_idx_mapping(prototype=prototype)
        gui_str = self.gui2string.gui2string(prototype=prototype, idx=True)
        if not self.prompt_template in ZS_GENERATION_SINGLE_TEMPALTES:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI, gui_str)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                parsed_content = json.loads(completion_content)
                is_correct = Generation.check_json_semantic_correctness(predictions=parsed_content,
                                                                        values=set(idx_mapping_comps.keys()))
                if is_correct:
                    for elem in parsed_content:
                        elem["comps"] = Generation.reverse_idx_mapping(values=elem["comps"],
                                                                       idx_mapping=idx_mapping_comps)
                    return parsed_content
                else:
                    logger.error('No correct format created : {} | Retry ({}/{})'.format(parsed_content,
                                                                                         str(current_retry + 1),
                                                                                         str(self.max_retries)))
                    current_retry += 1
                try:
                    pass
                except Exception as e:
                    logger.error('Exception occured while List decoding: {} | {} | | Retry ({}/{})'.format(
                        completion_content, e, str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
            else:
                logger.error('No completion created for prompt : {} | Retry ({}/{})'.format(filled_prompt,
                                                                                            str(current_retry + 1),
                                                                                            str(self.max_retries)))
                current_retry += 1
        return []

    async def feature_generation_1(self, text: str) -> List[Dict[str, Any]]:
        if not (self.prompt_template in ZS_GENERATION_FEATURE_TEMPLATES):
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text)
        logger.error(filled_prompt)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                    model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                try:
                    parsed_content = json.loads(completion_content)
                    if parsed_content:
                        return [{"number": str(idx), "name": elem['name'], "description": elem['description']}
                                for idx, elem in enumerate(parsed_content, 1)]
                except:
                    logger.error('No completion created for prompt | Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
            else:
                logger.error('No completion created for prompt| Retry ({}/{})'.format(
                    str(current_retry + 1), str(self.max_retries)))
                current_retry += 1

    @staticmethod
    def reverse_idx_mapping(values: List[str], idx_mapping: Dict[str, str]) -> List[str]:
        return [idx_mapping[value] for value in values]

    @staticmethod
    def check_json_semantic_correctness(predictions: List[Dict], values: Set[str]) -> bool:
        # Check if every element is constructed correctly
        for elem in predictions:
            if not elem.get("user_story") or not elem.get("comps") \
                    or not set(elem.get("comps")).issubset(values):
                return False
        return True