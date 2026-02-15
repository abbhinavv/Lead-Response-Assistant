def validate_response(response_text):
    forbidden_phrases = [
        "guarantee",
        "definitely caused by",
        "we assure",
        "this will permanently fix",
        "certainly structural failure"
    ]

    for phrase in forbidden_phrases:
        if phrase in response_text.lower():
            return False

    return True
