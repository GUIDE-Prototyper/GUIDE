import asyncio

from quartapp.generation.generation import Generation
from quartapp.utils.gui2string import GUI2String
from quartapp.openai_conf import openai_client
from ast import literal_eval

prototype = literal_eval('''
    "ui_comps": [
        {
                "attributes": {
                    "headline": "Shopping List",
                    "leading icon": "menu",
                    "trailing icon": "more_vert"
                },
                "generalAttributes": {
                    "fontSize": "4",
                    "height": "70",
                    "key": "f31942c1d4cfcea7f9ecd727ea411575d309d575",
                    "name": "top app bar",
                    "opacity": "1",
                    "textAlign": "center",
                    "textVerticalAlign": "middle",
                    "width": "420",
                    "xPos": "0",
                    "yPos": "0"
                },
                "group": "AppBar",
                "options": {
                    "Configuration": "Small",
                    "Elevation": "flat"
                },
                "type": "Top"
            },
      {
        "type": "Checkboxes",
        "group": "Checkboxes",
        "attributes": {
          "Standalone": true,
          "NumOptions": 2,
          "Type": "Selected",
          "Style": "Enabled"
        },
        "options": {
          "Type": "Selected",
          "Style": "Enabled"
        },
        "generalAttributes": {
          "figmaId": "137:5036",
          "id": "137:5036",
          "name": "Checkboxes",
          "xPos": 440,
          "yPos": 534,
          "matTitle": "Checkboxes",
          "key": "803e8921331bef5e7a9fb432862b80025b96d164",
          "width": 48,
          "height": 48,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Checkboxes",
        "group": "Checkboxes",
        "attributes": {
          "Standalone": true,
          "NumOptions": 2,
          "Type": "Unselected",
          "Style": "Enabled"
        },
        "options": {
          "Type": "Unselected",
          "Style": "Enabled"
        },
        "generalAttributes": {
          "figmaId": "137:5037",
          "id": "137:5037",
          "name": "Checkboxes",
          "xPos": 440,
          "yPos": 582,
          "matTitle": "Checkboxes",
          "key": "7d8905955a3f88c7f918e3a873dafb6f785110f9",
          "width": 48,
          "height": 48,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Full",
        "group": "DividerHoriz",
        "attributes": {
          "NumOptions": 0,
          "Standalone": true
        },
        "generalAttributes": {
          "figmaId": "137:5038",
          "id": "137:5038",
          "name": "Horizontal/Full-width",
          "xPos": 32,
          "yPos": 170,
          "matDescr": "Dividers are one way to visually group components and create hierarchy. They can also be used to imply nested parent/child relationships.\n\nUse full width dividers to separate larger sections of unrelated content. They can be used directly on a surface or inside other components like cards or lists.",
          "key": "b7f38eebae3ae9bbf4c127fe0686fcf409d5ffc8",
          "width": 437,
          "height": 3,
          "visible": true,
          "fontSize": null,
          "rotation": -0.000005008956130975318,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Mid",
        "group": "SegButtonBlocks",
        "attributes": {
          "Icon": "stars",
          "Text": "DELETE",
          "NumOptions": 3,
          "Standalone": false,
          "Configuration": "Label & icon",
          "Style": "Enabled",
          "Selected": "True"
        },
        "options": {
          "Configuration": "Label & icon",
          "Style": "Enabled",
          "Selected": "True"
        },
        "generalAttributes": {
          "figmaId": "137:5039",
          "id": "137:5039",
          "name": "Building Blocks/Segmented button/Button segment (middle)",
          "xPos": 4,
          "yPos": 772,
          "matTitle": "Building Blocks/Segmented button/Button segment (middle)",
          "key": "33d36c5c7adba42b0984a780f2eeb8c44831381a",
          "width": 146,
          "height": 62,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Label",
        "group": "Custom",
        "attributes": {
          "Label Text": "MOVE",
          "Standalone": true,
          "NumOptions": 0
        },
        "generalAttributes": {
          "figmaId": "137:5043",
          "id": "137:5043",
          "name": "label-text",
          "xPos": 222,
          "yPos": 793,
          "width": 56,
          "height": 20,
          "visible": true,
          "fontSize": 20,
          "fontName": {
            "family": "Roboto",
            "style": "Medium"
          },
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "color": [
            {
              "type": "SOLID",
              "color": "#1d192b",
              "opacity": "100%"
            }
          ]
        }
      },
      {
        "type": "Label",
        "group": "Custom",
        "attributes": {
          "Label Text": "SAVE ",
          "Standalone": true,
          "NumOptions": 0
        },
        "generalAttributes": {
          "figmaId": "137:5047",
          "id": "137:5047",
          "name": "label-text",
          "xPos": 433,
          "yPos": 50,
          "width": 50,
          "height": 20,
          "visible": true,
          "fontSize": 20,
          "fontName": {
            "family": "Roboto",
            "style": "Medium"
          },
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "color": [
            {
              "type": "SOLID",
              "color": "#1d192b",
              "opacity": "100%"
            }
          ]
        }
      },
      {
        "type": "Label",
        "group": "Custom",
        "attributes": {
          "Label Text": "Item has sales tax ",
          "Standalone": true,
          "NumOptions": 0
        },
        "generalAttributes": {
          "figmaId": "137:5051",
          "id": "137:5051",
          "name": "label-text",
          "xPos": 32.5,
          "yPos": 547.5,
          "width": 165,
          "height": 20,
          "visible": true,
          "fontSize": 20,
          "fontName": {
            "family": "Roboto",
            "style": "Medium"
          },
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "color": [
            {
              "type": "SOLID",
              "color": "#1d192b",
              "opacity": "100%"
            }
          ]
        }
      },
      {
        "type": "Label",
        "group": "Custom",
        "attributes": {
          "Label Text": "I have a coupon for this item ",
          "Standalone": true,
          "NumOptions": 0
        },
        "generalAttributes": {
          "figmaId": "137:5055",
          "id": "137:5055",
          "name": "label-text",
          "xPos": 32.5,
          "yPos": 599.5,
          "width": 257,
          "height": 20,
          "visible": true,
          "fontSize": 20,
          "fontName": {
            "family": "Roboto",
            "style": "Medium"
          },
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "color": [
            {
              "type": "SOLID",
              "color": "#1d192b",
              "opacity": "100%"
            }
          ]
        }
      },
      {
        "type": "Subhead",
        "group": "DividerHoriz",
        "attributes": {
          "Text": "Notes",
          "NumOptions": 0,
          "Standalone": true
        },
        "generalAttributes": {
          "figmaId": "137:5060",
          "id": "137:5060",
          "name": "Horizontal/Divider with subhead",
          "xPos": 23,
          "yPos": 658,
          "matDescr": "Dividers are one way to visually group components and create hierarchy. They can also be used to imply nested parent/child relationships.",
          "key": "f02a5fa2dcf4b078588979f112963b1012ce0c23",
          "width": 453,
          "height": 34,
          "visible": true,
          "fontSize": null,
          "rotation": -0.000005008956130975318,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Label",
        "group": "Custom",
        "attributes": {
          "Label Text": "Milk",
          "Standalone": true,
          "NumOptions": 0
        },
        "generalAttributes": {
          "figmaId": "137:5061",
          "id": "137:5061",
          "name": "Milk",
          "xPos": 4,
          "yPos": 137,
          "width": 98,
          "height": 28,
          "visible": true,
          "fontSize": 20,
          "fontName": {
            "family": "Roboto",
            "style": "Medium"
          },
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "color": [
            {
              "type": "SOLID",
              "color": "#000000",
              "opacity": "100%"
            }
          ]
        }
      },
      {
        "type": "TextFields",
        "group": "TextFields",
        "attributes": {
          "Label Text": "Quantity ",
          "Input Text": "--   +                     1",
          "Supporting Text": "Supporting text",
          "Show Support Text": true,
          "Leading Icon": "False",
          "Placeholder Text": "Placeholder",
          "Text Configuration": "Input text",
          "Trailing Icon": "True",
          "Standalone": true,
          "NumOptions": 5
        },
        "options": {
          "Style": "Filled",
          "State": "Enabled",
          "Text configurations": "Input text",
          "Leading icon": "False",
          "Trailing icon": "True"
        },
        "generalAttributes": {
          "figmaId": "137:5062",
          "id": "137:5062",
          "name": "Text field",
          "xPos": 32,
          "yPos": 205,
          "matTitle": "Text field",
          "key": "b16ac5a75a96c57615b2b7640135f096927f20fa",
          "width": 210,
          "height": 56,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "TextFields",
        "group": "TextFields",
        "attributes": {
          "Label Text": "Unit Price ",
          "Input Text": "$  1.99",
          "Supporting Text": "Supporting text",
          "Show Support Text": true,
          "Leading Icon": "False",
          "Placeholder Text": "Placeholder",
          "Text Configuration": "Input text",
          "Trailing Icon": "True",
          "Standalone": true,
          "NumOptions": 5
        },
        "options": {
          "Style": "Filled",
          "State": "Enabled",
          "Text configurations": "Input text",
          "Leading icon": "False",
          "Trailing icon": "True"
        },
        "generalAttributes": {
          "figmaId": "137:5063",
          "id": "137:5063",
          "name": "Text field",
          "xPos": 32,
          "yPos": 384,
          "matTitle": "Text field",
          "key": "b16ac5a75a96c57615b2b7640135f096927f20fa",
          "width": 210,
          "height": 56,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "TextFields",
        "group": "TextFields",
        "attributes": {
          "Label Text": "Category",
          "Input Text": "Dairy ",
          "Supporting Text": "Supporting text",
          "Show Support Text": true,
          "Leading Icon": "False",
          "Placeholder Text": "Placeholder",
          "Text Configuration": "Input text",
          "Trailing Icon": "True",
          "Standalone": true,
          "NumOptions": 5
        },
        "options": {
          "Style": "Filled",
          "State": "Enabled",
          "Text configurations": "Input text",
          "Leading icon": "False",
          "Trailing icon": "True"
        },
        "generalAttributes": {
          "figmaId": "137:5064",
          "id": "137:5064",
          "name": "Text field",
          "xPos": 33,
          "yPos": 293,
          "matTitle": "Text field",
          "key": "b16ac5a75a96c57615b2b7640135f096927f20fa",
          "width": 210,
          "height": 56,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Icon",
        "group": "Custom",
        "attributes": {
          "Standalone": true,
          "NumOptions": 0,
          "Icon": "more_vert"
        },
        "generalAttributes": {
          "figmaId": "137:5065",
          "id": "137:5065",
          "name": "more_vert",
          "xPos": 394,
          "yPos": 48,
          "key": "85ee52341e2845c3614046bb7d834c42faee1f67",
          "width": 24,
          "height": 24,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Icon",
        "group": "Custom",
        "attributes": {
          "Standalone": true,
          "NumOptions": 0,
          "Icon": "close"
        },
        "generalAttributes": {
          "figmaId": "137:5066",
          "id": "137:5066",
          "name": "close",
          "xPos": 10,
          "yPos": 41,
          "key": "64f805a63adf73d8a9f453e3c4ad5a5ce0d8850a",
          "width": 40,
          "height": 38,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Icon",
        "group": "Custom",
        "attributes": {
          "Standalone": true,
          "NumOptions": 0,
          "Icon": "arrow_drop_down"
        },
        "generalAttributes": {
          "figmaId": "137:5067",
          "id": "137:5067",
          "name": "arrow_drop_down",
          "xPos": 214,
          "yPos": 227,
          "key": "d2547873f01e49c6d52afbe1d816ff21c8f8f95d",
          "width": 24,
          "height": 24,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Icon",
        "group": "Custom",
        "attributes": {
          "Standalone": true,
          "NumOptions": 0,
          "Icon": "arrow_drop_down"
        },
        "generalAttributes": {
          "figmaId": "137:5068",
          "id": "137:5068",
          "name": "arrow_drop_down",
          "xPos": 172,
          "yPos": 308,
          "key": "d2547873f01e49c6d52afbe1d816ff21c8f8f95d",
          "width": 24,
          "height": 24,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },
      {
        "type": "Icon",
        "group": "Custom",
        "attributes": {
          "Standalone": true,
          "NumOptions": 0,
          "Icon": "edit"
        },
        "generalAttributes": {
          "figmaId": "137:5069",
          "id": "137:5069",
          "name": "edit",
          "xPos": 209,
          "yPos": 308,
          "key": "452979286e0ab19ef7eecb057dfd10215fdaf9e3",
          "width": 24,
          "height": 24,
          "visible": true,
          "fontSize": null,
          "rotation": 0,
          "removed": false,
          "opacity": 1,
          "minWidth": null,
          "minHeight": null,
          "locked": false,
          "expanded": false
        }
      },            {
                "attributes": {
                    "FAB": {
                        "attributes": {
                            "Icon": "add"
                        },
                        "generalAttributes": {
                            "fontSize": 4,
                            "height": 60,
                            "key": "ba0f2bd7cbbc6459659d067969aa99cefa89d181",
                            "name": "fab button",
                            "opacity": 1,
                            "textAlign": "center",
                            "textVerticalAlign": "middle",
                            "width": 60,
                            "xPos": 180,
                            "yPos": 10
                        },
                        "group": "Button",
                        "options": {
                            "State": "Enabled",
                            "Style": "Primary"
                        },
                        "type": "FAB"
                    },
                    "Icon 1": "home",
                    "Icon 2": "search",
                    "Icon 3": "notifications",
                    "Icon 4": "settings",
                    "Show FAB": "True"
                },
                "generalAttributes": {
                    "fontSize": 4,
                    "height": 70,
                    "key": "a462d6913507362de07fdfaa71f0f09082a1b411",
                    "name": "bottom app bar",
                    "opacity": 1,
                    "textAlign": "center",
                    "textVerticalAlign": "middle",
                    "width": 420,
                    "xPos": 0,
                    "yPos": 822
                },
                "group": "AppBar",
                "options": {
                    "Icons": "4"
                },
                "type": "Bottom"
            }
    ],
    "ui_groups": [
      
    ]
  }
''')


gui2string = GUI2String()
generation = Generation(openai_client=openai_client, gui2string=gui2string, max_retries=1)

loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(generation.generation_entire_gui(prototype=prototype))