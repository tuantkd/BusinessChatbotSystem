import json
import re
import unicodedata
from unidecode import unidecode

def filter_duplicate_in_array(array):
  unique_values = []
  for value in array:
    if value not in unique_values:
      unique_values.append(value)
  return unique_values


def get_number_in_string(str_text):
  if str_text:
      numbers = re.findall(r'\d+', str_text)
      return numbers[0]
  return str_text


def compare_array_source_array_dest(array_source, array_dest):
  for value in array_source:
    if value in array_dest:
      return True
  return False


def normalize_text(text):
  text = unicodedata.normalize("NFD", text)
  text = "".join([c for c in text if not unicodedata.combining(c)])
  text = re.sub(r"\s+", " ", text).strip().lower()
  return text


def read_json_file(file_path):
  try:
      with open(file_path, 'r', encoding='utf-8') as f:
          return json.load(f)
  except FileNotFoundError as e:
      print(f"Error: File not found: {e}")
      return None
  except json.JSONDecodeError as e:
      print(f"Error: Invalid JSON data: {e}")
      return None


def convert_to_snake_case(text):
  normalized_text = unicodedata.normalize("NFD", text)
  table = str.maketrans(" ", "_")
  processed_text = normalized_text.translate(table)

  return processed_text


def get_json(file_path):
  try:
    with open(file_path, 'r', encoding='utf-8') as json_file:
      data = json.load(json_file)
      return data
  except FileNotFoundError:
      print(f"File not found: {file_path}")
  except json.JSONDecodeError:
      print(f"Error decoding JSON in file: {file_path}")
  except Exception as e:
      print(f"An error occurred: {e}")
      

def cleaned_text(original_text):
  return re.sub(r'[^a-zA-Z0-9\s]', '', original_text)


def get_key_business_type(business_type_name, dictionaries):
  for dictionary in dictionaries:
    values = [remove_vietnamese_accents(value.strip().lower()) for value in dictionary['values']]
    text = remove_vietnamese_accents(business_type_name.strip().lower())
    found = find_text_in_list(text, values)
    if found:
      return dictionary['key']
  
  return business_type_name


def remove_vietnamese_accents(input_str):
    return unidecode(input_str)
  

def find_text_in_list(text_to_find, list_of_strings):
  for string in enumerate(list_of_strings):
    if text_to_find in string:
      return True
  return False