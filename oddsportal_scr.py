import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select  # to deal with dropdown menues
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.LINK_TEXT, "»|"))).click()
# wait until this stuff becomes clickable (it's at the bottom of the page)
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.LINK_TEXT, "«")))

"""
the idea here is to simply locate the main table first and then go through every row; as we go, we check whether the row is a header with 
the date and round information or a match result row or something else;
if it turns out to be a header, we update the date which will then be attached to all subsequently found match results.
"""

while True:

	# find the pagination bar that has an id=pagination
	try:
		pagination_bar = driver.find_element_by_xpath("//div[@id='pagination']")
	except NoSuchElementException:
		print("error! couldn\'t find the pagination bar on the page!")

	#
	# find the table; there's supposed to be only one table like this on the page
	#
	
	try:
		tbl = driver.find_element_by_xpath("//table[@id='tournamentTable']")
	except NoSuchElementException:
		print("error! couldn\'t find the main table on the page!")
	
	#
	# ok, now go through all rows of this table
	#
	for row in tbl.find_elements_by_xpath(".//tbody/tr"):
		# check if this row is a header
		try:
			date_round_span = row.find_element_by_xpath(".//th[@colspan='4']/span[@*]")
			dte = date_round_span.text  # grab the date, which has the form  like 13 Jan 2016
			# print("found span=", dte)
		
		except NoSuchElementException:  # this isn't a date-round row
			# print("this is not a header row...")
			# check if this is a typical result row
			try:
				result_tds = row.find_elements_by_xpath(".//td[@class]")
				# print("found tds..")
				# for td in result_tds:
				# 	print(td.text)
	
				if len(result_tds) > 3:  # has to be the proper result row
					# print("here tds more than 3...")
					starting_time, players, score = [w.text.strip() for w in result_tds[:3]]
					# print("time=",starting_time)
					# print("players=",players)
					# print("score=",score)
					p1, p2 = map(lambda _: _.strip(), players.split(" - "))
					list_matches.append(TennisMatch(dte, starting_time, p1, p2, score))
				else:
					continue
	
			except NoSuchElementException:
				continue # do nothing
			
	print("done with this page...")

	try:
		active_page_span = pagination_bar.find_element_by_xpath(".//span[@class='active-page']")
		print("active_page_span=", active_page_span.text)

		if not active_page_span.text.strip() == "1":
			# do another click
			print("clicking « ... ")
			WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.LINK_TEXT, "«"))).click()
			WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "»|")))
		else:
			break
	except NoSuchElementException:
		print("error! couldn\'t find the active page span on the pagination bar!")
		
print("done. got {} matches".format(len(list_matches)))
print(list_matches[-10:])
driver.quit()



	

