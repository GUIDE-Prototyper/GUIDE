from quartapp.openai_conf import openai_client
from quartapp.recommendation.prompts import ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT
from quartapp.utils.gui2string import GUI2String
from quartapp.recommendation.recommendation import Recommendation
import asyncio


gui2string = GUI2String()
recommendation = Recommendation(openai_client=openai_client, gui2string=gui2string,
                                prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT)

prototype = "Settings in a music player app"
user_stories = [
   {"id": "us1",
     "text": "As a user,  I want a popup alerting me before resetting my settings"
     },
   {"id": "us2",
     "text": "As a user,  I want filter options that I can click easily to filter for different types of genres"
     },
    {"id": "us3",
     "text": "As a user,  I want a list of song playing related settings that can be turned on or off."
     }
]

loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(recommendation.recommendation_no_prototype_text_tokens(text=prototype, user_stories=user_stories))