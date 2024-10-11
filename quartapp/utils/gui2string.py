from collections import deque
from typing import Dict, Any


class GUI2String(object):

    VERSION_1 = 'version_1'
    VERSION_2 = 'version_2'
    VERSION_3 = 'version_3'
    VERSION_4 = 'version_4'
    VERSION_5 = 'version_5'

    def __init__(self, version: str = VERSION_5):
        self.version = version

    def gui2string(self, prototype: Dict[str, Any], idx: bool = False, options: bool = False) -> str:
        if self.version == GUI2String.VERSION_1:
            return self.gui2string_v1(prototype=prototype, idx=idx, options=options)
        if self.version == GUI2String.VERSION_2:
            return self.gui2string_v2(prototype=prototype, idx=idx, options=options)
        if self.version == GUI2String.VERSION_3:
            return self.gui2string_v3(prototype=prototype, idx=idx, options=options)
        if self.version == GUI2String.VERSION_4:
            return self.gui2string_v4(prototype=prototype, idx=idx, options=options)
        if self.version == GUI2String.VERSION_5:
            return self.gui2string_v5(prototype=prototype, idx=idx)

    @staticmethod
    def gui2string_v1(prototype: Dict[str, Any], idx: bool = False, options: bool = False) -> str:
        if not prototype:
            return ""
        prototype_str = ""
        for component in prototype['ui_comps']:
            queue = deque()
            queue.append((component, 0))
            while queue:
                component, curr_level = queue.popleft()
                prototype_str += '\n '
                for i in range(curr_level):
                    prototype_str += '\t'
                prototype_str += '- ' + component['group'] + ' (' + component['type'] + ")"
                cp_attributes = component['attributes']
                # If attributes are complex components, append them to the queue for rendering
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, str):
                        if attr_value:
                            prototype_str += '|"' + attr_value + '"'
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append((list_item, curr_level + 1))
                    if isinstance(attr_value, dict):
                        queue.append((attr_value, curr_level + 1))
                if options:
                    cp_options = component['options']
                    for option_key, option_value in cp_options.items():
                        prototype_str += '|' + option_key + ':' + option_value
                if idx and component.get('idx'): prototype_str += ' (id=' + str(component['idx']) + ')'
        return prototype_str

    @staticmethod
    def gui2string_v2(prototype: Dict[str, Any], idx=True, options=True, sort=True) -> str:
        if not prototype:
            return ""
        prototype_str = ""
        components = prototype['ui_comps']
        for comp in components:
            try:
                comp['generalAttributes']['yPos']
            except:
                print(comp)
        for comp in components:
            if not comp['generalAttributes'].get('xPos'):
                comp['generalAttributes']['xPos'] = 1000
            if not comp['generalAttributes'].get('yPos'):
                comp['generalAttributes']['yPos'] = 1000
        if sort:
            components = sorted(components,
                                key=lambda x: (x['generalAttributes']['yPos'], x['generalAttributes']['xPos']))
        for component in components:
            queue = deque()
            queue.append((component, 0))
            while queue:
                component, curr_level = queue.popleft()
                prototype_str += '\n '
                for i in range(curr_level):
                    prototype_str += '\t'
                prototype_str += '- ' + component['group'] + ' (' + component['type'] + ")"
                cp_attributes = component['attributes']
                # If attributes are complex components, append them to the queue for rendering
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, str):
                        if attr_value:
                            prototype_str += '|"' + attr_value + '"'
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append((list_item, curr_level + 1))
                    if isinstance(attr_value, dict):
                        queue.append((attr_value, curr_level + 1))
                if options and component.get('options'):
                    cp_options = component['options']
                    for option_key, option_value in cp_options.items():
                        prototype_str += '|' + option_key + ':' + option_value
                if idx and component.get('idx'): prototype_str += ' (id=' + str(component['idx']) + ')'
        return prototype_str

    @staticmethod
    def gui2string_v3(prototype: Dict[str, Any], idx=True, options=True, pos=True, sort=True) -> str:
        if not prototype:
            return ""
        prototype_str = ""
        components = prototype['ui_comps']
        for comp in components:
            try:
                comp['generalAttributes']['yPos']
            except:
        for comp in components:
            if not comp['generalAttributes'].get('xPos'):
                comp['generalAttributes']['xPos'] = 1000
            if not comp['generalAttributes'].get('yPos'):
                comp['generalAttributes']['yPos'] = 1000
        if sort:
            components = sorted(components,
                                key=lambda x: (x['generalAttributes']['yPos'], x['generalAttributes']['xPos']))
        for component in components:
            queue = deque()
            queue.append((component, 0))
            while queue:
                component, curr_level = queue.popleft()
                prototype_str += '\n '
                for i in range(curr_level):
                    prototype_str += '\t'
                prototype_str += '- ' + component['group'] + ' (' + component['type'] + ")"
                if pos:
                    prototype_str += '(x:' + str(component['generalAttributes']['xPos']) + '|y:' + \
                                     str(component['generalAttributes']['yPos']) + ')'
                cp_attributes = component['attributes']
                # If attributes are complex components, append them to the queue for rendering
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, str):
                        if attr_value:
                            prototype_str += '|"' + attr_value + '"'
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append((list_item, curr_level + 1))
                    if isinstance(attr_value, dict):
                        queue.append((attr_value, curr_level + 1))
                if options and component.get('options'):
                    cp_options = component['options']
                    for option_key, option_value in cp_options.items():
                        prototype_str += '|' + option_key + ':' + option_value
                if idx and component.get('idx'): prototype_str += ' (id=' + str(component['idx']) + ')'
        return prototype_str

    @staticmethod
    def gui2string_v4(prototype: Dict[str, Any], idx=True, options=True, pos=True, size=True, sort=True) -> str:
        if not prototype:
            return ""
        prototype_str = ""
        components = prototype['ui_comps']
        for comp in components:
            try:
                comp['generalAttributes']['yPos']
            except:
        for comp in components:
            if not comp['generalAttributes'].get('xPos'):
                comp['generalAttributes']['xPos'] = 1000
            if not comp['generalAttributes'].get('yPos'):
                comp['generalAttributes']['yPos'] = 1000
        if sort:
            components = sorted(components,
                                key=lambda x: (int(x['generalAttributes']['yPos']), int(x['generalAttributes']['xPos'])))
        for component in components:
            queue = deque()
            queue.append((component, 0))
            while queue:
                component, curr_level = queue.popleft()
                prototype_str += '\n '
                for i in range(curr_level):
                    prototype_str += '\t'
                prototype_str += '- ' + component['group'] + ' (' + component['type'] + ")"
                if pos:
                    prototype_str += '(x:' + str(component['generalAttributes']['xPos']) + '|y:' + \
                                     str(component['generalAttributes']['yPos']) + ')'
                if size:
                    prototype_str += '(width:' + str(component['generalAttributes']['width']) + '|height:' + \
                                     str(component['generalAttributes']['height']) + ')'
                cp_attributes = component['attributes']
                # If attributes are complex components, append them to the queue for rendering
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, str):
                        if attr_value:
                            prototype_str += '|"' + attr_value + '"'
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append((list_item, curr_level + 1))
                    if isinstance(attr_value, dict):
                        queue.append((attr_value, curr_level + 1))
                if options and component.get('options'):
                    cp_options = component['options']
                    for option_key, option_value in cp_options.items():
                        prototype_str += '|' + option_key + ':' + option_value
                if idx and component.get('idx'): prototype_str += ' (id=' + str(component['idx']) + ')'
        return prototype_str

    @staticmethod
    def gui2string_v5(prototype: Dict[str, Any], idx=True, pos=True, size=True, sort=True) -> str:
        if not prototype:
            return ""
        prototype_str = ""
        components = prototype['ui_comps']
        for comp in components:
            try:
                comp['generalAttributes']['yPos']
            except:
        for comp in components:
            if not comp['generalAttributes'].get('xPos'):
                comp['generalAttributes']['xPos'] = 1000
            if not comp['generalAttributes'].get('yPos'):
                comp['generalAttributes']['yPos'] = 1000
        if sort:
            components = sorted(components,
                                key=lambda x: (int(x['generalAttributes']['yPos']), int(x['generalAttributes']['xPos'])))
        for component in components:
            queue = deque()
            queue.append((component, 0))
            while queue:
                component, curr_level = queue.popleft()
                prototype_str += '\n '
                for i in range(curr_level):
                    prototype_str += '\t'
                prototype_str += '- ' + component['group'] + ' (' + component['type'] + ")"
                if pos:
                    prototype_str += ' (x:' + str(component['generalAttributes']['xPos']) + '|y:' + \
                                     str(component['generalAttributes']['yPos']) + ')'
                if size:
                    prototype_str += ' (width:' + str(component['generalAttributes']['width']) + '|height:' + \
                                     str(component['generalAttributes']['height']) + ') '
                cp_attributes = component['attributes']
                # If attributes are complex components, append them to the queue for rendering
                for attr_key, attr_value in cp_attributes.items():
                    if isinstance(attr_value, str):
                        if attr_value:
                            prototype_str += '|' + attr_key + ':"' + attr_value + '"'
                    if isinstance(attr_value, list):
                        for list_item in attr_value:
                            queue.append((list_item, curr_level + 1))
                    if isinstance(attr_value, dict):
                        queue.append((attr_value, curr_level + 1))
                if idx and component.get('idx'): prototype_str += ' (id=' + str(component['idx']) + ')'
        return prototype_str