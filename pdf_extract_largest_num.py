import os
from PyPDF2 import PdfReader

curr_path = os.getcwd()
filename = "FY25 Air Force Working Capital Fund.pdf"
file_path = os.path.join(curr_path, filename)

def check_file():
    if not os.path.isfile(file_path):
        print("File Does Not Exist")
        raise FileNotFoundError

try:
    check_file()
except Exception as e:
    print(f"Exception {e}.")

file = open(file_path, "rb")
pdf = PdfReader(file)
max_pgs = len(pdf.pages)
ret_str = '1' # Largest number in string format
ret_num = float(ret_str) # Largest number

def check_string(string):
    curr_num_str = ''
    contains_period = False
    contains_minus = False
    for char in string:
        # Do not add ',' because if it is attached to a number, that will interfere with converting it into a float later
        if char >= '0' and char <= '9':
            curr_num_str += char
        elif char == '.' and curr_num_str != '': # Keep '.' in case they are part of numbers
            curr_num_str += char
            contains_period = True
        elif char == '-' and curr_num_str == '': # "-..." could be a negative number -> keep '-' for now
            curr_num_str += char
            contains_minus = True
        elif char != ',' and char >= '!' and char <= '~' and curr_num_str != '':
            # If char is not part of a number (,) but is anything else that comes after valid numbers, process valid number string first
            # eg. 2022-...-2024 or 2022...abc...2024 or 2022...)...2024 -> read all numbers separately
            # Unwanted character(s) mixed with numbers. Need to split string more
            check_string(curr_num_str)
            curr_num_str = '' # Reset curr_num_str to look at rest of string
            # Don't adjust contains_minus because while we are not adding the minus char to the string, we don't know if there was a minus sign at the front

    if curr_num_str != '': # After cleaning curr_num_str, if not empty check to convert to number
        if contains_period:
            if curr_num_str[-1] == '.': # Check if last char is period or not. If so, remove char
                # Could be number with a period at the end (eg. "2025.0.")
                curr_num_str = curr_num_str[:-1]
            if len(curr_num_str.split('.')) > 2: # Possible version number (eg. 2.2.0) - disregard
                return
        
        if contains_minus:
            minus_strings = curr_num_str.split('-')
            minus_substr_count = len(minus_strings)
            if minus_substr_count == 2 and minus_strings[0] == '' and minus_strings[1] != '':
                # First split substring is empty but not the second one - second half is a negative number
                curr_num_str = '-' + minus_strings[1]
        
        if curr_num_str != '-':
            num_float = float(curr_num_str)
            global ret_str
            global ret_num
            if num_float > ret_num: # Check to replace largest number
                ret_num = num_float
                ret_str = "{:,}".format(ret_num) # Need to include ',' to keep all numbers consistent when checking

def preprocess_by_type(num_string_input):
    # Input parameter could be a word (str) or a list of words (list[str]), like when reading y-axes of tables
    in_type = type(num_string_input)
    if in_type is str:
        check_string(num_string_input)
    elif in_type is list: # If list, read every string from list
        for list_string in num_string_input:
            check_string(list_string)

for page_num in range(max_pgs): # For every page in PDF document
    curr_page = pdf.pages[page_num] # Find current page
    line = curr_page.extract_text().split() # Extract text from page, then refine line

    for word in line: # For every line of text from page
        # Possible that string contains $#..$#.. because reading table y-axes -> process several numbers together
        # Could add other cases here for different types of units on table y-axes
        if '$' in word:
            word = word.split('$')
            for subword in word:
                preprocess_by_type(subword)
        else:
            preprocess_by_type(word)

print("Largest Number:", ret_str)