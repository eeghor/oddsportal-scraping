"""
Scrape OddsPortal.com: we are specifically interested in the Australian Open results and most of all the actual starting times

"""

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import pandas as pd
from collections import namedtuple


WAIT_TIME = 40  # max waiting time for a page to load
y_from =2009
y_to = 2016

comps = "MS WS"  # simply list competitions you want here, e.g. "MS WS"

abbr_dict = {"MS" : "Men's Singles", 
				"WS" : "Women's Singles"}

assert y_from > 2008 and y_to < 2017, ("We've got a problem: you requested years {}-{} but there's only data for 2009-2016...".format(y_from, y_to))

assert y_from <= y_to, ("Please, make sure that the earliest year you pick is not after the last year...")

# choose driver = webdriver.PhantomJS() for headless browsing!
driver = webdriver.Chrome('/Users/ik/Codes/oddsportal-scraping/chromedriver')
# driver = webdriver.PhantomJS()


what_click_comps = {"MS": "ATP Australian Open", "WS": "WTA Australian Open"}
TennisMatch = namedtuple("TennisMatch", "date time p1 p2 score")

list_matches = []

print("-------> scraping oddsportal.com")

driver.get("http://www.oddsportal.com/results/")
# select the Melbourne time zone
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-header-timezone-expander"))).click()
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Melbourne"))).click()

# now go to Tennis
WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Tennis"))).click()

page_to_go_back_to = driver.current_url


for i, comp in enumerate(comps.split()):

	if i > 0:
		driver.get(page_to_go_back_to)
	
	# what competition?
	print("extracting the {} tournament...".format(abbr_dict[comp]))
	WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, what_click_comps[comp]))).click()
	# and the year?
	
	for year in range(y_from, y_to +1):
	
		print("scraping year {}...".format(year))
		WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, str(year)))).click()
		# go to the very last page
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
				
				except NoSuchElementException:  # this isn't a date-round row
					# check if this is a typical result row
					try:
						result_tds = row.find_elements_by_xpath(".//td[@class]")
			
						if len(result_tds) > 3:  # has to be the proper result row
							starting_time, players, score = [w.text.strip() for w in result_tds[:3]]
							p1, p2 = map(lambda _: _.strip(), players.split(" - "))
							list_matches.append(TennisMatch(dte, starting_time, p1, p2, score))
						else:
							continue
			
					except NoSuchElementException:
						continue # do nothing
					
			# time to move to the next page
		
			try:
				active_page_span = pagination_bar.find_element_by_xpath(".//span[@class='active-page']")
				
				if not active_page_span.text.strip() == "1":
					# do another click
					WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.LINK_TEXT, "«"))).click()
					WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "»|")))
				else:
					break
			except NoSuchElementException:
				print("error! couldn\'t find the active page span on the pagination bar!")
		
driver.quit()

print("done. retrieved {} match results".format(len(list_matches)))

df = pd.DataFrame(columns="date time player1 player2 score".split())

for i, row in enumerate(list_matches):
	df.loc[i] = row
	
csv_fl = "scraped_oddportal_data_" + "_".join(comps.split()) + "_" + str(y_from) + "_" + str(y_to) + ".csv"

df.to_csv(csv_fl, index=False, sep="\t")

print("saved everything in the file called {} in your local directory".format(csv_fl))




	

