from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os 
import random


def createBrowserScript(payload, driver):

	all_lines = []
	cardInfo = []
	for k, v in payload.items():
		if k == "bd" or k == "bm" or k == "by":
			all_lines.append("document.querySelector('select[name=\"" + k + "\"]').selectedIndex = '" + v +"';\n")
		elif k == "country":
			all_lines.append("document.querySelector('select[name=\"" + k + "\"]').selectedIndex = '105' ;\n")
		elif k == "paymentForm:j_id_16_4:creditCardNumber" or k == "paymentForm:j_id_16_4:creditCardHolderName":
			cardInfo.append("document.getElementsByName('" + k + "')[0].value = '" + v + "';\n")
		elif k == "paymentForm:j_id_16_4:creditCardExpirationMonth" or k == "paymentForm:j_id_16_4:creditCardExpirationYear":
			cardInfo.append("document.querySelector(\'select[id=\"" + k + "\"]\').value = '" + v + "';\n")
		else:
			all_lines.append("document.getElementsByName('" + k + "')[0].value = '" + v + "';\n")
						
	commands = ";".join(all_lines)
	driver.execute_script(commands)
	driver.execute_script("window.scrollTo(0,700)")
	driver.find_element_by_xpath('//*[@id="contents"]/form/p[2]/input').click()

	#Confirm step
	driver.execute_script("window.scrollTo(0,500)")
	driver.find_element_by_xpath('//*[@id="regist3Form"]/p[2]/input').click()
					
	#Continue
	driver.find_element_by_xpath('//*[@id="contents"]/form/p/input').click()

	#Checkout
	driver.find_element_by_xpath('//*[@id="shippingForm:j_id_11:cart_next"]').click()

	#Checkout
	cardInfoScript = ';'.join(cardInfo)
	driver.execute_script(cardInfoScript)
	driver.execute_script("window.scrollTo(0,300)")
	#driver.find_element_by_xpath('//*[@id="paymentForm:cart_next"]').click()

def start(website):

	dirname = os.path.dirname(os.path.abspath(__file__))
	chromedriver = os.path.join(dirname,"chromedriver.exe")
	driver = webdriver.Chrome(chromedriver)
	driver.get(website)

	#wait
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "add-to-cart"))) 
	driver.execute_script("window.scrollTo(0,500)")

	#add to cart
	driver.find_element_by_xpath('//*[@id="add-to-cart"]').click()

	#Proceed to checkout
	driver.find_element_by_xpath('//*[@id="cartView:cartForm_298616:proceed_checkout_298616"]').click()

	#Register
	driver.find_element_by_xpath('//*[@id="j_id_v:j_id_1p:registerAsRakutenMember"]/a').click()


	f = open("zipcode.txt", "r")
	
	if f.mode == "r":
		content = f.readlines()
		bd = str(random.randint(1,30))
		bm = str(random.randint(1,12))
		by = str(random.randint(70,100))
		tel = "0" + str(random.randint(100000000,999999999))
	
		for each in content:
			listOfItems = each.split(',')
			payload = {
				"email" :listOfItems[0],
				"email2" : listOfItems[0],
				"p": listOfItems[1],
				"fname" : listOfItems[2],
				"lname" : listOfItems[3],
				"bd":bd, 
				"bm":bm,
				"by":by,
				"country": "japan", 
				"street": listOfItems[4],
				"city" : listOfItems[5], 
				"prefecture": listOfItems[6],
				"zip.values": listOfItems[7],
				"tel.values" : tel,
				"paymentForm:j_id_16_4:creditCardNumber": listOfItems[8],
				"paymentForm:j_id_16_4:creditCardExpirationMonth" : listOfItems[9],
				"paymentForm:j_id_16_4:creditCardExpirationYear" : listOfItems[10],
				"paymentForm:j_id_16_4:creditCardHolderName": listOfItems[11],
			}
			createBrowserScript(payload, driver)
		