## Scrape [OddsPortal.com][1]
---- 
The purpose of this script is to scrape the Australian Open match results and specifically, the **actual** times when matches started. A few things to keep in mind:

1. You need to install [Selenium][2] 
2. You also need to either install [PhantomJS][3] for the headless (invisible) browsing or in case you would like to watch your browser grabbing the data, you need to download a web driver, e.g. [ChromeDriver][4] to use Chrome
3. The data available on OddsPortal.com covers years **2009** to **2016**. Should you try to ask for any other years, the script will do nothing and suggest that you think again
4. It is not uncommon for the actual starting time to be *considerably different* from the scheduled time. For example, a match was to commence at 10 am but was shifted to afternoon, say, 14:30 pm instead.  The times listed on OddsPortal.com are typically some minutes before the matches **actually** started.

[1]:	http://www.oddsportal.com/
[2]:	http://selenium-python.readthedocs.io/index.html
[3]:	http://phantomjs.org/
[4]:	https://sites.google.com/a/chromium.org/chromedriver/