#!/usr/bin/python -i

# Install before execution
# python3
# pip install BeautifulSoup4
# pip install schedule
# pip install selenium and follow instructions

import urllib.request
import webbrowser
import schedule
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

#SCRAPING
SAMEDI = 'Samedi'
PASS3JOURS = 'Billet 3 Jours'
TICKETSWAP_BASE_URL = 'https://www.ticketswap.fr'
TICKETSWAP_MAIN_SQUARE = '/event/main-square-festival-2020/bb407518-6928-4a6c-b035-5c3944029c18'
ALARM = 'https://www.youtube.com/watch?v=bWr2rZtV0Kk&fbclid=IwAR1JrzWiRULMxfd-lfDlDZoUwQJDTAQ-1ypLaHOjM6H-piX7kwTROJ-BenM'

# SELENIUM
BUTTON_TICKET = '//*[@class="css-1rg1x3j e1suhhn80"]'
BUTTON_FB = '/html/body/div[2]/div/div/div/div/div/button'
BUTTON_MAIL = 'Se connecter avec une adresse e-mail'
BUTTON_LOGIN = '//*[@id="email"]'
BUTTON_PASSWORD = '//*[@id="pass"]'
BUTTON_SUBMIT = '//*[@id="u_0_0"]'

# Facebook credentials
VALUE_LOGIN = ''
VALUE_PASSWORD = ''

def clic_to_lock(url):
	driver = webdriver.Chrome()
	driver.get(url)

	#clic to 'Acheter un billet'
	driver.find_element_by_xpath(BUTTON_TICKET).click()
	
	#clic to 'Se connecter avec Facebook'
	driver.find_element_by_xpath(BUTTON_FB).click()
	
	#switch to popup
	driver.switch_to.window(driver.window_handles[1])
	
	#seek and fill form
	driver.find_element_by_xpath(BUTTON_LOGIN).send_keys(VALUE_LOGIN)
	driver.find_element_by_xpath(BUTTON_PASSWORD).send_keys(VALUE_PASSWORD)
	driver.find_element_by_xpath(BUTTON_SUBMIT).click()

def concat_url(url):
	return TICKETSWAP_BASE_URL + url

def cook_soup(url):
	page = urllib.request.urlopen(concat_url(url))
	return BeautifulSoup(page, 'html.parser')

def check_for_offer(offer):
	div = offer.find_parent("div").find_parent("div")
	span = div.find('footer').find_all("span")
	return span[0].text

def get_offer_link(offer):
	a = offer.find_parent('a')
	return a.get('href')

def get_available_tickets(url):
	offer_page = cook_soup(url)
	available_tickets = offer_page.find('ul', attrs={"data-testid": "available-tickets-list"})
	return available_tickets.find_all('a')

def run(offer):
	if check_for_offer(offer) != '0':
		#alarm
		webbrowser.open_new_tab(ALARM)

		#get offer link
		url = get_offer_link(offer)
		print("Href found : {}".format(url))
		
		for ticket in get_available_tickets(url):
			try:
				clic_to_lock(concat_url(ticket.get('href')))
				break
			except Exception as e:
				pass

#conf
webbrowser.register('chrome', None)

#scraping
soup = cook_soup(TICKETSWAP_MAIN_SQUARE)
samedi = soup.find(string=SAMEDI)
pass_3_jours = soup.find(string=PASS3JOURS)
#dimanche = soup.find(string='Dimanche')

#jobs
schedule.every().minute.do(run, samedi)
schedule.every().minute.do(run, pass_3_jours)
#schedule.every().minute.do(run, dimanche)

print('--- Starting schedules')
while True:
	schedule.run_pending()
	time.sleep(60)
	print("running {} ...".format(datetime.now().strftime("%H:%M:%S")))