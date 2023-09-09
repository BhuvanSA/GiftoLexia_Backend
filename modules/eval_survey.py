# Function for age group 3-5 and return result
def eval_agegroup1(data, threshold):
    option_scores = {
        1: 1,
        2: 3,
        3: 5}
    score = 0
    # for item in data['survey']:
    for item, index in enumerate(data['selectedOptions']):
        # score = score + option_scores[item["option_id"]]
        score = score + option_scores[item[str(int(index)+1)]]
    result = {
        "score": score,
        "action": "ok" if score < threshold else "cta",
        "msg": "Score has crossed the threshold value contact us immediately"}
    return result

# Function for age group 5-8 and return result


def eval_agegroup2(data, threshold):
    option_scores = {
        1: 1,
        2: 3,
        3: 5}
    score = 0
    for item, index in enumerate(data['selectedOptions']):
        score = score + option_scores[item[str(int(index)+1)]]
    result = {
        "score": score,
        "action": "ok" if score < threshold else "cta",
        "msg": ""}
    return result

# Function for age group 8-12 and return result


def eval_agegroup3(data, threshold):
    option_scores = {
        1: 1,
        2: 3,
        3: 5}
    score = 0
    # for item in data['survey']:
    for item, index in enumerate(data['selectedOptions']):
        # score = score + option_scores[item["option_id"]]
        score = score + option_scores[item[int(index)+1]]
    result = {
        "score": score,
        "action": "ok" if score < threshold else "cta",
        "msg": ""}
    return result

# Prepare the message to be displayed to the user after the score has been calculated
#


def get_eval_message(data, result):
    lang_code = data["language_code"]
    age_group = data["age_group"]
    msg = ""

    if result["action"] == "ok":
        msg = get_ok_message(lang_code)

    if result["action"] == "cta":
        msg = get_cta_message(lang_code)

    return msg


def get_ok_message(lang_code):
    return "Based on your responses, your child is not at risk. If you have any questions, please contact us."


def get_cta_message(lang_code):
    return "Based on your responses, your childs score is above 90. We recommend that you seek professional guidance. If you have any questions, please contact us. "
