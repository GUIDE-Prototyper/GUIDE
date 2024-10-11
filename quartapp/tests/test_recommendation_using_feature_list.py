from quartapp.openai_conf import openai_client
from quartapp.recommendation.prompts import ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1
from quartapp.utils.gui2string import GUI2String
from quartapp.recommendation.recommendation import Recommendation
import asyncio


gui2string = GUI2String()
recommendation = Recommendation(openai_client=openai_client, gui2string=gui2string,
                                prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1)

text = "a product detail view"
user_stories = [
    {
        "description": "A high-quality image of the product that allows users to see what they are purchasing.",
        "name": "Product Image",
        "number": "1"
    },
    {
        "description": "The name of the product, prominently displayed to inform users about the item.",
        "name": "Product Title",
        "number": "2"
    },
    {
        "description": "The current price of the product, clearly shown to help users make purchasing decisions.",
        "name": "Price Display",
        "number": "3"
    },
    {
        "description": "A button that allows users to add the product to their shopping cart for purchase.",
        "name": "Add to Cart Button",
        "number": "4"
    },
    {
        "description": "Detailed information about the product, including features and specifications.",
        "name": "Product Description",
        "number": "5"
    },
    {
        "description": "User-generated reviews and ratings to provide feedback and insights about the product.",
        "name": "Customer Reviews",
        "number": "6"
    },
    {
        "description": "An option for users to select the number of items they wish to purchase.",
        "name": "Quantity Selector",
        "number": "7"
    },
    {
        "description": "Suggestions for similar or complementary products that users might be interested in.",
        "name": "Related Products",
        "number": "8"
    },
    {
        "description": "An option for users to save the product to a wishlist for future consideration.",
        "name": "Wishlist Button",
        "number": "9"
    },
    {
        "description": "A feature that allows users to share the product details with others via social media or messaging.",
        "name": "Share Button",
        "number": "10"
    }
]

loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(recommendation.recommendation_using_feature_list_1(text=text, user_stories=user_stories))

print(result)