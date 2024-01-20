import re

def is_var_int_format(variable, input_string):
    # Define a regular expression pattern for the desired format
    pattern = rf'^{re.escape(variable)}:\d+$'

    # Use re.match to check if the input string matches the pattern
    match = re.match(pattern, input_string)

    # If there is a match, return True; otherwise, return False
    return bool(match)

input_string = "aberration"
print(is_var_int_format("aberration", input_string))