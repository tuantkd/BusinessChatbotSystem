import json
import re
import unicodedata
from unidecode import unidecode
from difflib import get_close_matches
from typing import List, Dict, Union

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

def get_closest_step(input_text: str, steps: List[Dict[str, Union[int, str]]], threshold: float = 0.5) -> Union[Dict[str, Union[int, str]], None]:
    """
    Trả về bước có tên gần giống nhất với văn bản đầu vào nếu độ khớp của nó vượt qua ngưỡng cho trước, 
    ngược lại trả về None.
    
    Args:
    - input_text (str): Văn bản đầu vào.
    - steps (List[Dict[str, Union[int, str]]]): Danh sách các bước với tên và các thông tin liên quan.
    - threshold (float): Ngưỡng độ khớp tối thiểu để xem xét một bước là phù hợp (mặc định là 0.5).
    
    Returns:
    - (Dict[str, Union[int, str]] | None): Bước có tên gần giống nhất với độ khớp vượt qua ngưỡng, 
      hoặc None nếu không tìm thấy bước nào phù hợp.
    """
    step_names = [step['step_name'] for step in steps]
    closest_match = get_close_matches(input_text, step_names, n=1, cutoff=threshold)
    
    if closest_match:
        closest_step = next(step for step in steps if step['step_name'] == closest_match[0])
        return closest_step
    
    return None

def get_closest_activity(input_text: str, activities: List[Dict[str, Union[int, str]]], threshold: float = 0.5) -> Union[Dict[str, Union[int, str]], None]:
    """
    Trả về ngành nghề có tên gần giống nhất với văn bản đầu vào nếu độ khớp của nó vượt qua ngưỡng cho trước,
    ngược lại trả về None.

    Args:
    - input_text (str): Văn bản đầu vào.
    - activities (List[Dict[str, Union[int, str]]]): Danh sách các ngành nghề với tên và các thông tin liên quan.
    - threshold (float): Ngưỡng độ khớp tối thiểu để xem xét một ngành nghề là phù hợp (mặc định là 0.5).

    Returns:
    - (Dict[str, Union[int, str]] | None): Ngành nghề có tên gần giống nhất với độ khớp vượt qua ngưỡng,
      hoặc None nếu không tìm thấy ngành nghề nào phù hợp.
    """
    activity_names = [activity['activity_name'] for activity in activities]
    closest_match = get_close_matches(input_text, activity_names, n=1, cutoff=threshold)
    
    if closest_match:
        closest_activity = next(activity for activity in activities if activity['activity_name'] == closest_match[0])
        return closest_activity
    
    return None

def get_first_level_code(industry: dict) -> Union[str, None]:
    """
    Trả về mã số level đầu tiên của ngành nghề nếu có (xét từ level 1 đến level 5).
    Nếu không tìm thấy level nào, trả về None.

    Args:
    - industry (dict): Object ngành nghề chứa thông tin các level.

    Returns:
    - str | None: Mã số level đầu tiên hoặc None nếu không tìm thấy level nào.
    """
    if 'level1' in industry and industry['level1']:
        return industry['level1']
    elif 'level2' in industry and industry['level2']:
        return industry['level2']
    elif 'level3' in industry and industry['level3']:
        return industry['level3']
    elif 'level4' in industry and industry['level4']:
        return industry['level4']
    elif 'level5' in industry and industry['level5']:
        return industry['level5']
    else:
        return None