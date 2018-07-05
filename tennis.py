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

def reserve(datepickertag, tomorrow, reserveid, starttime, endtime):
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

	elems = driver.find_elements_by_id('reserve')
	elems[reserveid].click() # weekend # 10 court 1 11 weekend 12 court 2 13 weekend

	elem = driver.find_element_by_id('resv-date')
	elem.click()

	daystr = str(tomorrow.day);
	datetofind = "//*[contains(text(), '" + daystr + "')]"

	datepick = driver.find_elements_by_class_name(datepickertag) # ui-datepicker-week-end
	for parent in datepick:
		child = parent.find_elements_by_xpath(datetofind)
		if(len(child) > 0) :
			child[3].click()
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
	driver.quit()


thread_list = []

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

weekno = tomorrow.weekday()

datepickertag = 'ui-datepicker-week-end'

if weekno < 5:
    datepickertag = 'ui-state-default'
    t = threading.Thread(target=reserve, args=(datepickertag, tomorrow, 10, '7:00 PM', '8:00 PM'))
    thread_list.append(t)
    t = threading.Thread(target=reserve, args=(datepickertag, tomorrow, 12, '8:00 PM', '9:00 PM'))
    thread_list.append(t)
    # reserve(datepickertag, tomorrow, 10, '7:00 PM', '8:00 PM')
    # reserve(datepickertag, tomorrow, 12, '8:00 PM', '9:00 PM')
else:
	t = threading.Thread(target=reserve, args=(datepickertag, tomorrow, 11, '7:00 PM', '8:00 PM'))
	thread_list.append(t)
	t = threading.Thread(target=reserve, args=(datepickertag, tomorrow, 13, '8:00 PM', '9:00 PM'))
	thread_list.append(t)	# reserve(datepickertag, tomorrow, 11, '7:00 PM', '8:00 PM')
	# reserve(datepickertag, tomorrow, 13, '8:00 PM', '9:00 PM')



for thread in thread_list:
	thread.start()
for thread in thread_list:
	thread.join()

