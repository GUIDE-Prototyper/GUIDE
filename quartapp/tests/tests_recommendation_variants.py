from quartapp.openai_conf import openai_client
from quartapp.recommendation.prompts import ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1
from quartapp.utils.gui2string import GUI2String
from quartapp.recommendation.recommendation import Recommendation
import asyncio


gui2string = GUI2String()
recommendation = Recommendation(openai_client=openai_client, gui2string=gui2string,
                                prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1)

num_variants = 3
text = "a product detail view"
user_story = {
        "description": "A high-quality image of the product that allows users to see what they are purchasing.",
        "name": "Product Image",
        "number": "1",
        "recommendation": [
            {
                "attributes": {
                    "Header Text": "Product Image",
                    "Media": "product_image_url",
                    "Monogram": "",
                    "Subheader Text": ""
                },
                "general_attributes": {
                    "fontSize": "0",
                    "height": "300",
                    "key": "a50608d9b12e6a77b526772c4794e94ff8c91726",
                    "name": "product_image",
                    "opacity": "1",
                    "textAlign": "center",
                    "textVerticalAlign": "middle",
                    "width": "400",
                    "xPos": "10",
                    "yPos": "10"
                },
                "group": "Cards",
                "options": {
                    "Style": "Elevated"
                },
                "type": "Horizontal"
            }
        ]
    }

loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(recommendation.recommendation_feature_variants_1(num_variants=num_variants,
                                                                                  text=text, user_story=user_story))
