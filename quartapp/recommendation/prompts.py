PLACEHOLDER_US = '{placeholder_us}'
PLACEHOLDER_US_MULTIPLE = '{placeholder_us_multiple}'
PLACEHOLDER_GUI = '{placeholder_gui}'
PLACEHOLDER_GUI_TEXT = '{placeholder_gui_text}'
PLACEHOLDER_COMPONENT_LIBRARY = '{placeholder_component_library}'
PLACEHOLDER_GENERAL_ATTRIBUTES = '{placeholder_general_attributes}'
PLACEHOLDER_ICON_LIBRARY = '{placeholder_icon_library}'
PLACEHOLDER_USER_STORY_NAME = '{placeholder_user_story_name}'
PLACEHOLDER_USER_STORY_DESCRIPTION = '{placeholder_user_story_description}'
PLACEHOLDER_CURRENT_IMPLEMENTATION = '{placeholder_current_implementation}'
PLACEHOLDER_NUM_VARIANTS = '{placeholder_num_variants}'
PLACEHOLDER_SEL_COMPS_VARIANTS = '{placeholder_selected_comps_variants}'

ZS_TEMPLATE_SINGLE_RECOMMENDATION_1 = '''You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual representation of a graphical user interface. The GUI is organized as a two-level bullet point list, the outer points representing layouting groups and the inner points the user interface features contained in that layouting group. Each feature is represented in the following abstract pattern: 'text' (ui component type) (semantic description of ui component), the 'text' being the visual text of the component. In addition, you are given a list of UI components that can use to implement the user story. Each UI component
comes as a JSON with a name followed by several attributes and their options. Moreover, there are general attributes (e.g., text, width, heigth etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:
Component Library Example: {"comp": "Button", "style": [”Tonal”, “Elevated”, “Text”, “Outlined”, “Filled”], “state”: [”Disabled”, “Focused”, “Hovered”, “Pressed”, “Enabled”], “show_icon”: [”True”, “False”]}
Component Instantiation Example: {"comp": "Button", "options":{"style": "Filled", "state": "Enabled", "show_icon": "True"}, "x": 200, "y":100, "width": 150, "height":20, "text": "Order now", "name": "order_now_button"}
Your task implement the feature of the user story in using the given components and create accurate instantiations. Do not provide any explanation. Output each component instantiation by starting a new line and produce correct JSON for each instantiation. 
\n\ncomponent library: \n{placeholder_component_library} \n\ngeneral attributes: \n{placeholder_general_attributes}\n\nuser story: '{placeholder_us}' \n\ngraphical user interface description: {placeholder_gui} \n\nuser story implementation:
'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual representation of a graphical user interface, for which the user story should be implemented. The GUI is organized as a multi-level bullet point list, the outer points representing layouting groups or components and the inner points the user interface features contained in that layouting group or component, sometimes the grouping information may not be available. Each feature is represented in the following abstract pattern: - component-group (component-type) (position) (size) |attribute name:"attribute value"|, and one or more attributes can occur. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. Only provide the implementation of the user story, not the entire GUI. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. For this, also use the size and position information contained in the given gui representation.

GUI representation: {placeholder_gui}

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

User story: "{placeholder_us}"

'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual representation of a graphical user interface (and a short textual description), for which the user story should be implemented. The GUI is organized as a multi-level bullet point list, the outer points representing layouting groups or components and the inner points the user interface features contained in that layouting group or component, sometimes the grouping information may not be available. Each feature is represented in the following abstract pattern: - component-group (component-type) (position) (size) |attribute name:"attribute value"|, and one or more attributes can occur. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. Only provide the implementation of the user story, not the entire GUI. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. For this, also use the size and position information contained in the given gui representation.

GUI text description: "{placeholder_gui_text}"

GUI representation: {placeholder_gui}

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

User story: "{placeholder_us}"

'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V2 = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual representation of a graphical user interface (and a short textual description), for which the user story should be implemented. The GUI is organized as a multi-level bullet point list, the outer points representing layouting groups or components and the inner points the user interface features contained in that layouting group or component, sometimes the grouping information may not be available. Each feature is represented in the following abstract pattern: - component-group (component-type) (position) (size) |attribute name:"attribute value"|, and one or more attributes can occur. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. Only provide the implementation of the user story, not the entire GUI. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. For this, also use the size and position information contained in the given gui representation. Also make sure to add a padding of 10 points on each side.

GUI text description: "{placeholder_gui_text}"

GUI representation: {placeholder_gui}

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

User story: "{placeholder_us}"

'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V3 = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual representation of a graphical user interface (and a short textual description), for which the user story should be implemented. The GUI is organized as a multi-level bullet point list, the outer points representing layouting groups or components and the inner points the user interface features contained in that layouting group or component, sometimes the grouping information may not be available. Each feature is represented in the following abstract pattern: - component-group (component-type) (position) (size) |attribute name:"attribute value"|, and one or more attributes can occur. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. Provide the implementation of the user story. If a AppBar (Top) is not yet in the gui representation, then implement a top app bar as well. For the top app bar, include a "yPos" offset of 70, but also include all other general_attributes. If the AppBar (Bottom) is not yet in the gui representation, then implement a bottom app bar as well. Do not implement the entire gui representation, focus on the user story and when not yet available, the app bars. The width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. For this, also use the size and position information contained in the given gui representation. Also make sure to add a padding of 10 points on each side. 

GUI text description: "{placeholder_gui_text}"

GUI representation: {placeholder_gui}

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

User story: "{placeholder_us}"

'''



ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

User story: "{placeholder_us}"

'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT = '''
You are given a user story in the context of a graphical user interface (which is described also briefly in text), this user story is not yet implemented. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include "general_attributes" for each component.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Make sure to consider the GUI context given by the textual description of the GUI while implementing the GUI feature, but focus on implementing the specifc functionality requested in the user story. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components),  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. Remember that you HAVE TO include "general_attributes" for each component.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

GUI text description: "{placeholder_gui_text}"

User story: "{placeholder_us}"

'''


ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1 = '''
You are given a list of user stories in the context of a graphical user interface description. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user stories. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component and their sub components. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created. Make sure to always include general_attributes. Make sure that all of these sub components always have "general_attributes". Make sure that you always select one value for each key of the "options". Only use components from the component library, do NOT invent new components.

Your task is to implement the features for each user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each user story, create a new key (being the number of the user story) with the corresponding implementation as the value as a correct JSON (e.g., {"1": [{"group": "Button" etc.}, {"group": "Chips" etc.}]). For each user story, create a list containing the main components (i.e. not the sub components) to fulfill the user story. Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. Please always set the font size to 12. Please also leave some small margins (at least 10 pixels vertically) between the components. There is no list component, so make sure to implement list in a different way using the provided components.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

GUI description: "{placeholder_gui_text}"

User stories: 
{placeholder_us_multiple}

output:
'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1 = '''
You are given a name and description of a user story in the context of a graphical user interface description. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component and their sub components. Here is an example of a component followed by an example how it should be created later:

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}}

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below. For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50",  "fontSize": "4",  "textAlign": "center",  "textVerticalAlign": "middle",  "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes. Make sure that all of these sub components always have "general_attributes".

In addition to the given information, you are also given a first implementation of the user story. Your task is to implement {placeholder_num_variants} more variants for the user story that are all different by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for new implementation of the user story,  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"variant-1": [{"group": "Button" etc.}, {"group": "Chips" etc.}]). For the user story, create a list containing the main components (i.e. not the sub components) to fulfill the user story. Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

GUI description: "{placeholder_gui_text}"
User story name: "{placeholder_user_story_name}"
User story description: "{placeholder_user_story_description}"
Current implementation:
{placeholder_current_implementation}

output:
'''

ZS_TEMPLATE_STAGE_1_PROMPT = '''You are given a user story in the context of a graphical user interface (which is described 
also briefly in text), this user story is not yet implemented. In addition, you are given a list of UI components (i.e. 
component library) that you can use to implement the user story. Each new line represents a new UI component, which 
comes in the format "group|type|standalone{group:type|...}, where group refers to the general component group, type 
to the specific component type and standalone is a Boolean representing whether it can be used as a standalone component,
and none or multiple sub components that the component uses. If the type is set to None in the sub components, any of the
types from the group can be selected. In the case of when the type is set to None, always make sure to select a matching 
component type from the specified group and add it to the list. Your task is to select all the components relevant to 
implement the user story. If the component has sub components, also explicitly select them as components, and potentially 
their sub components and so on. For example, when selecting a Dialog|List, then a Button|SimpleButton has to be included,
but also e.g. a Lists|List0 and also their sub components in this case e.g. the ListItem|Item0. Make sure to consider 
the GUI context given by the textual description of the GUI while implementing the GUI feature, but focus on implementing
the specific functionality requested in the user story. As your result, give a list of "group|type" strings representing 
all selected components. Do not provide any explanation and do not provide any python markup, directly output a python list.

Components:

AppBar|Bottom|True{Button:FAB}
AppBar|Top|True{}
Button|SimpleButton|True{}
Button|ExtFAB|True{}
Button|FAB|True{}
Button|Icon|True{}
Button|IconTogg|True{}
Button|LargeFAB|True{}
Button|SegButton|True{SegButtonBlocks:Start|SegButtonBlocks:None}
Button|SmallFAB|True{}
SegButtonBlocks|End|False{}
SegButtonBlocks|Mid|False{}
SegButtonBlocks|Start|False{}
Badges|Badges|True{}
Cards|Horizontal|True{}
Cards|Stacked|True{Button:IconButton|Button:SimpleButton}
Carousel|Carousel|True{}
Carousel|Full|True{}
Checkboxes|Checkboxes|True{}
Chips|Assistive|True{}
Chips|Filter|True{}
Chips|Input|True{}
Chips|Suggestion|True{}
DatePicker|Docked|True{}
DatePicker|Input|True{}
DatePicker|Modal|True{}
Dialog|Basic|True{Button:SimpleButton}
Dialog|List|True{Lists:None|Button:SimpleButton}
Dialog|Scrollable|True{Lists:None|Button:SimpleButton}
DividerHoriz|Subhead|True{}
DividerHoriz|Full|True{}
DividerHoriz|Inset|True{}
DividerHoriz|Middle|True{}
DividerVert|Full|True{}
DividerVert|Inset|True{}
DividerVert|Middle|True{}
Lists|List0|True{ListItem:None}
Lists|List-2|True{ListItem:None}
Lists|List-4|True{ListItem:None}
ListBlocks|Enabled|False{}
ListBlocks|Hovered|False{}
ListBlocks|Focused|False{}
ListBlocks|Pressed|False{}
ListBlocks|Dragged|False{}
ListItem|Item0|False{}
ListItem|Item-2|False{}
ListItem|Item-4|False{}
Menu|Menu|True{MenuListItem:None}
Menu|Icon|True{Menu:Menu}
Menu|TextField1|True{Menu:Menu}
Menu|TextField2|True{Menu:Menu}
Nav|Bar|True{NavBlocks:None}
Nav|Drawer|True{NavBlocks:None}
Nav|Rail|True{NavBlocks:None}
NavBlocks|Item1|False{}
NavBlocks|Item2|False{}
NavBlocks|Item3|False{}
ProgressInd|CircDet|True{}
ProgressInd|CircInDet|True{}
ProgressInd|LinDet|True{}
ProgressInd|LinInDet|True{}
RadioButtons|RadioButtons|True{}
SearchBar|SearchBar|True{}
SearchBar|Full|True{ListItem:None}
SearchBar|View|True{ListItem:None}
Sheets|Bottom|True{}
Sheets|Side|True{Button:SimpleButton}
Sliders|Centered|True{}
Sliders|Continuous|True{}
Sliders|Discrete|True{}
Sliders|Range|True{}
Snackbar|Snackbar|True{}
Switch|Switch|True{}
Tabs|Tabs|True{TabsBlocksPri:None}
TabsBlocksPri|IconLabel|False{}
TabsBlocksPri|Icon|False{}
TabsBlocksPri|Label|False{}
TabsBlocksSec|IconLabel|False{}
TabsBlocksSec|Label|False{}
TextFields|TextFields|True{}
TimePicker|Dial|True{Button:SimpleButton}
TimePicker|Keyboard|True{Button:SimpleButton}
ToolTip|Plain|True{}
ToolTip|Rich|True{Button:SimpleButton}
Custom|Label|True{}
Custom|Rectangle|True{}
Custom|Placeholder|True{}
Custom|Icon|True{}
MenuListItem|ListItem|False{}

GUI description: "{placeholder_gui_text}"

user story: "{placeholder_us}"

output:
'''

ZS_TEMPLATE_STAGE_2_PROMPT = '''You are given a user story in the context of a graphical user interface (which is described also briefly in text), this user story is not yet implemented. In addition, you are given a list of UI components that you must use to implement the user story. The components have already been selected by an expert, so use these to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later: 

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}} 

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options:" {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}} 

Note that for the options, you should select exactly one of the options from the list. If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below. For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options:" {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure to always include general_attributes.

Your task implement the feature of the user story by using the given components and create accurate instantiations. Make sure to consider the GUI context given by the textual description of the GUI while implementing the GUI feature, but focus on implementing the specifc functionality requested in the user story. Do not provide any explanation. Output the result as a dictionary and for each main component (i.e. not the sub components), create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"comp-1": {"group": "Button" etc.}, "comp-2": {"group": "Chips" etc.}). Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size. 

Component library: \n{placeholder_component_library} 

General attributes: \n{placeholder_general_attributes} 

Icons: \n{placeholder_icon_library} 

GUI text description: "{placeholder_gui_text}" 

User story: "{placeholder_us}"
'''

ZS_TEMPLATE_FEATURE_LIST_STAGE_1_PROMPT = '''
You are given a list of user stories with a name and a description in the context of a graphical user interface (which is described also briefly in text), these user stories are not yet implemented. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user stories. Each new line represents a new UI component, which comes in the format "group|type|standalone{group:type|...}, where group refers to the general component group, type 
to the specific component type and standalone is a Boolean representing whether it can be used as a standalone component, and none or multiple sub components that the component uses. If the type is set to None in the sub components, any of the types from the group can be selected. In the case of when the type is set to None, always make sure to select a matching component type from the specified group and add it to the list. Your task is to select all the components relevant to implement the user stories. If the component has sub components, also explicitly select them as components, and potentially 
their sub components and so on. For example, when selecting a Dialog|List, then a Button|SimpleButton has to be included, but also e.g. a Lists|List0 and also their sub components in this case e.g. the ListItem|Item0. Make sure to consider the GUI context given by the textual description of the GUI while implementing the GUI feature, but focus on implementing the specific functionality requested in the user stories. Output the result as a dictionary and for each user story, create a new key (being the number of the user story) with the corresponding list of  "group|type" strings representing all selected components for that user story as a correct JSON (e.g., {"1": ["AppBar|Top", "Button|SimpleButton" etc.]). Do not provide any explanation and do not provide any python markup.

Components:

AppBar|Bottom|True{Button:FAB}
AppBar|Top|True{}
Button|SimpleButton|True{}
Button|ExtFAB|True{}
Button|FAB|True{}
Button|Icon|True{}
Button|IconTogg|True{}
Button|LargeFAB|True{}
Button|SegButton|True{SegButtonBlocks:Start|SegButtonBlocks:None}
Button|SmallFAB|True{}
SegButtonBlocks|End|False{}
SegButtonBlocks|Mid|False{}
SegButtonBlocks|Start|False{}
Badges|Badges|True{}
Cards|Horizontal|True{}
Cards|Stacked|True{Button:IconButton|Button:SimpleButton}
Carousel|Carousel|True{}
Carousel|Full|True{}
Checkboxes|Checkboxes|True{}
Chips|Assistive|True{}
Chips|Filter|True{}
Chips|Input|True{}
Chips|Suggestion|True{}
DatePicker|Docked|True{}
DatePicker|Input|True{}
DatePicker|Modal|True{}
Dialog|Basic|True{Button:SimpleButton}
Dialog|List|True{Lists:None|Button:SimpleButton}
Dialog|Scrollable|True{Lists:None|Button:SimpleButton}
DividerHoriz|Subhead|True{}
DividerHoriz|Full|True{}
DividerHoriz|Inset|True{}
DividerHoriz|Middle|True{}
DividerVert|Full|True{}
DividerVert|Inset|True{}
DividerVert|Middle|True{}
Lists|List0|True{ListItem:None}
Lists|List-2|True{ListItem:None}
Lists|List-4|True{ListItem:None}
ListBlocks|Enabled|False{}
ListBlocks|Hovered|False{}
ListBlocks|Focused|False{}
ListBlocks|Pressed|False{}
ListBlocks|Dragged|False{}
ListItem|Item0|False{}
ListItem|Item-2|False{}
ListItem|Item-4|False{}
Menu|Menu|True{MenuListItem:None}
Menu|Icon|True{Menu:Menu}
Menu|TextField1|True{Menu:Menu}
Menu|TextField2|True{Menu:Menu}
Nav|Bar|True{NavBlocks:None}
Nav|Drawer|True{NavBlocks:None}
Nav|Rail|True{NavBlocks:None}
NavBlocks|Item1|False{}
NavBlocks|Item2|False{}
NavBlocks|Item3|False{}
ProgressInd|CircDet|True{}
ProgressInd|CircInDet|True{}
ProgressInd|LinDet|True{}
ProgressInd|LinInDet|True{}
RadioButtons|RadioButtons|True{}
SearchBar|SearchBar|True{}
SearchBar|Full|True{ListItem:None}
SearchBar|View|True{ListItem:None}
Sheets|Bottom|True{}
Sheets|Side|True{Button:SimpleButton}
Sliders|Centered|True{}
Sliders|Continuous|True{}
Sliders|Discrete|True{}
Sliders|Range|True{}
Snackbar|Snackbar|True{}
Switch|Switch|True{}
Tabs|Tabs|True{TabsBlocksPri:None}
TabsBlocksPri|IconLabel|False{}
TabsBlocksPri|Icon|False{}
TabsBlocksPri|Label|False{}
TabsBlocksSec|IconLabel|False{}
TabsBlocksSec|Label|False{}
TextFields|TextFields|True{}
TimePicker|Dial|True{Button:SimpleButton}
TimePicker|Keyboard|True{Button:SimpleButton}
ToolTip|Plain|True{}
ToolTip|Rich|True{Button:SimpleButton}
Custom|Label|True{}
Custom|Rectangle|True{}
Custom|Placeholder|True{}
Custom|Icon|True{}
MenuListItem|ListItem|False{}

GUI description: "{placeholder_gui_text}"
User stories:
{placeholder_us_multiple}

output:'''

ZS_TEMPLATE_FEATURE_LIST_STAGE_2_PROMPT = '''You are given a list of user stories with a name and a description in the context of a graphical user interface (which is described also briefly in text), this user story is not yet implemented. In addition, you are given a list of UI components that you can use to implement the user story. For each user story, the components to use have already been selected by an expert (added at the end of each user story), so use these to implement the user stories. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set.Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component and their sub components. Here is an example of a component followed by an example how it should be created later: 

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}} 

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}} 

Note that for the options, you should select exactly one of the options from the list (also when the values represent numbers e.g. "Value": ["0", "50", "100"], then you must select a number from the given list). If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below. For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options": {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure that all of these sub components always have "general_attributes".

Your task is to implement the features for each user story by using the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for each user story, create a new key (being the number of the user story) with the corresponding implementation as the value as a correct JSON (e.g., {"1": [{"group": "Button" etc.}, {"group": "Chips" etc.}]). For each user story, create a list containing the main components (i.e. not the sub components) to fulfill the user story. Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

GUI description: "{placeholder_gui_text}"

User stories: 
{placeholder_us_multiple}

output:
'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_1 = '''
You are given an user story with a name and a description in the context of a graphical user interface (which is described also briefly in text). In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes in the format "group|type|standalone{group:type|...}, where group refers to the general component group, type to the specific component type and standalone is a Boolean representing whether it can be used as a standalone component, and none or multiple sub components that the component uses. If the type is set to None in the sub components, any of the types from the group can be selected. In the case of when the type is set to None, always make sure to select a matching component type from the specified group and add it to the list. 

In addition to the given information, you are also given a first selection of components for the user story. Your task is to implement {placeholder_num_variants} more variants for the user story that are all different by selecting the given components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for new implementation of the user story, create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"variant-1": ["Button|SimpleButton", etc.]). If the component has sub components, also explicitly select them as components, and potentially their sub components and so on. For example, when selecting a Dialog|List, then a Button|SimpleButton has to be included, but also e.g. a Lists|List0 and also their sub components in this case e.g. the ListItem|Item0. And for example, sometimes a component has also multiple sub components (e.g., Cards|Stacked|True{Button:IconButton|Button:SimpleButton} has two different buttons as sub components), make sure to also include them. Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size.

Components:

AppBar|Bottom|True{Button:FAB}
AppBar|Top|True{}
Button|SimpleButton|True{}
Button|ExtFAB|True{}
Button|FAB|True{}
Button|Icon|True{}
Button|IconTogg|True{}
Button|LargeFAB|True{}
Button|SegButton|True{SegButtonBlocks:Start|SegButtonBlocks:None}
Button|SmallFAB|True{}
SegButtonBlocks|End|False{}
SegButtonBlocks|Mid|False{}
SegButtonBlocks|Start|False{}
Badges|Badges|True{}
Cards|Horizontal|True{}
Cards|Stacked|True{Button:IconButton|Button:SimpleButton}
Carousel|Carousel|True{}
Carousel|Full|True{}
Checkboxes|Checkboxes|True{}
Chips|Assistive|True{}
Chips|Filter|True{}
Chips|Input|True{}
Chips|Suggestion|True{}
DatePicker|Docked|True{}
DatePicker|Input|True{}
DatePicker|Modal|True{}
Dialog|Basic|True{Button:SimpleButton}
Dialog|List|True{Lists:None|Button:SimpleButton}
Dialog|Scrollable|True{Lists:None|Button:SimpleButton}
DividerHoriz|Subhead|True{}
DividerHoriz|Full|True{}
DividerHoriz|Inset|True{}
DividerHoriz|Middle|True{}
DividerVert|Full|True{}
DividerVert|Inset|True{}
DividerVert|Middle|True{}
Lists|List0|True{ListItem:None}
Lists|List-2|True{ListItem:None}
Lists|List-4|True{ListItem:None}
ListBlocks|Enabled|False{}
ListBlocks|Hovered|False{}
ListBlocks|Focused|False{}
ListBlocks|Pressed|False{}
ListBlocks|Dragged|False{}
ListItem|Item0|False{}
ListItem|Item-2|False{}
ListItem|Item-4|False{}
Menu|Menu|True{MenuListItem:None}
Menu|Icon|True{Menu:Menu}
Menu|TextField1|True{Menu:Menu}
Menu|TextField2|True{Menu:Menu}
Nav|Bar|True{NavBlocks:None}
Nav|Drawer|True{NavBlocks:None}
Nav|Rail|True{NavBlocks:None}
NavBlocks|Item1|False{}
NavBlocks|Item2|False{}
NavBlocks|Item3|False{}
ProgressInd|CircDet|True{}
ProgressInd|CircInDet|True{}
ProgressInd|LinDet|True{}
ProgressInd|LinInDet|True{}
RadioButtons|RadioButtons|True{}
SearchBar|SearchBar|True{}
SearchBar|Full|True{ListItem:None}
SearchBar|View|True{ListItem:None}
Sheets|Bottom|True{}
Sheets|Side|True{Button:SimpleButton}
Sliders|Centered|True{}
Sliders|Continuous|True{}
Sliders|Discrete|True{}
Sliders|Range|True{}
Snackbar|Snackbar|True{}
Switch|Switch|True{}
Tabs|Tabs|True{TabsBlocksPri:None}
TabsBlocksPri|IconLabel|False{}
TabsBlocksPri|Icon|False{}
TabsBlocksPri|Label|False{}
TabsBlocksSec|IconLabel|False{}
TabsBlocksSec|Label|False{}
TextFields|TextFields|True{}
TimePicker|Dial|True{Button:SimpleButton}
TimePicker|Keyboard|True{Button:SimpleButton}
ToolTip|Plain|True{}
ToolTip|Rich|True{Button:SimpleButton}
Custom|Label|True{}
Custom|Rectangle|True{}
Custom|Placeholder|True{}
Custom|Icon|True{}
MenuListItem|ListItem|False{}

GUI description: "{placeholder_gui_text}"
User story name: "{placeholder_user_story_name}"
User story description: "{placeholder_user_story_description}"
Current implementation: {placeholder_current_implementation}

output:
'''

ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_STAGE_2 = '''
You are given an user story with a name and a description in the context of a graphical user interface (which is described also briefly in text). In addition, you are given a list of UI components that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set.Moreover, there are general attributes (e.g., xPos, yPos, width, height etc.) that also should be set for each component and their sub components. Here is an example of a component followed by an example how it should be created later: 

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}} 

Component Instantiation Example: {"group": "Button", "type": "SimpleButton", "options": {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}} 

Note that for the options, you should select exactly one of the options from the list (also when the values represent numbers e.g. "Value": ["0", "50", "100"], then you must select a number from the given list). If you set an attribute similar to "icons" to "True", then you should also provide a text for the respective icons in the "attributes". This value should be one of the strings from the icons list provided below. For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton", "cardinality": "single"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. If the "cardinality" is set to "single", then only a single component can be instantiated. Do not provide these references as new lines, instead, directly write their instantiations as the attribute e.g., "primary_action": {"group": "Button", "type": "SimpleButton", "options": {"Style": "Filled", "State": "Enabled", "Show Icon": "True"}", "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"name": "calculation button", "xPos": "0", "yPos": "0", "width": "200", "height": "50", "fontSize": "4", "textAlign": "center", "textVerticalAlign": "middle", "opacity": "0"}. If "cardinality" is set to "multiple", then a list of these component instantiations should be created (e.g. "Lists" have an attribute "List Items" which will be a list of multiple "ListItem" instantiations). Make sure that all of these sub components always have "general_attributes".

In addition to the given information, you are also given the current implementation of the user story, which is represented by selected components. Moreover, an expert created {placeholder_num_variants} variants of the feature implementation and selected components for each of the variant. Your task is to implement these variants for the user story by using the preselected components and create accurate instantiations. Do not provide any explanation. Output the result as a dictionary and for new implementation of the user story,  create a new key with the corresponding implementation as the value as a correct JSON (e.g., {"variant-1": [{"group": "Button" etc.}, {"group": "Chips" etc.}]). For the user story, create a list containing the main components (i.e. not the sub components) to fulfill the user story. Do not provide the answer in a JSON markdown or any other markdown, directly output the JSON. The  width of the screen is 420 and the height is 892, so create recommendations that fit into such a screen size.

Component library: \n{placeholder_component_library}

General attributes: \n{placeholder_general_attributes}

Icons: \n{placeholder_icon_library}

GUI description: "{placeholder_gui_text}"
User story name: "{placeholder_user_story_name}"
User story description: "{placeholder_user_story_description}"
Current implementation: {placeholder_current_implementation}
Variant selected components:
{placeholder_selected_comps_variants}

output:
'''

ZS_RECOMMENDATION_SINGLE_TEMPLATE = {ZS_TEMPLATE_SINGLE_RECOMMENDATION_1, ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE, ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE}

COMPONENT_LIBRARY_1 = "component-library-1"

COMPONENT_LIBRARY_2 = "component-library-2"

COMPONENT_LIBRARY_3 = "component-library-3"

GENERAL_COMPONENT_ATTRIBUTES_1 = '''
{
  "name": "String",
  "xPos": "Number",
  "yPos": "Number",
  "width": "Number",
  "height": "Number",
  "fontSize": "Number",
  "textAlign": ["left", "center", "right"],
  "textVerticalAlign": ["top", "middle", "bottom"],
  "opacity": "Number"
}
'''

ICON_LIBRARY_1 = '''
["sticker", "check_small", "directions_car", "radio_button_unchecked", "cancel", "bookmark_filled", "share", "navigate_next", "skip_previous_filled", "commute", "gmail_groups", "today", "upload", "folder", "fast_forward_filled", "GIF", "schedule", "chat_bubble", "attach_file", "account_circle", "navigate_before", "light_mode", "mic", "notifications", "folder_filled", "videocam", "arrow_back", "error", "star", "mood", "arrow_left", "inbox", "arrow_forward", "edit", "play_arrow", "check_box_outline_blank", "pause", "keyboard", "indeterminate_check_box", "arrow_drop_up", "mail", "delete", "person", "content_cut", "photo", "download", "play_arrow_filled", "outbox", "radio_button_checked", "text_fields", "language", "add_circle", "skip_next", "close", "mobile_friendly", "directions_subway", "star_filled", "fast_rewind_filled", "directions_walk", "location_on", "skip_previous", "settings", "list", "check", "local_taxi", "archive", "arrow_right", "keyboard_return", "search", "music_note", "send", "check_box", "add", "forward", "directions_bus", "fast_rewind", "dark_mode", "skip_next_filled", "bookmark", "fast_forward", "check_indeterminate_small", "menu", "more_horiz", "stars", "more_vert", "arrow_drop_down", "favorite", "g_translate"]
'''

NEW_PROMPT = '''
You are given a user story in the context of a graphical user interface, this user story is not yet implemented. In addition to the user story, you are also given a textual description of a graphical user interface, for which the user story should be implemented. In addition, you are given a list of UI components (i.e. component library) that you can use to implement the user story. Each new line represents a new UI component, which comes as a JSON with a group, type, whether it can be used as a standalone component and several options and attributes that must be set. Moreover, there are general attributes (e.g., x, y, width, height etc.) that also should be set for each component. Here is an example of a component followed by an example how it should be created later: 

Component Library Example: {"group:": "Button", "type": "SimpleButton", "standalone": "True", "options:" {"Style": ["Tonal", "Elevated", "Text", "Outlined", "Filled"], "State": ["Disabled", "Pressed", "Focused", "Hovered", "Enabled"], "Show Icon": ["True", "False"]}", "attributes:" {"Icon": "String", "Label Text": "String"}}

Component Instantiation Example: {"group:": "Button", "type": "SimpleButton", "options:" {"Style":  "Filled", "State":  "Enabled", "Show Icon": "True"}",  "attributes:" {"Icon": "play", "Label Text": "Start Calculation"}, "general_attributes": {"x": "0", "y": "0", "width": "200", "height": "50"}}

Note that for the options, you should select exactly one of the options from the list. For the attributes, it is specified what datatype it is (usually string), but it can also be a reference to another component in the library, which in turn also needs to be instantiated. This reference is represented by a JSON with an attribute "group" and "instance", for example: "primary_action": {"Group": "Button", "Instance": "SimpleButton"}. This means that the "primary_action" attribute refers to the group of "Button" and the concrete instance "SimpleButton". Hence, an entire button instance needs to be instantiated correctly for this attribute. If the "Instance" is None, any of the components from the group can be chosen. 

Your task implement the feature of the user story by using the given components and create accurate instantiations. Do not provide any explanation. Output each component instantiation by starting a new line and produce correct JSON for each instantiation.

GUI description: "Settings in a music player app"
Component Library:
'''

CARDINALITY_SINGLE = "single"
CARDINALITY_MULTIPLE = "mutliple"


ZS_TEMPLATE_SINGLE_USER_STORY_GENERATION_1 = '''You are given a textual representation of a graphical user interface. The 
GUI is organized as a multi-level bullet point list, the outer points representing layouting groups or components and the 
inner points the user interface features contained in that layouting group or component, sometimes the grouping information 
may not be available. Each feature is represented in the following abstract pattern: - component-group (component-type) (position) (size) |attribute name:"attribute value".
Your task is to create an exhaustive list of user stories implemented in the GUI prototype and output a Python list of 
strings. Do not provide any explanation. Do not provide any Python markdown, directly output the list.

GUI representation:\n\n{placeholder_gui}

output:'''

if __name__ == "__main__":
    filled_prompt = ZS_TEMPLATE_SINGLE_RECOMMENDATION_1.replace(PLACEHOLDER_COMPONENT_LIBRARY, COMPONENT_LIBRARY_1) \
                                                        .replace(PLACEHOLDER_GENERAL_ATTRIBUTES, GENERAL_COMPONENT_ATTRIBUTES_1) \
                                                        .replace(PLACEHOLDER_GUI, 'GUI-Test') \
                                                        .replace(PLACEHOLDER_US, 'US-Test')
    print(filled_prompt)