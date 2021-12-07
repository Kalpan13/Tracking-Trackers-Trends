"""
Author : Swetang Finviya
"""
from adblockparser import AdblockRules
import json
from haralyzer import HarParser
import pandas as pd
from tqdm import tqdm
import os

tracker_file_name = 'easyprivacy.txt'
adblock_filter_rules_file = open(f"./tracker_lists/{tracker_file_name}", 'r')
year = '2014'
line = adblock_filter_rules_file.readline()
raw_rules = []

# Parse the tracker list
while line:
    if(line[0]!='!'):
        raw_rules.append(line)
    line = adblock_filter_rules_file.readline()

adblock_filter_rules_file.close()
rules = AdblockRules(raw_rules)

"""
Create a folder of each year containing all the HARs files
|_2014
|_2015
|...
"""
HAR_files = os.listdir(year)
result_dataframe = pd.DataFrame()

# Parse HAR file and extract URL details
for HAR_file in tqdm(HAR_files):

    with open(year + '/'+ HAR_file, 'r', encoding="utf8") as file:
        har_parser = HarParser(json.loads(file.read()))

    page_load_info = har_parser.har_data
    
    total_matches = 0
    current_row = {}
    current_row['Website'] = HAR_file

    for http_request in page_load_info['entries']:
        anti_adblocker_found = rules.should_block(http_request['request']['url'])
        if(anti_adblocker_found):
            total_matches = total_matches + 1
    
    current_row['Tracking_Requests_Count'] = total_matches
    result_dataframe = result_dataframe.append(current_row, ignore_index=True)

result_dataframe.to_csv("./trends/year" + '-' + tracker_file_name + '.csv')               
