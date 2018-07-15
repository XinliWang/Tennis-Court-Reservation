from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException        

from selenium.webdriver.support.ui import Select
import threading

import time
import datetime

def fillform(id, value, driver):
	elem = driver.find_element_by_id(id)
	elem.clear()
	elem.send_keys(value)

# def tabs(N, driver):
# 	actions = ActionChains(driver) 
# 	actions.send_keys(Keys.TAB * N)
# 	actions.perform()

file_object = open("account.txt", "r")
username = ''
password = ''
for line in file_object:
	strs = line.split()
	username = strs[0]
	password = strs[1]

def cancel():
	# incognito mode
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")

	# open chrome
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.implicitly_wait(15)
	driver.get("***REMOVED***")

	fillform('UserName', username, driver)
	fillform('password', password, driver)
	submit = driver.find_element_by_id('submit-sign-in')
	submit.submit()

	elems = driver.find_elements_by_class_name('reservation-info')

	for elem in elems:
		# print(elem.text)
		
		tag = elem.find_element_by_tag_name('a')
		cancelbutton = driver.find_elements_by_id(tag.get_attribute('id'))

		for button in cancelbutton:
			if(button.text == 'cancel reservation'):
				button.click()

	
	driver.quit()


cancel()

