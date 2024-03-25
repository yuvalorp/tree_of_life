# flake8: noqa

import logging
import os
import re

from src.data_table_cache import BaseCache, WikiPageCache, TableDataCache

logging.basicConfig(level=100)
# Specify the directory path

directory = r"C:\Users\yuval\projects\python\famely_tree\cache\person_info"

# Get all files in the directory
files = os.listdir(directory)

# Print the list of files
print("Files in directory:")
for file in files:
    print(file)

table_data_manager = TableDataCache()
data_dict = table_data_manager.get_or_load_resource("/wiki/Catherine_Middleton")
born = data_dict.get("Born", 1000000000000000)
if type(born) == list:
    born = born[0]
    pattern = "[0-9]{3,4}"
    match_results = re.search(pattern, born, re.IGNORECASE)
    if match_results is None:
        born = 2000
    else:
        born = int(match_results.group())
print(born)
