import ast
import copy
import os
import random
from collections import deque
from typing import List, Dict, Any, Set, Union
from openai import AsyncOpenAI
import json
from quartapp.utils.openai_utils import create_completion
from quartapp.openai_conf import base_model, base_temperature, base_n, openai_client
from quartapp.utils.gui2string import GUI2String
from quartapp.logger_conf import logger
from quartapp.recommendation.prompts import PLACEHOLDER_GUI, PLACEHOLDER_US, ZS_TEMPLATE_SINGLE_RECOMMENDATION_1, \
    ZS_RECOMMENDATION_SINGLE_TEMPLATE, PLACEHOLDER_COMPONENT_LIBRARY, COMPONENT_LIBRARY_1, \
    GENERAL_COMPONENT_ATTRIBUTES_1, PLACEHOLDER_GENERAL_ATTRIBUTES, ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE, \
    COMPONENT_LIBRARY_2, CARDINALITY_SINGLE, CARDINALITY_MULTIPLE, ICON_LIBRARY_1, PLACEHOLDER_ICON_LIBRARY, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT, ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE, \
    PLACEHOLDER_GUI_TEXT, ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT, COMPONENT_LIBRARY_3, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V2, ZS_TEMPLATE_SINGLE_USER_STORY_GENERATION_1, \
    ZS_TEMPLATE_STAGE_1_PROMPT, ZS_TEMPLATE_STAGE_2_PROMPT, ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1, \
    PLACEHOLDER_US_MULTIPLE, ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1, PLACEHOLDER_USER_STORY_NAME, \
    PLACEHOLDER_USER_STORY_DESCRIPTION, PLACEHOLDER_CURRENT_IMPLEMENTATION, PLACEHOLDER_NUM_VARIANTS, \
    ZS_TEMPLATE_FEATURE_LIST_STAGE_1_PROMPT, ZS_TEMPLATE_FEATURE_LIST_STAGE_2_PROMPT, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_1, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_2, PLACEHOLDER_SEL_COMPS_VARIANTS


class Recommendation(object):

    TYPE_SINGLE = 'type_single'
    TYPE_MULTIPLE = 'type_multiple'

    def __init__(self, openai_client: AsyncOpenAI, gui2string: GUI2String,
                 type: str = TYPE_SINGLE, prompt_template: str = ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE,
                 component_library_name: str = COMPONENT_LIBRARY_3, general_attributes: str = GENERAL_COMPONENT_ATTRIBUTES_1,
                 icon_library: str = ICON_LIBRARY_1, model: str = base_model, temperature: float = base_temperature,
                 n: int = base_n, max_retries: int = 3):
        self.openai_client = openai_client
        self.gui2string = gui2string
        self.type = type
        self.prompt_template = prompt_template
        print(general_attributes)
        self.general_attributes = json.loads(general_attributes)
        self.model = model
        self.temperature = temperature
        self.n = n
        self.max_retries = max_retries
        self.component_library = Recommendation.init_component_library(component_library_name)
        self.md_specification = Recommendation.init_md_specification()
        self.config_key_mapping = Recommendation.init_config_key_mapping()
        self.component_library_mapping = Recommendation.init_component_library_mapping_simple_full()
        self.icon_library = icon_library

    @staticmethod
    def init_component_library(component_library_name) -> str:
        if component_library_name == COMPONENT_LIBRARY_1:
            data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/component_libraries/component_library_1.txt'))
            print(data_path)
            with open(data_path, 'r') as file:
                data = file.read()
        if component_library_name == COMPONENT_LIBRARY_2:
            data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/component_libraries/component_library_2.txt'))
            print(data_path)
            with open(data_path, 'r') as file:
                data = file.read()
        if component_library_name == COMPONENT_LIBRARY_3:
            data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/component_libraries/component_library_3.txt'))
            print(data_path)
            with open(data_path, 'r') as file:
                data = file.read()
        return data

    @staticmethod
    def init_md_specification() -> Dict:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            "../../data/material_design/blueprint_mat 2.json"))
        with open(data_path, 'r') as file:
            data = json.load(file)
            return data

    @staticmethod
    def init_config_key_mapping() -> Dict:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            "../../data/config_key_mappings/config_key_mapping_3.json"))
        with open(data_path, 'r') as file:
            data = json.load(file)
            return data

    @staticmethod
    def init_component_library_mapping_simple_full() -> Dict:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            "../../data/component_libraries/component_library_mapping_simple_full.json"))
        with open(data_path, 'r') as file:
            data = json.load(file)
            return data

    async def recommendation_prototype(self, prototype:  Dict[str, Any], user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        gui_str = self.gui2string.gui2string(prototype=prototype)
        for user_story in user_stories:
            filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI, gui_str) \
                                                 .replace(PLACEHOLDER_US, user_story['text']) \
                                                 .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                                 .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                                 .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_and_check_correctness(completion_content)
                    if parsed_content:
                        predictions.append({"id": user_story['id'],
                                            "recommendation": parsed_content})
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                 str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return predictions

    async def recommendation_prototype_text(self, text: str, prototype:  Dict[str, Any], user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if not (self.prompt_template == ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT or
                self.prompt_template == ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V2):
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        gui_str = self.gui2string.gui2string(prototype=prototype)
        for user_story in user_stories:
            filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text) \
                                                 .replace(PLACEHOLDER_GUI, gui_str) \
                                                 .replace(PLACEHOLDER_US, user_story['text']) \
                                                 .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                                 .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                                 .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_and_check_correctness(completion_content)
                    if parsed_content:
                        predictions.append({"id": user_story['id'],
                                            "recommendation": parsed_content})
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                 str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return predictions

    async def recommendation_no_prototype(self, user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        for user_story in user_stories:
            filled_prompt = self.prompt_template.replace(PLACEHOLDER_US, user_story['text']) \
                                                 .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                                 .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                                 .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_and_check_correctness(completion_content)
                    if parsed_content:
                        predictions.append({"id": user_story['id'],
                                            "recommendation": parsed_content})
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                 str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return predictions

    async def recommendation_no_prototype_text(self, text: str, user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        for user_story in user_stories:
            filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text) \
                                                 .replace(PLACEHOLDER_US, user_story['text']) \
                                                 .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                                 .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                                 .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_and_check_correctness(completion_content)
                    if parsed_content:
                        predictions.append({"id": user_story['id'],
                                            "recommendation": parsed_content})
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                 str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return predictions

    async def recommendation_no_prototype_text_tokens(self, text: str, user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        for user_story in user_stories:
            filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text) \
                                                 .replace(PLACEHOLDER_US, user_story['text']) \
                                                 .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                                 .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                                 .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_and_check_correctness(completion_content)
                    if parsed_content:
                        predictions.append({"id": user_story['id'],
                                            "recommendation": parsed_content,
                                            "usage": completion.usage.to_dict()})
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                 str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return predictions

    async def recommendation_no_prototype_text_two_stage_tokens(self, text: str, user_stories: List[Dict[str, Any]]) -> \
            Dict[str, Any]:
        predictions = {}
        curr_stage_1 = None
        for user_story in user_stories:
            # First stage
            filled_prompt = ZS_TEMPLATE_STAGE_1_PROMPT.replace(PLACEHOLDER_GUI_TEXT, text) \
                                                      .replace(PLACEHOLDER_US, user_story['text'])
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                     model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    parsed_content = self.parse_list_and_check(completion_content)
                    if parsed_content:
                        curr_stage_1 = {"stage_1": parsed_content,
                                        "usage_1": completion.usage.to_dict()}
                        predictions[user_story['id']] = curr_stage_1
                        break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                        curr_stage_1 = None
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
                    curr_stage_1 = None
            if curr_stage_1:
                # Stage two
                curr_component_library = ''
                for sel_comp in curr_stage_1['stage_1']:
                    curr_component_library += str(self.component_library_mapping[sel_comp]) + '\n'
                filled_prompt = ZS_TEMPLATE_STAGE_2_PROMPT.replace(PLACEHOLDER_GUI_TEXT, text) \
                    .replace(PLACEHOLDER_US, user_story['text']) \
                    .replace(PLACEHOLDER_COMPONENT_LIBRARY, curr_component_library) \
                    .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                    .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
                logger.error(filled_prompt)
                current_retry = 0
                # Conduct multiple retries when an error occurs
                while current_retry < self.max_retries:
                    completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                         model=self.model, temp=self.temperature, n=self.n)
                    if completion:
                        completion_content = completion.choices[0].message.content
                        parsed_content = self.parse_and_check_correctness(completion_content)
                        if parsed_content:
                            predictions[user_story['id']].update({"stage_2": parsed_content,
                                                                  "usage_2": completion.usage.to_dict()})
                            curr_elem = predictions[user_story['id']]
                            predictions[user_story['id']].update({"stage_2": parsed_content,
                                                                  "usage": {"completion_tokens": (curr_elem['usage_1']["completion_tokens"] + curr_elem['usage_2']["completion_tokens"]),
                                                                            "prompt_tokens": (curr_elem['usage_1']["prompt_tokens"] + curr_elem['usage_2']["prompt_tokens"]),
                                                                            "total_tokens": (curr_elem['usage_1']["total_tokens"] + curr_elem['usage_2']["total_tokens"])}})
                            break
                        else:
                            logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                str(current_retry + 1), str(self.max_retries)))
                            current_retry += 1
                    else:
                        logger.error('No completion created for prompt| Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
        return predictions

    async def recommendation_using_feature_list_1(self, text: str, user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        user_stories_str = ""
        user_stories_sorted = sorted(user_stories, key=lambda x: int(x['number']), reverse=False)
        for us in user_stories_sorted:
            user_stories_str += us['number'] + '. "' + us['name'] + '": "' + us['description'] + '"\n'
        filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text) \
                                            .replace(PLACEHOLDER_US_MULTIPLE, user_stories_str) \
                                            .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                            .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                            .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
        logger.error(filled_prompt)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                parsed_content = self.parse_and_check_correctness_list(completion_content)
                if parsed_content:
                    for us in user_stories:
                        us['recommendation'] = parsed_content[us['number']]
                    return user_stories
                else:
                    logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
            else:
                logger.error('No completion created for prompt| Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                current_retry += 1
        return []

    async def recommendation_using_feature_list_two_stage(self, text: str, user_stories: List[Dict[str, Any]], include_tokens: bool=False) -> \
            List[Dict[str, Any]]:
        curr_stage_1 = None
        user_stories_str = ""
        user_stories_sorted = sorted(user_stories, key=lambda x: int(x['number']), reverse=False)
        for us in user_stories_sorted:
            user_stories_str += us['number'] + '. "' + us['name'] + '": "' + us['description'] + '"\n'
        # First stage
        filled_prompt = ZS_TEMPLATE_FEATURE_LIST_STAGE_1_PROMPT.replace(PLACEHOLDER_GUI_TEXT, text) \
                                                               .replace(PLACEHOLDER_US_MULTIPLE, user_stories_str)
        logger.error(filled_prompt)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                parsed_content = self.parse_json_list_and_check(completion_content, [us['number'] for us in user_stories])
                if parsed_content:
                    curr_stage_1 = {"stage_1": parsed_content,
                                    "usage_1": completion.usage.to_dict()}
                    break
                else:
                    logger.error('No completion created for prompt | Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
                    curr_stage_1 = None
            else:
                logger.error('No completion created for prompt| Retry ({}/{})'.format(
                    str(current_retry + 1), str(self.max_retries)))
                current_retry += 1
                curr_stage_1 = None
        if curr_stage_1:
            # Stage two
            curr_component_library = ''
            already_included_comps = set()
            for us_idx, sel_comps in curr_stage_1['stage_1'].items():
                for sel_comp in sel_comps:
                    if not sel_comp in already_included_comps:
                        curr_component_library += str(self.component_library_mapping[sel_comp]) + '\n'
                        already_included_comps.add(sel_comp)
            user_stories_str = ""
            user_stories_sorted = sorted(user_stories, key=lambda x: int(x['number']), reverse=False)
            for us in user_stories_sorted:
                user_stories_str += us['number'] + '. "' + us['name'] + '": "' + us['description'] + "(" + ",".join(curr_stage_1['stage_1'][us['number']]) + '")\n'
            filled_prompt = ZS_TEMPLATE_FEATURE_LIST_STAGE_2_PROMPT.replace(PLACEHOLDER_GUI_TEXT, text) \
                .replace(PLACEHOLDER_US_MULTIPLE, user_stories_str) \
                .replace(PLACEHOLDER_COMPONENT_LIBRARY, curr_component_library) \
                .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                        model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    # Set strict to False and therefore allow for setting default values in case of errorneous option values
                    parsed_content = self.parse_and_check_correctness_list(completion_content, strict=False)
                    if parsed_content:
                        for us in user_stories:
                            us['recommendation'] = parsed_content[us['number']]
                        return user_stories
                            #curr_stage_2 = {"stage_2": parsed_content, "usage_2": completion.usage.to_dict()}
                          #  predictions[user_story['id']].update({"stage_2": parsed_content,
                               #                                     "usage": {"completion_tokens": (curr_elem['usage_1']["completion_tokens"] + curr_elem['usage_2']["completion_tokens"]),
                               #                                             "prompt_tokens": (curr_elem['usage_1']["prompt_tokens"] + curr_elem['usage_2']["prompt_tokens"]),
                               #                                             "total_tokens": (curr_elem['usage_1']["total_tokens"] + curr_elem['usage_2']["total_tokens"])}})
                           # break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return []

    async def recommendation_feature_variants_1(self, num_variants: int, text: str, user_story: Dict[str, Any]) -> \
            List[Dict[str, Any]]:
        if self.prompt_template != ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        Recommendation.remove_key_attributes(user_story['recommendation'])
        filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI_TEXT, text) \
                                            .replace(PLACEHOLDER_USER_STORY_NAME, user_story['name']) \
                                            .replace(PLACEHOLDER_USER_STORY_DESCRIPTION, user_story['description']) \
                                            .replace(PLACEHOLDER_CURRENT_IMPLEMENTATION, str(user_story['recommendation'])) \
                                            .replace(PLACEHOLDER_NUM_VARIANTS, str(num_variants)) \
                                            .replace(PLACEHOLDER_COMPONENT_LIBRARY, self.component_library) \
                                            .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                                            .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
        logger.error(filled_prompt)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                parsed_content = self.parse_and_check_correctness_list(completion_content)
                if parsed_content:
                    return parsed_content
                else:
                    logger.error('No completion created for prompt | Retry ({}/{})'.format(
                                str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
            else:
                logger.error('No completion created for prompt| Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                current_retry += 1
        return []

    @staticmethod
    def create_simplfied_str_repr_recommendation(recommendation: List[Dict[str, Any]]) -> str:
        queue = deque()
        for comp in recommendation:
            queue.append(comp)
        comp_strs = []
        while queue:
            comp = queue.pop()
            comp_strs.append(comp["group"] + "|" + comp["type"])
            for attr_key, attr_val in comp['attributes'].items():
                if isinstance(attr_val, dict):
                    queue.append(attr_val)
                if isinstance(attr_val, list):
                    for elem in attr_val:
                        queue.append(elem)
        return str(list(set(comp_strs)))

    async def recommendation_feature_variants_two_stage(self, num_variants: int, text: str, user_story: Dict[str, Any], include_tokens: bool=False) -> \
            List[Dict[str, Any]]:
        curr_stage_1 = None
        # First stage
        us_curr_implementation = Recommendation.create_simplfied_str_repr_recommendation(user_story['recommendation'])
        filled_prompt = ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_1 \
                                    .replace(PLACEHOLDER_GUI_TEXT, text)\
                                    .replace(PLACEHOLDER_USER_STORY_NAME, user_story['name'])\
                                    .replace(PLACEHOLDER_USER_STORY_DESCRIPTION, user_story['description'])\
                                    .replace(PLACEHOLDER_CURRENT_IMPLEMENTATION, us_curr_implementation)\
                                    .replace(PLACEHOLDER_NUM_VARIANTS, str(num_variants))
        logger.error(filled_prompt)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                parsed_content = self.parse_json_list_and_check_2(completion_content)
                if parsed_content:
                    curr_stage_1 = {"stage_1": parsed_content,
                                    "usage_1": completion.usage.to_dict()}
                    break
                else:
                    logger.error('No completion created for prompt | Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
                    curr_stage_1 = None
            else:
                logger.error('No completion created for prompt| Retry ({}/{})'.format(
                    str(current_retry + 1), str(self.max_retries)))
                current_retry += 1
                curr_stage_1 = None
        if curr_stage_1:
            # Stage two
            curr_component_library = ''
            already_included_comps = set()
            for us_idx, sel_comps in curr_stage_1['stage_1'].items():
                for sel_comp in sel_comps:
                    if not sel_comp in already_included_comps:
                        curr_component_library += str(self.component_library_mapping[sel_comp]) + '\n'
                        already_included_comps.add(sel_comp)
            sel_comp_variants_str = ""
            for us_idx, sel_comps in curr_stage_1['stage_1'].items():
                sel_comp_variants_str += us_idx + ": " + str(sel_comps) + "\n"
            filled_prompt = ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_2 \
                .replace(PLACEHOLDER_GUI_TEXT, text) \
                .replace(PLACEHOLDER_USER_STORY_NAME, user_story['name']) \
                .replace(PLACEHOLDER_USER_STORY_DESCRIPTION, user_story['description']) \
                .replace(PLACEHOLDER_CURRENT_IMPLEMENTATION, us_curr_implementation) \
                .replace(PLACEHOLDER_SEL_COMPS_VARIANTS, sel_comp_variants_str) \
                .replace(PLACEHOLDER_NUM_VARIANTS, str(num_variants)) \
                .replace(PLACEHOLDER_COMPONENT_LIBRARY, curr_component_library) \
                .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, str(self.general_attributes)) \
                .replace(PLACEHOLDER_ICON_LIBRARY, str(self.icon_library))
            logger.error(filled_prompt)
            current_retry = 0
            # Conduct multiple retries when an error occurs
            while current_retry < self.max_retries:
                completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                        model=self.model, temp=self.temperature, n=self.n)
                if completion:
                    completion_content = completion.choices[0].message.content
                    # Set strict to False and therefore allow for setting default values in case of errorneous option values
                    parsed_content = self.parse_and_check_correctness_list(completion_content)
                    if parsed_content:
                        return parsed_content
                            #curr_stage_2 = {"stage_2": parsed_content, "usage_2": completion.usage.to_dict()}
                          #  predictions[user_story['id']].update({"stage_2": parsed_content,
                               #                                     "usage": {"completion_tokens": (curr_elem['usage_1']["completion_tokens"] + curr_elem['usage_2']["completion_tokens"]),
                               #                                             "prompt_tokens": (curr_elem['usage_1']["prompt_tokens"] + curr_elem['usage_2']["prompt_tokens"]),
                               #                                             "total_tokens": (curr_elem['usage_1']["total_tokens"] + curr_elem['usage_2']["total_tokens"])}})
                           # break
                    else:
                        logger.error('No completion created for prompt | Retry ({}/{})'.format(
                            str(current_retry + 1), str(self.max_retries)))
                        current_retry += 1
                else:
                    logger.error('No completion created for prompt| Retry ({}/{})'.format(
                        str(current_retry + 1), str(self.max_retries)))
                    current_retry += 1
        return []


    def parse_list_and_check(self, content: str) -> Union[List[str], None]:
        # Check if the result can at all be parsed to JSON
        try:
            parsed_content = ast.literal_eval(content)
            for elem in parsed_content:
                if elem not in self.component_library_mapping:
                    return None
            return parsed_content
        except:
            return None

    def parse_json_list_and_check(self, content: str, user_story_ids : List[str]) -> Dict[str, Any]:
        # Check if the result can at all be parsed to JSON
        try:
            parsed_content = json.loads(content)
            for key, compstr_list in parsed_content.items():
                for elem in compstr_list:
                    if elem not in self.component_library_mapping:
                        return {}
            if not (set(parsed_content.keys()) == set(user_story_ids)):
                return {}
            return parsed_content
        except:
            return {}

    def parse_json_list_and_check_2(self, content: str) -> Dict[str, Any]:
        # Check if the result can at all be parsed to JSON
        try:
            parsed_content = json.loads(content)
            for key, compstr_list in parsed_content.items():
                for elem in compstr_list:
                    if elem not in self.component_library_mapping:
                        return {}
            return parsed_content
        except:
            return {}

    async def recommendation_multiple(self, gui_str: str, user_stories: List[Dict[str, Any]]) -> \
            List[Dict[str, Any]]:
        if not self.prompt_template in ZS_RECOMMENDATION_SINGLE_TEMPLATE:
            raise ValueError('The selected template cannot be used with the '
                             'selected type [{}]'.format(self.type))
        predictions = []
        idx_mapping = {}
        user_stories_str = ""
        for idx, user_story in enumerate(user_stories, 1):
            idx_mapping[str(idx)] = user_story['id']
            user_stories_str += str(idx) + ". " + user_story['text'] + "\n"
        filled_prompt = self.prompt_template.replace(PLACEHOLDER_GUI, user_stories_str) \
                                            .replace(PLACEHOLDER_GUI, gui_str)
        current_retry = 0
        # Conduct multiple retries when an error occurs
        while current_retry < self.max_retries:
            completion = await create_completion(openai_client=self.openai_client, prompt=filled_prompt,
                                                 model=self.model, temp=self.temperature, n=self.n)
            if completion:
                completion_content = completion.choices[0].message.content
                try:
                    data_dict = json.loads(completion_content)
                    is_correct = await Recommendation.check_semantic_correctness(data_dict=data_dict,
                                                                            keys=set(idx_mapping.keys()),
                                                                            labels=ZS_RECOMMENDATION_SINGLE_TEMPLATE)
                    if is_correct:
                        return [{'id': idx_mapping[idx], 'impl': pred} for idx, pred in data_dict.items()]
                    else:
                        logger.error('No correct format created : {} | Retry ({}/{})'.format(data_dict,
                                str(current_retry+1), str(self.max_retries)))
                        current_retry += 1
                except json.JSONDecodeError as e:
                    logger.error('Exception occured while JSON decoding: {} | {} | | Retry ({}/{})'.format(
                            completion_content, e, str(current_retry+1), str(self.max_retries)))
                    current_retry += 1
            else:
                logger.error('No completion created for prompt | Retry ({}/{})'.format(
                        str(current_retry+1), str(self.max_retries)))
                current_retry += 1
        return predictions

    def parse_and_check_correctness_list(self, content: str, strict=True) -> Union[List[Dict], None]:
        # Check if the result can at all be parsed to JSON
        try:
            parsed_content = json.loads(content)
            parsed_components = []
            for us_idx, component_list in parsed_content.items():
                for component_specs in component_list:
                    result = self.check_semantic_correctness_add_key(component_specs, strict=strict)
                    if not result:
                        return None
            return parsed_content
        except Exception as e:
            message = "Exception occured while parsing and checking components: {}".format(e)
            logger.error(message)
            return None

    def parse_and_check_correctness(self, content: str) -> Union[List[Dict], None]:
        # Check if the result can at all be parsed to JSON
        try:
            parsed_content = json.loads(content)
            parsed_components = []
            for component, component_specs in parsed_content.items():
                result = self.check_semantic_correctness_add_key(component_specs)
                if result:
                    parsed_components.append(component_specs)
                else:
                    return None
            return parsed_components
        except Exception as e:
            message = "Exception occured while parsing and checking components: {}".format(e)
            logger.error(message)
            return None

    def check_semantic_correctness_add_key(self, component, strict=True):
        queue = deque()
        queue.append(component)
        while queue:
            logger.error(curr_component)
            logger.error(curr_component.keys())
            comp_mds = self.md_specification[curr_component['group']][curr_component['type']]
            # Check if component matches the specification
            is_correct_spec = self.check_component_specification(comp_mds, curr_component, strict=strict)
            if not is_correct_spec:
                return None
            # Match the specific configuration key of the created configuration with specification
            if comp_mds['options']:
                config_str = Recommendation.create_config_str(curr_component['group'], curr_component['type'],
                                               curr_component['options'], comp_mds['options'])
                key_mapping = self.config_key_mapping[config_str].strip()
            else:
                key_mapping = "-"
            curr_component['general_attributes']['key'] = key_mapping
            # Iterate all the attributes and check for sub components
            for attribute_name, attribute_value in curr_component['attributes'].items():
                # If it is a dict then it is a complex component reference that should also be verified
                if isinstance(attribute_value, dict):
                    queue.append(attribute_value)
                # If it is a list then it is a list of complex component references that also need to be verified
                if isinstance(attribute_value, list):
                    for list_component in attribute_value:
                        queue.append(list_component)
        return component

    def check_component_specification(self, component_specification, component, strict=True) -> bool:
        # Check correct options
        cps_options = component_specification['options']
        if cps_options and not "options" in component.keys():
            logger.error('No options in generated component')
            return False
        if cps_options:
            cp_options = component.get('options')
            # If options in spec and generated comp do not match it is a wrong spec
            if not Recommendation.check_key_sets(cps_options, cp_options):
                logger.error("Option key sets not identical")
                return False
            # If a set option is not part of the possible options it is a wrong spec
            for option_key, option_values in cps_options.items():
                if not (cp_options[option_key] in option_values):
                    logger.error("Option values not from specification")
                    if strict:
                        return False
                    else:
                        # In non-strict mode select a default value randomly
                        cp_options[option_key] = random.choice(option_values)
        cps_attributes = copy.deepcopy(component_specification['attributes'])
        del cps_attributes['Standalone']
        del cps_attributes['NumOptions']
        if not "attributes" in component.keys():
            logger.error('No attributes in generated component')
            return False
        cp_attributes = component.get('attributes')
        # If attribues in spec and generated comp do not match it is a wrong spec
        if not Recommendation.check_key_sets_included(cps_attributes, cp_attributes):
            return False
        # Check if all attribute value types correspond with the spec
        for attr_key, attr_value in cps_attributes.items():
            if attr_key in cp_attributes:
                if isinstance(attr_value, str):
                    if not isinstance(cp_attributes[attr_key], str):
                        logger.error("Attribute value not string")
                        return False
                if isinstance(attr_value, list):
                    if not (cp_attributes[attr_key] in attr_value):
                        logger.error("Attribute value not list")
                        return False
                if isinstance(attr_value, dict):
                    # If the complex component is only a single component
                    if attr_value['cardinality'] == CARDINALITY_SINGLE:
                        if not ((attr_value['Group'] == cp_attributes[attr_key]['group']) and
                                (not attr_value['Instance'] or attr_value['Instance'] == cp_attributes[attr_key]['type'])):
                            return False
                        # If the component is a list of complex components
                        elif attr_value['cardinality'] == CARDINALITY_MULTIPLE:
                            # Check semantic correctness for each component in the list
                            for list_component in cp_attributes[attr_key]:
                                if not ((attr_value['Group'] == list_component['group']) and
                                        (not attr_value['Instance'] or attr_value['Instance'] == list_component['type'])):
                                    logger.error("Attribute value not match dict with cardinality multiple")
                                    return False
        # If general attributes in spec and generated comp do not match it is a wrong spec
        if not "general_attributes" in component.keys():
            logger.error('No general_attributes in generated component')
            return False
        cp_general_attributes = component.get('general_attributes')
        if not Recommendation.check_key_sets(self.general_attributes, cp_general_attributes):
            return False
        return True

    @staticmethod
    def remove_key_attributes(json_obj):
        if isinstance(json_obj, dict):
            # Remove "key" from the dictionary if it exists
            if 'key' in json_obj:
                del json_obj['key']
            # Recursively call the function for each value in the dictionary
            for value in json_obj.values():
                Recommendation.remove_key_attributes(value)
        elif isinstance(json_obj, list):
            # Recursively call the function for each item in the list
            for item in json_obj:
                Recommendation.remove_key_attributes(item)

    @staticmethod
    def create_config_str(group_name, component_name, component_options, md_spec_options) -> str:
        config_str = group_name + '|' + component_name
        for option in md_spec_options.keys():
            config_str += '|' + option.strip() + ':' + component_options[option.strip()].strip()
        return config_str

    @staticmethod
    def is_int_parsable(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_key_sets(dict_1, dict_2) -> bool:
        return (set(dict_1.keys()) == set(dict_2.keys()))

    @staticmethod
    def check_key_sets_included(dict_1, dict_2) -> bool:
        return set(dict_2.keys()).issubset(set(dict_1.keys()))

    @staticmethod
    def create_comp_string_repr(comp_data: Dict, separator: str = ':') -> str:
        comp_str = comp_data['comp'] + separator
        for key, value in comp_data['options']:
            comp_str += value + separator
        return comp_str[:len(comp_str-1)]

    @staticmethod
    async def check_semantic_correctness(data_dict: Dict[str, str], keys: Set[str], labels: Set[str]) -> bool:
        predicted_keys = set(data_dict.keys())
        predicted_labels = set(data_dict.values())
        return predicted_keys == keys and predicted_labels == labels and \
               len(predicted_keys) == len(keys) and len(predicted_labels) == len(predicted_keys)