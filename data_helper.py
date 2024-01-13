import pandas as pd
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API key using the variable name defined in .env
api_key = os.getenv("Dictionary_API_key")

WORD_FILE = './data/word.json'

def get_random_words():
    try:
        with open(WORD_FILE, 'r', encoding="utf-8") as json_file:
            df = pd.read_json(json_file, orient='records')

            # Filter out words that are not v, adj, n and adv
            filtered_df = df[df['pos'].isin(['v.', 'adj.', 'n.', 'adv.'])]

            # Select a random part of speech
            random_word = filtered_df.sample(n=1)
            selected_pos = random_word['pos'].values[0]

            # Select 4 random words from the selected pos
            grouped_df = filtered_df.groupby('pos')

            if selected_pos in ['adj.', 'adv.']:
                selected_pos_df = pd.concat([
                    grouped_df.get_group('adj.'), 
                    grouped_df.get_group('adv.')
                ])
            else:
                selected_pos_df = grouped_df.get_group(selected_pos)

            random_words = selected_pos_df.sample(n=4)

            return random_words.to_dict(orient='records')
    except FileNotFoundError:
        print(f'File not found: {WORD_FILE}')
        return None
    except KeyError:
        print('Invalid part of speech: {pos}')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None
    
def get_example(word):
    try:
        API_URL = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'
        response = requests.get(API_URL)

        if response.status_code == 200:
            # Parse the response content (assuming it's JSON in this example)
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  # Print the error message or response content

    except Exception as e:
        print(f'Error: {e}')
        return None
        