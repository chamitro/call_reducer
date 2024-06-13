import re
import sys

def count_words_excluding_comments(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove single-line comments
    content_no_single_line_comments = re.sub(r'//.*', '', content)

    # Remove multi-line comments
    content_no_comments = re.sub(r'/\*.*?\*/', '', content_no_single_line_comments, flags=re.DOTALL)

    # Remove strings to avoid counting them as words
    content_no_strings = re.sub(r'".*?"|\'.*?\'', '', content_no_comments)

    # Split the remaining content into words based on whitespace and special characters
    words = re.findall(r'\b\w+\b', content_no_strings)

    return len(words)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)
    
    solidity_file_path = sys.argv[1]
    word_count = count_words_excluding_comments(solidity_file_path)
    print(f"Word count excluding comments: {word_count}")

