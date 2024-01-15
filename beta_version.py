import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steam_functions import open_listing, find_item
import time
import sys
import pandas

#loading item float extension
service = Service()
option = webdriver.ChromeOptions()
option.add_extension("sih.crx")
#option.add_extension("float.crx")

#enter proxy (recommended to use rotatiing proxy)
print("Enter proxy IP (0 if no proxy): ")
proxy_ip = input()
if not proxy_ip:
    print("Enter proxy port")
    proxy_port=input()
    option.add_argument(f'--proxy-server={proxy_ip}:{proxy_port}')

driver = webdriver.Chrome(service=service, options=option)

#openning steam website and waiting for login (to be automatized)
url = "https://steamcommunity.com/market/"
driver.get(url)
print("Please manually login to Steam and press Enter")
input()

file = pandas.read_excel("Skins.xlsx") # if no pages are specified, then the last one saved is open
skins_list = file.values.tolist()
print(skins_list)

#input delay between tries
print("Enter delay between tries: ")
try_delay=int(input())

#Main
while(1):
    for line in skins_list:
        
        name = line[0]
        url = line[1]
        float_cap = line[2]
        #pattern = line[3] #it is possible to search for listing with desired pattern if necessary (need to adjust steam_functions)

        open_listing(driver, url)
        find_item(driver, url, float_cap)
        time.sleep(try_delay)