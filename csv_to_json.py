import csv
import json
import re

INPUT_FILE = './data/GRE_vocab.csv'
OUTPUT_FILE = './data/word.json'

# Convert CSV to JSON
data = []
with open(INPUT_FILE, 'r', encoding="utf-8") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        pos = row['pos']

        # Matches all parts of speech
        pattern = re.compile(r'([a-zA-Z]+\.)') 
        matches = pattern.findall(pos)
        added_pos = set()
        for match in matches:
            if match in added_pos:
                continue
            data.append({
                **row,
                'pos': match if match != 'a.' else 'adj.'
            })
            added_pos.add(match)

# Save to JSON
with open(OUTPUT_FILE, 'w') as jsonfile:
    json.dump(data, jsonfile, indent=2)

print(f'Conversion complete. Saved to {OUTPUT_FILE}')