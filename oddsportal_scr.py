import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select  # to deal with dropdown menues
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
from collections import namedtuple


WAIT_TIME = 40
year = 2016

TennisMatch = namedtuple("TennisMatch", "date time p1 p2 score")
list_matches = []

driver = webdriver.Chrome('/Users/ik/Codes//oddsportal-scraping/chromedriver')

print("""-------> scraping aopen.com""")

driver.get("http://www.oddsportal.com/results/")

WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-header-timezone-expander"))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Melbourne"))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Tennis"))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "ATP Australian Open"))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, str(year)))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "»|"))).click()
time.sleep(3)

# date has the form 13 Jan 2016
#dates = driver.find_element_by_xpath("//table[@id='tournamentTable']").find_elements_by_xpath("//tbody/tr/th[@colspan='4']/span[@*]")
#print("there are {} dates on this page".format(len(dates)))
#for data in dates:
#	print("in rows {}".format(data@rowIndex))
#for date in dates:@contains(@class, ' deactivate')]"):
	#print("found {} rows".format(len(driver.find_elements_by_xpath("//tr[contains(@class, ' deactivate')]"))))
tbl = driver.find_element_by_xpath("//table[@id='tournamentTable']")
for row in tbl.find_elements_by_xpath("tr"):
	if row.find_element_by_xpath("//th[@colspan='4']/span[@*]"):
		dte = row.find_element_by_xpath("//th[@colspan='4']/span[@*]").text
	elif len(row.find_elements_by_xpath("td")) > 3:
		time, players, score = [w.text.strip() for w in row.find_elements_by_xpath("td")[:3]]

		#time, players, score = [w.text.strip() for w in row.find_elements_by_xpath("td")[:3]]
		#print("time=",time,"players=",players)
		p1, p2 = map(lambda _: _.strip(), players.split(" - "))
		list_matches.append(TennisMatch(dte, time, p1, p2, score))

WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "«"))).click()

print(list_matches)
time.sleep(3)
driver.quit()



	

