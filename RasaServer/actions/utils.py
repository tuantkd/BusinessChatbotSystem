import json
import re
import unicodedata

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
