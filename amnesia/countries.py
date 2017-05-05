''' Script that collects all the countries and their corresponding alpha-2 codes from wikipedia and adds entries to the DB. '''

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amnesia.settings")
import django
django.setup()

import requests, bs4

def send_request(url):
	try:
		r = requests.get(url)
	except:
		print("Error occurred while sending request to %s" % url)
		exit(1)
	return r

def get_wiki_table_rows(url):
	r = send_request(url)
	soup = bs4.BeautifulSoup(r.text, 'html.parser')
	# Searching for the desired table
	table = soup.find('table', attrs={'class': 'wikitable sortable'}) # Don't add jquery-tablesorter to class because wikipedia adds that class using JS
	trows = table.find_all('tr')[1:] # First row contains headings
	return trows

def get_countries(url):
	"""
		Returns a list of dictionary of countries with their ISO-Alpha 2 Code {'name': , 'code': }
	"""
	trows = get_wiki_table_rows(url)
	countries = []
	for row in trows:
		tds = row.find_all('td')
		code = tds[0].text.strip()
		name = tds[1].text.strip()
		href = tds[1].find('a')['href']
		if '%' not in href:
			if not href.startswith('/'):
				href = '/' + href
			if href[-1] == '/':
				href = href[:-1]
			name = ' '.join(href.split('/')[-1].split('_')).strip()
		countries.append({'name': name.strip(), 'code': code})
	countries = sorted(countries, key=lambda c: c['name'])
	return countries

def get_calling_codes(url):
	trows = get_wiki_table_rows(url)
	countries = []
	for row in trows:
		tds = row.find_all('td')
		name = tds[0].text.strip()
		calling_code = tds[1].find('a').text.strip()
		countries.append({'name': name, 'calling_code': calling_code})
	countries = sorted(countries, key=lambda c: c['name'])
	return countries

def commit_to_db(countries):
	from number.models import Country
	from django.db.utils import IntegrityError
	for country in countries:
		try:
			Country.objects.create(
					name=country['name'],
					code=country['code'],
					calling_code=country.get('calling_code', '')
				)
		except IntegrityError as e:
			print("ERROR: Couldn't add %s" % (country))
			print(e.__str__())

if __name__ == '__main__':

# Countries
	url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"
	countries = get_countries(url)

# Country Calling Codes
	url = "https://en.wikipedia.org/wiki/List_of_country_calling_codes"
	calling_codes = get_calling_codes(url)
	
	for each in calling_codes:
		name = each['name'].lower()
		cc = each['calling_code']
		if len(cc.split(',')) > 1 or len(cc.split(' ')) > 1:
			continue
		for country in countries:
			cname = country['name'].lower()
			if name == cname:
				country['calling_code'] = cc
				break
	# Couldn't add the codes for a few countries because of data irregularities. Need to add calling_codes to those countries manually.

# Committing to DB
	commit_to_db(countries)

'''
Note:
	Few of the countries have been assigned calling code with primary code of some other country + some area code.
	For such countries, calling_code has been left empty.
'''
