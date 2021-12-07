# Extracts URLs from Wayback API 
import requests
import pandas as pd
from tqdm import tqdm

def get_timestamps(start : str , end : str):
    """Function to generate timestamps
    
    Args:
        start (str): Start date of timestamp.
        end (str): End date of timestamp.
    """
    dates = list(pd.date_range(start, end, freq='AS'))
    dates_formated = [str(date).split(" ")[0].replace("-",'') for date in dates]
    return dates_formated


if __name__ == '__main__':
    top_sites_df = pd.read_csv("top-1m.csv")  # CSV file containing top-1 million csv
    top_2000_websites = list(top_sites_df['website'])[:2000]
    timestamps = get_timestamps(start = '2014-01-01', end = '2021-01-01')

    df = pd.DataFrame()
    # Get Wayback URL for a each website for all timestamps
    for website in tqdm(top_2000_websites,desc=" outer", position=0):
        for timestamp in tqdm(timestamps, desc=" inner", position=1, leave=False):
            row = {}
            row["website"] = website
            row["req_timestamp"] = timestamp
            
            # GET Request website with timestamp
            response = requests.get(f"https://archive.org/wayback/available?url={website}&timestamp={timestamp}")
            try:
                response = response.json()
                if len(response["archived_snapshots"])>0:
                    response["archived_snapshots"]["closest"]["url"]
                    row["resp_timestamp"] = response["archived_snapshots"]["closest"]["timestamp"]
                    row["resp_url"] = response["archived_snapshots"]["closest"]["url"]
            except Exception as e:
                print(e)

            df = df.append(row,ignore_index = True)
    df.to_csv("Wayback-data.csv")        

