import re

translation_of_ptos = {"n.": "noun", "adj.": "adjective", "adv.": "adverb", "v.": "verb"}

def get_one_example(word, data, ptos):
    example = ""

    for part in data:
        # If part['fl'] equals the desired part of speech
        if part['fl'] == translation_of_ptos[ptos]:
            tmp = []
            dfs_search(part, "t", tmp)

            if tmp:
                tmp = [s for s in tmp if len(s) <= 200]
                sentence = max(tmp, key=len)

                patterns_to_remove = ['{wi}', '{/wi}', '{qword}', '{/qword}', '{it}', '{/it}']

                # Create a regular expression pattern by joining the patterns with the '|' (OR) operator
                pattern = '|'.join(re.escape(p) for p in patterns_to_remove)

                # Use re.sub() to replace matched patterns with an empty string
                result_string = re.sub(pattern, '', sentence)

                escaped_word = re.escape(word)

                # Create a regular expression pattern to match the word
                pattern = r'\b' + escaped_word + r'\b'

                # Use re.sub() to replace the matched word with underscores
                result = re.sub(pattern, '_____', result_string)

                # Find out the longest one
                if len(result) > len(example):
                    example = result

    return example

def dfs_search(json_data, target, searchlist):
    # If it is a list
    if isinstance(json_data, list):

        findFlag = False
        for item in json_data:

            # If found target before, add the next element to the list
            if findFlag:
                searchlist.append(item)
            
            if item == target:
                findFlag = True
            else:
                dfs_search(item, target, searchlist)

    # If it is a dictionary
    elif isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == "syns":
                continue
            if key == target:
                searchlist.append(value)
            else:
                dfs_search(value, target, searchlist)