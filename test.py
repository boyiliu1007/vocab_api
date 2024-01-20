import re

def escape_words(words, input_string):
    escaped_words = [re.escape(word) for word in words]
    
    # Join the escaped words with '|' (OR) for the regular expression pattern
    pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'

    # Use re.sub() to replace the matched words with underscores
    result_string = re.sub(pattern, '_____', input_string)

    return result_string

# Example usage
words_to_escape = ['word1', 'word2', 'word3']
input_string = "This is a sentence with word1, word2, and word3."

output_string = escape_words(words_to_escape, input_string)

print("Original string:", input_string)
print("String after replacement:", output_string)