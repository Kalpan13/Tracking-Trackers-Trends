from selenium import webdriver
from browsermobproxy import Server
import time
import json
import pandas as pd
from tqdm import tqdm
import warnings
import re
import os
warnings.filterwarnings("ignore", category=DeprecationWarning) 

if "BROWSERMOB_PROXY_PATH" not in os.environ:
    BROWSERMOB_PROXY_PATH="browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy"
else:
    BROWSERMOB_PROXY_PATH = os.environ['BROWSERMOB_PROXY_PATH']

def get_har_file_name(website : str):
    """Get the name of the HAR file

    Args:
        website (str): website URL

    Returns:
        str : name of the file
    """
    # Extract timestamp from URL
    timestamps_indices = [(m.start(0), m.end(0)) for m in re.finditer('[0-9]{14}', website)]
    timestamp_indices = timestamps_indices[0]
    timestamp = website[timestamp_indices[0]:timestamp_indices[1]]
    
    # Extract website name from URL
    website_name = website[timestamp_indices[1]+1:]

    if website_name[-1]=='/':
        website_name = website_name[:-1]
    website_name = website_name[website_name.find('//')+2:]
    
    filename = website_name + "-" + timestamp
    return filename

def create_proxy_server():
    """To create Proxy Server
    """

    # Path to Browsermob-proxy
    global BROWSERMOB_PROXY_PATH
    path = BROWSERMOB_PROXY_PATH
    server = Server(path, options={'port': 8090})
    server.start()
    # Create proxy server
    proxy = server.create_proxy(params={"trustAllServers": "true"})
    return proxy, server

def capture_har(website, proxy, server):
    """To Capture HAR files

    Args:
        website (str): Website URL
        proxy : Proxy Object
        server : Server object
    """
    options = webdriver.ChromeOptions()
    
    # Chrome Options for selenium
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--proxy-server={0}".format(proxy.proxy))
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("start-maximized") # https:#stackoverflow.com/a/26283818/1689770
    options.add_argument("enable-automation") # https:#stackoverflow.com/a/43840128/1689770
    options.add_argument("--headless") # only if you are ACTUALLY running headless
    options.add_argument("--no-sandbox") #https:#stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-infobars") #https:#stackoverflow.com/a/43840128/1689770
    options.add_argument("--disable-dev-shm-usage") #https:#stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-browser-side-navigation") #https:#stackoverflow.com/a/49123152/1689770
    options.add_argument("--disable-gpu") #https:#stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

    driver = webdriver.Chrome(chrome_options = options)

    # Create a new HAR file
    proxy.new_har(website)

    driver.get(website)
    time.sleep(3)
    
    # Write captured details to HAR file
    with open(f"./captured_hars/{get_har_file_name(website)}.har","w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))

    print("Quitting Selenium WebDriver")
    driver.quit()

if __name__ == '__main__':

    # Read the csv containing Wayback URLs
    df = pd.read_csv('Wayback-data.csv')
    df = df.dropna()
    websites = list(df['resp_url'])

    # Creating a proxy server to capture network traffic
    proxy, server = create_proxy_server()
    error_list = []
    for website in tqdm(websites):
        try:
            print("Trying : {}".format(website))
            capture_har(website, proxy, server)
        except Exception as e:
            print(e)
            error_list.append(website)

    
    