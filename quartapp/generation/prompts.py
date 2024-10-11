PLACEHOLDER_US = '{placeholder_us}'
PLACEHOLDER_US_MULTIPLE = '{placeholder_us_multiple}'
PLACEHOLDER_GUI = '{placeholder_gui}'
PLACEHOLDER_GUI_TEXT = '{placeholder_gui_text}'

ZS_TEMPLATE_SINGLE_GENERATION_1 = '''You are given a graphical user interface as a textual representation. The GUI is
 organized as a multi-level bullet point list, the outer points representing layouting groups or components and the 
 inner points the user interface features contained in that layouting group or component. Each feature is represented 
 in the following abstract pattern: component-group (component-type) | "text" (id), the 'text' being the visual text 
 of the component and the 'id' being a number identifying each component. Your task is to write user stories that are 
 implemented in the GUI and extract a list of ids as strings belonging to the user interface components for each written user 
 interface. Do not provide any explanation. As your output, create a JSON with the following structure: 
 {"user_story": "user story text", "comps": [list of component ids belonging to the user story]}. 
 Do not provide any markdown. \n\ngraphical user interface description: {placeholder_gui} \n\noutput:'''

ZS_GENERATION_SINGLE_TEMPALTES = {ZS_TEMPLATE_SINGLE_GENERATION_1}


ZS_TEMPLATE_FEATURE_GENERATION_1 = '''Using the provided short description of a mobile page, please analyze the content 
and identify the specific features that are necessary for optimal functionality and user experience. Focus solely on 
visible functionalities. Output a python list of JSON objects, each feature with a short name and a longer description.
For example: [{"name": "Feature Name", "description": "Longer feature description"}]. Do not provide markdown, directly output the list. 
GUI description: "{placeholder_gui_text}"
ouput:'''

ZS_TEMPLATE_FEATURE_GENERATION_2 = '''Using the provided short description of a mobile page, please analyze the content
and identify the specific features that are necessary for optimal functionality and user experience. Focus solely on 
visible functionalities and do not include non-functional features (e.g., responsive design, accessibility etc.). Make 
sure to include features for the top app bar and bottom app bar with matching functionality. However, do not provide 
additional individual features that reference the top or bottom app bar (e.g., top app bar should include a menu icon).
All information regarding the top and bottom app bars should only provided in the description for these features. 
Write down a comprehensive features set of at least 12 features, describe each feature in detail. Do not repeat features
e.g., when a previous more complex feature already contains sub features, do not include them as individual features.
Sort the feature from top to bottom as they would appear in the mobile app. Output a python list of JSON objects, 
each feature with a short name and a longer description. For example: [{"name": "Feature Name", "description": "Longer feature description"}]. 
Do not provide JSON markdown, directly output the JSON itself.

GUI description:  "{placeholder_gui_text}"
output:'''


ZS_TEMPLATE_FEATURE_GENERATION_2_OLD = '''Using the provided short description of a mobile page, please analyze the content
and identify the specific features that are necessary for optimal functionality and user experience. Focus solely on 
visible functionalities and do not include non-functional features (e.g., responsive design, accessibility etc.). Make 
sure to include features for the top app bar and bottom app bar with matching functionality. However, do not provide 
additional individual features that reference the top or bottom app bar (e.g., top app bar should include a menu icon).
All information regarding the top and bottom app bars should only provided in the description for these features. 
Write down a comprehensive features set of at least 10 features, describe each feature in detail. Do not repeat features
e.g., when a previous more complex feature already contains sub features, do not include them as individual features. 
Output a python list of JSON objects, each feature with a short name and a longer description. For example: [{"name": "Feature Name", "description": "Longer feature description"}]. 
Do not provide JSON markdown, directly output the JSON itself.

GUI description:  "{placeholder_gui_text}"
output:'''

ZS_GENERATION_FEATURE_TEMPLATES = {ZS_TEMPLATE_FEATURE_GENERATION_1, ZS_TEMPLATE_FEATURE_GENERATION_2}