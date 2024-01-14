import re

translation_of_ptos = {"n.": "noun", "adj.": "adjective", "adv.": "adverb", "v.": "verb"}

def get_one_example(data, ptos):
    example = ""

    for part in data:
        # If part['fl'] equals the desired part of speech
        if part['fl'] == translation_of_ptos[ptos]:
            tmp = []
            dfs_search(part, "t", tmp)

            if tmp:
                # Delete strings that without a {/wi} in it 
                filtered_list = list(filter(lambda x: re.search(r'{/wi}', x), tmp))
                if filtered_list:
                    sentence = max(filtered_list, key=len)

                    # Define a regular expression pattern that replace 
                    # d ... {/wi} or f ... {/wi} or {wi} ... {/wi} with ___
                    pattern = re.compile(r'(\s[df]\s|{wi})(.*?){/wi}')
                    _string = pattern.sub(' ______', sentence)

                    # Find out the longest one
                    if len(_string) > len(example):
                        example = _string

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
            
            if key == target:
                searchlist.append(value)
            else:
                dfs_search(value, target, searchlist)