import requests
from bs4 import BeautifulSoup as BS 
import json
from pprint import pprint
from fake_useragent import UserAgent as UA
import re
import os
import json

def write_data(file_name, data):
	with open(file_name, 'w', encoding="utf8") as file:
		json.dump(data, file, indent=4)


def get_request(actor_id, url):
	session = requests.Session()
	headers = {
		'User-Agent': UA().random
	}
	session.headers.update(headers)
	request = session.get(url.format(actor_id=actor_id))
	return request.text

def get_actor(response):
	soup = BS(response, 'html.parser')
	bio_info = soup.find('table', {"id": "name-overview-widget-layout"})
	name = soup.title.text.strip(' - IMDb')
	born = bio_info.find('div', {"id": 'name-born-info'}).find('time')['datetime']
	died = bio_info.find('div', {"id": 'name-death-info'}).find('time')['datetime']
	born_in = bio_info.find('div', {"id": 'name-born-info'}).find_all('a')[-1].get_text()#.get_all('a')[-1].get_text()
	died_in = bio_info.find('div', {"id": 'name-death-info'}).find_all('a')[-1].get_text()#.get_all('a')[-1].get_text()
	img = bio_info.find('img', {'id': "name-poster"})['src']
	if not os.path.exists:
		with open('img.jpg', 'wb') as file:
			r = requests.get(img)
			file.write(r.content)
	
	all_films = soup.find('div', {'class': 'filmo-category-section'})
	all_films_links = []
	for film in all_films:
		try:
			all_films_links.append(film.find('a')['href'])
		except Exception as error:
			continue
		
	data = {
		"Name": name,
		"Born": born, 
		"Died": died,
		"Born in": born_in,
		"Died in": died_in
	}
	write_data(f'{name}.json', data)
	
	return all_films_links
	# профессия
	# д.р.
	# д.с.

def get_film(response):

def main():
	# https://www.imdb.com/name/nm0091074/?ref_=nv_sr_srsg_1
	actor_id = input()
	# https://www.imdb.com/name/nm0091074/bio?ref_=nm_ov_bio_sm
	#url = 'https://www.imdb.com/name/{actor_id}/?ref_=nm_ov_bio_sm'
	url = "https://www.imdb.com/name/{actor_id}/?ref_=nv_sr_srsg_1"
	request = get_request(actor_id, url)
	get_actor(request)

if __name__ == '__main__':
	main()