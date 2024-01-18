import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

#Function to open steam listing's page
def open_listing(driver, url):
    while(1):
        driver.get(url)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "market_title_text")))
        try:
            error_message_locator = driver.find_element(By.XPATH, "//h3[text()='You\'ve made too many requests recently. Please wait and try your request again later.']")
            print("Requests error. Change IP/Proxy")
            sys.exit()
        except:
            try:
                error_div = driver.find_element(By.XPATH, "//div[contains(@class, 'market_listing_table_message') and contains(text(), 'There was an error getting listings for this item. Please try again later.')]")
                print("Error message found. Reloading the page")
                time.sleep(1)
                driver.get(url)

            except:
                try:
                    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "market_listing_header_namespacer")))
                    print("Page loaded")
                except:
                    continue
                break

#Function to parse through available listings and buy certain float item
def find_item(driver, url, float_cap, purchased_float_list):
    #display 100 listings instead of 10 (only works in SIH)
    action_chains = ActionChains(driver)
    dropdown_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[id^="ui-id-"][id$="-button"]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)
    action_chains.move_to_element(dropdown_element).click().perform()
    options_locator = (By.CSS_SELECTOR, '[id^="ui-id-"][id$="-menu"] li')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(options_locator))
    options = driver.find_elements(*options_locator)
    options[3].click()
    time.sleep(5)

    outer_div = driver.find_element(By.ID, "searchResultsRows")
    inner_divs = outer_div.find_elements(By.XPATH, ".//div[contains(@class, 'market_listing_row') and starts-with(@id, 'listing_')]")
    current_float_list=[]

    for inner_div in inner_divs:
        #Code to work with CSFloat extension
        #WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, ".//csfloat-item-row-wrapper")))
        #try:
            #csfloat_info=inner_div.find_element(By.XPATH, ".//csfloat-item-row-wrapper")
        #except StaleElementReferenceException:
            #csfloat_info=WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, ".//csfloat-item-row-wrapper")))
        #if(csfloat_info.text[0:7]!="Loading"):
            #item_float=float(csfloat_info.text[7:20])
        try:
            sih_info = WebDriverWait(inner_div, 10).until(EC.visibility_of_element_located((By.XPATH, ".//span[@class='value']")))
        except:
            print("Failed to get sih info")
            # break
        if sih_info.text:
            try:
                item_float=float(sih_info.text)
                print(item_float)
                current_float_list.append(item_float)
                # Buy listing with appropriate float
                if(item_float<float_cap and item_float not in purchased_float_list):
                    try:
                        button = inner_div.find_element(By.CLASS_NAME, "item_market_action_button.btn_green_white_innerfade.btn_small")
                        button.click()
                        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "market_buynow_dialog_accept_ssa")))
                        checkbox = driver.find_element(By.ID, "market_buynow_dialog_accept_ssa")
                        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox) #JavaScript code to sroll down to checkbox
                        if not checkbox.is_selected():
                            # action_chains.move_to_element(checkbox).click().perform()
                            checkbox.click()
                        #time.sleep(0.01)
                        button = driver.find_element(By.ID, "market_buynow_dialog_purchase")
                        button.click()
                        purchased_float_list.append(item_float)
                        break
                    except:
                        print("Buy error")
                        break
            except:
                print("Failed to convert to float")
        else:
            print("Failed to get sih info") 
    #Information block
    
    print("Items parsed: "+str(len(current_float_list)))
    try:
        print("Min float: "+str(min(current_float_list)))
        print("Max float: "+str(max(current_float_list)))
    except:
        print()

#Function to open steam and login into account
def steam_login(driver, login, password):
    driver.get("https://steamcommunity.com/login/home/?goto=market%2F")
    time.sleep(10)
    try:
        button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "acceptAllButton")))
        button.click()
    except:
        print()
    login_input = driver.find_element(By.XPATH, "//input[@type='text']")
    login_input.send_keys(login)
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)
    button = driver.find_element(By.XPATH, "//button[@type='submit']")
    button.click()
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "newlogindialog_EnterCodeInsteadLink_37AOB")))
    button.click()
    print("Enter your Steam Guard code: ")
    steam_guard_code = input() #2FA authentication
    segmented_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "segmentedinputs_SegmentedCharacterInput_3PDBF")))
    fields = segmented_input.find_elements(By.CLASS_NAME, "segmentedinputs_Input_HPSuA")
    for i in range(len(fields)):
        fields[i].send_keys(steam_guard_code[i])
    
    #select option to get float information by default (SIH extension)
    time.sleep(10)
    open_listing(driver, "https://steamcommunity.com/market/listings/730/P250%20%7C%20Metallic%20DDPAT%20%28Factory%20New%29")
    time.sleep(4)
    button = driver.find_element(By.CSS_SELECTOR, "label[for='auto_get_float_and_sticker_wear']")
    button.click()
