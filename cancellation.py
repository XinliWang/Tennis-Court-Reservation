from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException        

from selenium.webdriver.support.ui import Select
import threading

import time
import datetime
import send
import logging

logging.basicConfig(filename='tennis.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')

def fillform(id, value, driver):
	elem = driver.find_element_by_id(id)
	elem.clear()
	elem.send_keys(value)


def cancel():
	# read username and password
	file_object = open("account.txt", "r")
	username = ''
	password = ''
	url = ''
	for line in file_object:
		strs = line.split('=')
		strs = list(map(lambda s: s.strip(), strs))
		if strs[0] == 'username':
			username = strs[1]
		elif strs[0] == 'password':
			password = strs[1]
		elif strs[0] == 'url':
			url = strs[1]
		elif strs[0] == 'email':
			email = strs[1]
		elif strs[0] == 'emailpassword':
			emailpassword = strs[1]
		elif strs[0] == 'target':
			target = list(map(lambda s: s.strip(),strs[1].split(',')))

	# incognito mode
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')

	# open chrome
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.implicitly_wait(15)
	driver.get(url)

	logging.info(str(threading.current_thread()) + " signin " + username + " successfully")

	fillform('UserName', username, driver)
	fillform('password', password, driver)
	submit = driver.find_element_by_id('submit-sign-in')
	submit.submit()

	logging.info(str(threading.current_thread()) + " signin " + username + " successfully")

	today = datetime.date.today()

	datestr = today.strftime('%B %d, %Y')

	elems = driver.find_elements_by_class_name('reservation-info')

	while(len(elems) != 0):
		n = len(elems)
		for elem in elems:
			if(datestr in elem.text):
				tag = elem.find_element_by_tag_name('a')
				cancelbutton = driver.find_elements_by_id(tag.get_attribute('id'))
				
				for button in cancelbutton:
					if(button.text == 'cancel reservation'):
						# print/(button.text)
						button.click()
						submit = driver.find_element_by_id('cancel-resv-btn')
						submit.submit()
						break
				logging.info(str(threading.current_thread()) +  datstr + " cancel sucessfully")
				send.send(email, emailpassword, target, ("\n" + datstr + ": cancel sucessfully" ))
				break
			n-=1
		if(n == 0):
			break
		elems = driver.find_elements_by_class_name('reservation-info')

	logging.info(str(threading.current_thread()) + "cancellation script done")
	driver.quit()
