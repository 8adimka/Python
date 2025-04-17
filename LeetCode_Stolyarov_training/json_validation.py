import json

def json_validation(input_json):
    try:
        data = json.loads(input_json)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    def validate_element(el):
        if isinstance(el, dict):
            for key, value in el.items():
                if not isinstance(key, str):
                    return False
                if not validate_element(value):
                    return False
        elif isinstance(el, list):
            for item in el:
                if not validate_element(item):
                    return False
        elif not isinstance(el, (str, int, float, bool, type(None))):
            return False
        return True

    if validate_element(data):
        return True, "Valid JSON"
    else:
        return False, "Invalid structure or unsupported types"

