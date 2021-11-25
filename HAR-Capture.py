from selenium import webdriver
from browsermobproxy import Server
import time
import json
import pandas as pd
from tqdm import tqdm

def create_proxy_server():
    path = "D:/SBU Projects/anti-adblocker-analysis/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

    server = Server(path, options={'port': 8090})
    server.start()
    proxy = server.create_proxy(params={"trustAllServers": "true"})
    return proxy, server

def capture_har(website):
    proxy, server = create_proxy_server()
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--proxy-server={0}".format(proxy.proxy))

    driver = webdriver.Chrome(chrome_options = options)

    proxy.new_har(website)

    driver.get(f"http://www.{website}")
    time.sleep(5)

    with open(f"./captured_hars/{website}.har","w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))

    print("Quitting Selenium WebDriver")
    server.stop()
    driver.quit()

df = pd.read_csv("top-1m.csv")
df = df.drop_duplicates(subset=["website"], keep='last')

websites = list(df['website'])
websites = websites[140:1001]

for website in tqdm(websites):
    if website in ['whatsapp.com', 'adobe.com']:
        continue
    print("Tryinhg : {}".format(website))
    capture_har(website)
    