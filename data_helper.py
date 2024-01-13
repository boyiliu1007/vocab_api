import pandas as pd

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