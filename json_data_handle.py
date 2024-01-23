import requests
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("Dictionary_API_key")
WORD_FILE = './data/word.json'
OUTPUT_FILE = './data/testOutput.json'
translation_of_ptos = {"n.": "noun", "adj.": "adjective", "adv.": "adverb", "v.": "verb"}

def get_res(word, ptos):
    try:
        API_URL = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            try:
                res = response.json()
                if res:
                    return res
                else:
                    print("No such word or pos")
                    return None
            except json.JSONDecodeError as json_error:
                print(f'Error decoding JSON: {json_error}')
                print(response.text)  # Print the response content
                return None
        else:
            print(f"Error in get_res: {response.status_code}")
            print(response.text)  # Print the error message or response content
            return None

    except Exception as e:
        print(f'Error in get_res: {e}')
        return None
    
#===================================================================================

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
            if key == "syns" or key == "uros":
                continue
            if key == target:
                searchlist.append(value)
            else:
                dfs_search(value, target, searchlist)

#===================================================================================
def escapeWord(sentence, wordList):
    patterns_to_remove = ['{wi}', '{/wi}', '{qword}', '{/qword}', '{it}', '{/it}']

    # Create a regular expression pattern by joining the patterns with the '|' (OR) operator
    pattern = '|'.join(re.escape(p) for p in patterns_to_remove)

    # Use re.sub() to replace matched patterns with an empty string
    result_string = re.sub(pattern, '', sentence)

    escaped_words = [re.escape(word) for word in wordList]
    
    # Join the escaped words with '|' (OR) for the regular expression pattern
    pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'

    # Use re.sub() to replace the matched words with underscores
    result_string = re.sub(pattern, '_____', result_string)

    return result_string

#===================================================================================

def is_var_int_format(variable, input_string):
    # Define a regular expression pattern for the desired format
    pattern = rf'^{re.escape(variable)}:\d+$'

    # Use re.match to check if the input string matches the pattern
    match = re.match(pattern, input_string)

    # If there is a match, return True; otherwise, return False
    return bool(match)

#===================================================================================

def get_one_example(word, data, ptos):
    example = ""

    for part in data:
        # If part['fl'] equals the desired part of speech
        if 'fl' in part:
            if part['fl'] == translation_of_ptos[ptos] or translation_of_ptos[ptos] in part['fl']:
                if part['meta']['id'] == word or is_var_int_format(word, part['meta']['id']):
                    stemList = []
                    dfs_search(part, "stems", stemList)
                    escapeWordList = stemList[0]
                    escapeWordList.append(word)

                    tmp = []
                    dfs_search(part, "t", tmp)

                    if tmp:
                        tmp = [s for s in tmp if len(s) <= 200]
                        if tmp:
                            sentence = max(tmp, key=len)
                        else:
                            return example

                        result = escapeWord(sentence, escapeWordList)
                        
                        # Find out the longest one
                        if len(result) > len(example):
                            example = result

    return example
#===================================================================================

def get_def(word, data, pos):
    definition = []
    for part in data:
        if 'fl' in part:
            if part['fl'] == translation_of_ptos[pos] or translation_of_ptos[pos] in part['fl']:
                if part['meta']['id'] == word or is_var_int_format(word, part['meta']['id']):
                    tmp = []
                    dfs_search(part, "shortdef", tmp)
                    definition.extend(tmp)
        else:
            print(word, "no fl label!")

    return definition

try:
    target = "catholic"
    endCount = 200
    startFlag = False
    target_index = 0
    with open(WORD_FILE, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        count = 0
        for item in data:
            word = item["word"]
            pos = item["pos"]
            defNoneFlag = False
            if item["word"] == target and startFlag == False:
                startFlag = True
            if count == endCount:
                break
            if startFlag:
                if pos in translation_of_ptos:
                    res = get_res(item["word"], item["pos"])
                    example = get_one_example(item["word"], res, item["pos"])
                    definition = get_def(item["word"], res, item["pos"])
                    if definition != [[]] and definition != []:
                        item["example"] = example
                        item["definition"] = definition
                    else:
                        defNoneFlag = True
                count += 1
            if defNoneFlag:
                print(f'delete {item["word"]}')
                data.remove(item)
            if not startFlag:
                target_index += 1

    data = data[target_index:target_index + count]
    try:
    # Read existing JSON data from the file
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)

        # Append new data to the existing list
        existing_data.extend(data)

        # Write the updated data back to the file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

        print("Data appended successfully.")

    except FileNotFoundError:
        print(f'File not found: {OUTPUT_FILE}')
    except json.JSONDecodeError as json_error:
        print(f'Error decoding existing JSON: {json_error}')
    except Exception as e:
        print(f"Error: {e}")

except FileNotFoundError:
    print(f'File not found: {WORD_FILE}')
except KeyError:
    print(f'Invalid part of speech! word: {word} pos: {pos}')
except Exception as e:
    print(f'Error in main: {e}')




