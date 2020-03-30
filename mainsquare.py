#Install before execution
# python3
# pip install BeautifulSoup4
# pip install schedule

from bs4 import BeautifulSoup
import urllib.request
import webbrowser
import schedule
import time

VENDREDI = 'Vendredi'
PASS3JOURS = 'Billet 3 Jours'
TICKETSWAP_BASE_URL = 'https://www.ticketswap.fr'
TICKETSWAP_MAIN_SQUARE = TICKETSWAP_BASE_URL + '/event/main-square-festival-2020/bb407518-6928-4a6c-b035-5c3944029c18'


def check_for_offer(offer):
	print('running...')

	div = offer.find_parent("div").find_parent("div")
	span = div.find('footer').find_all("span")
	places = span[0].text
	
	if places != '0':
		a = offer.find_parent('a')
		url = a.get('href')
		webbrowser.open_new_tab(TICKETSWAP_BASE_URL + url)

#conf
webbrowser.register('chrome', None)
page = urllib.request.urlopen(TICKETSWAP_MAIN_SQUARE)
soup = BeautifulSoup(page, 'html.parser')

#scraping
vendredi = soup.find(string=VENDREDI)
pass_3_jours = soup.find(string=PASS3JOURS)

#jobs
schedule.every().minute.do(check_for_offer, offer=vendredi)
schedule.every().minute.do(check_for_offer, offer=pass_3_jours)

while True:
	schedule.run_pending()
	time.sleep(1)