import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steam_functions import open_listing, find_item
import time
import sys

#loading item float extension
service = Service()
option = webdriver.ChromeOptions()
option.add_extension("sih.crx")
#option.add_extension("float.crx")
driver = webdriver.Chrome(service=service, options=option)

#openning steam website and waiting for login (to be automatized)
url = "https://steamcommunity.com/market/"
driver.get(url)
print("Please manually login to Steam and press Enter")
input()

# url input
# print("Enter link to Steam listing: ")
# url_input=input()
# url_list=[]
# url_list.append(url_input)

#preset
url_list=["https://steamcommunity.com/market/listings/730/P250%20%7C%20Metallic%20DDPAT%20%28Factory%20New%29", #P250 Metallic DDPAT
          "https://steamcommunity.com/market/listings/730/MAG-7%20%7C%20Metallic%20DDPAT%20%28Factory%20New%29"] #MAG-7 Metallic DDPAT

#float cap input
print("Enter float cap: ")
float_cap=float(input())

#input delay between tries
print("Enter delay between tries: ")
try_delay=int(input())

#Main
while(1):
    for url in url_list:
        try:
            open_listing(driver, url)
        except:
            print("Requests error") 
            #Requests error means Steam has temporarily blocked current IP address (it is necessary to involve proxy servers in future versions to resolve)
            sys.exit() 
        try:
            find_item(driver, url, float_cap)
        except:
            print("Find/Buy error")
            continue
        time.sleep(try_delay)