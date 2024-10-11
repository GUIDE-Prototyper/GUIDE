from quart import Quart, render_template, request, jsonify, Response
from quartapp.authentification.authentification import requires_auth, secret_key
from quartapp.detection.prompts import ZS_TEMPLATE_MULTIPLE_PRED_1
from quartapp.generation.generation import Generation
from quartapp.generation.prompts import ZS_TEMPLATE_FEATURE_GENERATION_1, ZS_TEMPLATE_FEATURE_GENERATION_2
from quartapp.matching.prompts import ZS_TEMPLATE_MULTIPLE_MATCH_1
from quartapp.openai_conf import openai_client
from quartapp.logger_conf import logger
from quartapp.recommendation.prompts import ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE, ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT, ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V2, \
    ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1, ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1
from quartapp.utils.gui2string import GUI2String
from quartapp.recommendation.recommendation import Recommendation

# Initialize quart app instance and set secret key
app = Quart(__name__)
app.config['QUART_AUTH_SECRET_KEY'] = secret_key

# Matching mnodule with specific gui2string configuration
gui2string_recommendation = GUI2String()
recommendation_prototype = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                          prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE)

gui2string_recommendation = GUI2String()
recommendation_prototype_text = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                               prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT)

gui2string_recommendation = GUI2String()
recommendation_prototype_text_v2 = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                               prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_PROTOTYPE_TEXT_V2)

gui2string_recommendation = GUI2String()
recommendation_no_prototype = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                             prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE)

gui2string_recommendation = GUI2String()
recommendation_no_prototype_text = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                                  prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_NO_PROTOTYPE_TEXT)

gui2string_recommendation = GUI2String()
recommendation_using_feature_list = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                                  prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1)

gui2string_recommendation = GUI2String()
recommendation_using_feature_list_two_stage = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                                  prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_LIST_1)

gui2string_recommendation = GUI2String()
recommendation_feature_variants_obj = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation,
                                                     prompt_template=ZS_TEMPLATE_SINGLE_RECOMMENDATION_FEATURE_VARIANTS_1)

gui2string_recommendation = GUI2String()
recommendation_feature_variants_two_stage = Recommendation(openai_client=openai_client, gui2string=gui2string_recommendation)

# Matching mnodule with specific gui2string configuration
gui2string_generation = GUI2String()
generation = Generation(openai_client=openai_client, gui2string=gui2string_recommendation)

gui2string_feature_generation = GUI2String()
generation_features = Generation(openai_client=openai_client, gui2string=gui2string_feature_generation,
                                prompt_template=ZS_TEMPLATE_FEATURE_GENERATION_1)

gui2string_feature_generation = GUI2String()
generation_features_v2 = Generation(openai_client=openai_client, gui2string=gui2string_feature_generation,
                                prompt_template=ZS_TEMPLATE_FEATURE_GENERATION_2)


@app.route('/interlinking/v1/recommendation_prototype', methods=['POST'])
@requires_auth
async def interlinking_recommendation_prototype():
    data = await request.get_json()
    # Check for main attributes
    prototype_response = create_missing_attribute_response(json_data=data, field_name="prototype")
    if prototype_response:
        return prototype_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    prototype = data['prototype']
    user_stories = data['user_stories']
    response = await recommendation_prototype.recommendation_prototype(prototype=prototype, user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v1/recommendation_prototype_text', methods=['POST'])
@requires_auth
async def interlinking_recommendation_prototype_text():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    prototype_response = create_missing_attribute_response(json_data=data, field_name="prototype")
    if prototype_response:
        return prototype_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    text = data['text']
    prototype = data['prototype']
    user_stories = data['user_stories']
    response = await recommendation_prototype_text.recommendation_prototype_text(text=text, prototype=prototype, user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v2/recommendation_prototype_text', methods=['POST'])
@requires_auth
async def interlinking_recommendation_prototype_text_v2():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    prototype_response = create_missing_attribute_response(json_data=data, field_name="prototype")
    if prototype_response:
        return prototype_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    text = data['text']
    prototype = data['prototype']
    user_stories = data['user_stories']
    response = await recommendation_prototype_text_v2.recommendation_prototype_text(text=text, prototype=prototype, user_stories=user_stories)
    return jsonify(response)

@app.route('/interlinking/v1/recommendation_no_prototype', methods=['POST'])
@requires_auth
async def interlinking_recommendation_no_prototype():
    data = await request.get_json()
    # Check for main attributes
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    user_stories = data['user_stories']
    response = await recommendation_no_prototype.recommendation_no_prototype(user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v1/recommendation_no_prototype_text', methods=['POST'])
@requires_auth
async def interlinking_recommendation_no_prototype_text():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    text = data['text']
    user_stories = data['user_stories']
    response = await recommendation_no_prototype_text.recommendation_no_prototype_text(text=text, user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v1/us_generation_full', methods=['POST'])
@requires_auth
async def us_generation_full():
    data = await request.get_json()
    # Check for main attributes
    prototype_response = create_missing_attribute_response(json_data=data, field_name="prototype")
    if prototype_response:
        return prototype_response
    prototype = data['prototype']
    response = await generation.generation_entire_gui(prototype=prototype)
    return jsonify(response)


@app.route('/interlinking/v1/feature_generation', methods=['POST'])
@requires_auth
async def feature_generation():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    text = data['text']
    response = await generation_features.feature_generation_1(text=text)
    return jsonify(response)


@app.route('/interlinking/v2/feature_generation', methods=['POST'])
@requires_auth
async def feature_generation_v2():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    text = data['text']
    response = await generation_features_v2.feature_generation_1(text=text)
    return jsonify(response)


@app.route('/interlinking/v1/recommendation_using_feature_list', methods=['POST'])
@requires_auth
async def recommendation_using_feature_list_endpoint():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    text = data['text']
    user_stories = data['user_stories']
    response = await recommendation_using_feature_list.recommendation_using_feature_list_1(text=text, user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v2/recommendation_using_feature_list', methods=['POST'])
@requires_auth
async def recommendation_using_feature_list_two_stage_endpoint():
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_stories")
    if user_story_response:
        return user_story_response
    text = data['text']
    user_stories = data['user_stories']
    response = await recommendation_using_feature_list_two_stage.recommendation_using_feature_list_two_stage(text=text, user_stories=user_stories)
    return jsonify(response)


@app.route('/interlinking/v1/recommendation_feature_variants', methods=['POST'])
@requires_auth
async def recommendation_feature_variants():
    NUM_VARIANTS = 3
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_story")
    if user_story_response:
        return user_story_response
    text = data['text']
    user_story = data['user_story']
    response = await recommendation_feature_variants_obj.recommendation_feature_variants_1(num_variants=NUM_VARIANTS,
                                                                                           text=text, user_story=user_story)
    return jsonify(response)


@app.route('/interlinking/v2/recommendation_feature_variants', methods=['POST'])
@requires_auth
async def recommendation_feature_variants_two_stage_endpoint():
    NUM_VARIANTS = 3
    data = await request.get_json()
    # Check for main attributes
    text_response = create_missing_attribute_response(json_data=data, field_name="text")
    if text_response:
        return text_response
    user_story_response = create_missing_attribute_response(json_data=data, field_name="user_story")
    if user_story_response:
        return user_story_response
    text = data['text']
    user_story = data['user_story']
    response = await recommendation_feature_variants_two_stage.recommendation_feature_variants_two_stage(num_variants=NUM_VARIANTS,
                                                                                                         text=text, user_story=user_story)
    return jsonify(response)

def create_missing_attribute_response(json_data: json, field_name: str) -> json:
    if not json_data.get(field_name):
        return jsonify({
            "error": "Invalid request",
            "message": "The {} field is missing.".format(field_name)
        }), 400
    return None

if __name__ == "__main__":
    app.run()