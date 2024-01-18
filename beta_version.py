import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steam_functions import open_listing, find_item, steam_login
import time
import sys
import pandas

#loading item float extension
service = Service()
option = webdriver.ChromeOptions()
option.add_extension("sih.crx")

#enter proxy (recommended to use rotatiing proxy)
print("Enter proxy IP (blank if no proxy): ")
proxy_ip = input()
if proxy_ip:
    print("Enter proxy port")
    proxy_port=input()
    option.add_argument(f'--proxy-server={proxy_ip}:{proxy_port}')


file = pandas.read_excel("Skins.xlsx")
skins_list = file.values.tolist()

#input delay between tries
print("Enter delay between tries: ")
try_delay=int(input())

#input desired ammount of bought items
print("Enter desired ammount of bought items: ")
bought_items_cap = int(input())

#Main
print("Enter Steam login: ")
login=input()
print("Enter Steam password: ")
password=input()

driver = webdriver.Chrome(service=service, options=option)

steam_login(driver, login, password)

purchased_float_list=[]

while len(purchased_float_list)<bought_items_cap:
    for line in skins_list:
        
        name = line[0]
        url = line[1]
        float_cap = float(line[2])
        #pattern = line[3] #it is possible to search for listing with desired pattern if necessary (need to adjust steam_functions)

        open_listing(driver, url)
        find_item(driver, url, float_cap, purchased_float_list)

        if len(purchased_float_list)>(bought_items_cap-1):
            break

        time.sleep(try_delay)

print("Total listings bought: " + str(bought_items_cap))
print("Purchased floats:", end=" ")
for item in purchased_float_list:
    print(item, end=", ")
