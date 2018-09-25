from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import Select
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

import time
import datetime
import send
import logging

logging.basicConfig(filename='tennis.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')



def fillform(id, value, driver):
	elem = driver.find_element_by_id(id)
	elem.clear()
	elem.send_keys(value)

def reserve(tomorrow, reserveid, starttime, endtime):
	# read username and password
	file_object = open("account.txt", "r")
	username = ''
	password = ''
	url = ''
	email = ''
	emailpassword = ''
	target = []
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

	logging.info(str(threading.current_thread()) + " open: " + url)

	fillform('UserName', username, driver)
	fillform('password', password, driver)
	submit = driver.find_element_by_id('submit-sign-in')
	submit.submit()
	logging.info(str(threading.current_thread()) + " signin " + username + " successfully")

	elems = driver.find_elements_by_id('reserve')
	elems[reserveid].click() # weekend # 10 court 1 11 weekend 12 court 2 13 weekend

	elem = driver.find_element_by_id('resv-date')
	elem.click()

	daystr = str(tomorrow.day);
	if(tomorrow.day == 1):
		n = driver.find_elements_by_class_name('ui-icon-circle-triangle-e')
		n[0].click()
	datetofind = "//*[contains(text(), '" + daystr + "')]"

	datepick = driver.find_elements_by_xpath(datetofind)
	for ch in datepick:
		if(ch.text == daystr):
			ch.click()
			break

	time.sleep(3)

	start = driver.find_element_by_id('SelStartTime')
	select = Select(start)
	select.select_by_visible_text(starttime)

	end = driver.find_element_by_id('SelEndTime')
	select = Select(end)
	select.select_by_visible_text(endtime)

	submit = driver.find_element_by_id('submit-new-reservation')
	submit.submit()

	success = driver.find_elements_by_xpath("//*[contains(text(), 'A reservation already exists during this time period.')]")
	court = 1 if reserveid == 10 or reserveid == 11 else 2
	if(len(success) == 1):
		logging.info(str(threading.current_thread()) + " court " + str(court) + ": " + starttime + " " + endtime + " not available")
		if(email != ''):
			send.send(email, emailpassword, target, ("\n" + str(tomorrow) + " court " + str(court) + ": " + starttime + " " + endtime + " not available"))
	else:
		logging.info(str(threading.current_thread()) + " court " + str(court) + ": " + starttime + " " + endtime + " reserved")
		if(email != ''):
			send.send(email, emailpassword, target, ("\n" + str(tomorrow) + " court " + str(court) + ": " + starttime + " " + endtime + " reserved"))
	driver.quit()


def runReserve():
	thread_list = []

	tomorrow = datetime.date.today() + datetime.timedelta(days=1)

	weekno = tomorrow.weekday()

	# datepickertag = 'ui-datepicker-week-end'

	if weekno < 5:
	    t = threading.Thread(target=reserve, args=(tomorrow, 10, '6:00 PM', '7:00 PM'))
	    thread_list.append(t)
	    t = threading.Thread(target=reserve, args=(tomorrow, 12, '5:00 PM', '6:00 PM'))
	    thread_list.append(t)
	    # reserve(tomorrow, 10, '7:00 PM', '8:00 PM')
	    # reserve(tomorrow, 12, '8:00 PM', '9:00 PM')
	else:
		t = threading.Thread(target=reserve, args=(tomorrow, 11, '4:00 PM', '5:00 PM'))
		thread_list.append(t)
		t = threading.Thread(target=reserve, args=(tomorrow, 13, '3:00 PM', '4:00 PM'))
		thread_list.append(t)
		# reserve(tomorrow, 11, '7:00 PM', '8:00 PM')
		# reserve(tomorrow, 13, '8:00 PM', '9:00 PM')

	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()