import requests
from bs4 import BeautifulSoup as BS 
import json
from pprint import pprint
from fake_useragent import UserAgent as UA
import re
import os
import json

# запись в json
def write_data(file_name, data):
	with open(file_name, 'w', encoding="utf8") as file:
		json.dump(data, file, indent=4, ensure_ascii=False)

# запрос
def get_request(_id, url):
	session = requests.Session()
	headers = {
		'User-Agent': UA().random
	}
	session.headers.update(headers)
	request = session.get(url.format(_id=_id))
	return request.text

def get_actor(response, actor_id):
	soup = BS(response, 'html.parser')
	
	# вся инфа
	bio_info = soup.find('table', {"id": "name-overview-widget-layout"})
	
	# имя
	name = soup.title.text.strip(' - IMDb')
	
	# born
	try:
		born = bio_info.find('div', {"id": 'name-born-info'}).find('time')['datetime']
	except Exception as error:
		born = None
	
	# died
	try:
		died = bio_info.find('div', {"id": 'name-death-info'})
	except Exception as error:
		died = None
	else:
		# died is None if there is no
		if type(died) == None:
			died = None
		else:
			died = bio_info.find('div', {"id": 'name-death-info'}).find('time')['datetime']
	
	# born in
	try:
		born_in = bio_info.find('div', {"id": 'name-born-info'}).find_all('a')[-1].get_text()
	except Exception as error:
		born_in = None

	# dead in
	try:
		died_in = bio_info.find('div', {"id": 'name-death-info'})
	except Exception as error:
		died_in = None
	else:
		# died in is None if there is no
		if type(died_in) == None:
			died_in = None
		else:
			died_in = bio_info.find('div', {"id": 'name-death-info'}).find_all('a')[-1].get_text()
	# jobs 
	job_block = soup.find('div', {'id': 'name-job-categories'}).find_all('span', {'class': 'itemprop'})
	jobs = []
	for job in job_block:
		jobs.append(job.get_text())
	
	# biography
	bio = bio_info.find('div', {'class': 'inline'}).get_text() # !!!!!!!!!
	
	# actor poster
	try:
		img_src = bio_info.find('img', {'id': "name-poster"})['src']
	except Exception as error:
		img = None
	else:
		# check actors_poster dir
		if not os.path.exists('actors_posters'):
			os.mkdir('actors_posters')
		os.chdir('actors_posters')
		
		# save actor poster
		with open(f'{actor_id}.jpg', 'wb') as img:
			r = requests.get(img_src)
			img.write(r.content)
	# all films in filmography
	all_films = soup.find('div', {'class': 'filmo-category-section'})
	# all films links
	all_films_links = []
	
	for film in all_films:
		try:
			all_films_links.append(film.find('b').find('a')['href'])
		except Exception as error:
			continue
		
	data = {
		"Name": name,
		"Jobs": jobs,
		"Biography": bio,
		"Born": born, 
		"Died": died,
		"Born in": born_in,
		"Died in": died_in
	}
	write_data(f'{actor_id}.json', data)
	
	return all_films_links

def get_film(response):
	soup = BS(response, 'html.parser')
	try:
		film_info = soup.find('div', {'id': 'title-overview-widget'})
	except Exception as error:
		print(error)
		film_info = None
	
	# title
	try:
		title = soup.title.text.strip(' - IMDb')
	except Exception as error:
		print(error)
		title = None
	
	# release
	try:
		release_date = film_info.find('div', {'class': 'subtext'}).find_all('a')[-1]
	except Exception as error:
		print(error)
		release_date = None

	# duration
	try:
		duration = film_info.find('div', {'class': 'subtext'}).find('time').get_text()
	except Exception as error:
		print(error)
		duration = None

	# writer
	try:
		writer = film_info.find('h4', {'text': 'Writer:'}).get_text()
	except Exception as error:
		print(error)
		writer = None

	# director
	try:
		director = film_info.find('h4', {'text': 'Director:'}).get_text()
	except Exception as error:
		print(error)
		director = None

	# description
	try:
		description = film_info.find('div', {'class': 'ipc-html-content ipc-html-content--base'}).find('div').get_text()
	except Exception as error:
		print(error)
		description = None

	# жанр
	try:
		genres = [genre.get_text() for genre in film_info.find_all('div', {'class': 'subtext'})[0:-2]]
	except Exception as error:
		print(error)
		genres = None

	data = {
		'title': title,
		'release_date': release_date,
		'duration': duration,
		'writer': writer,
		'director': director,
		'description': description,
		'genres': genres,

	}
	return data
def main():
	actor_id = input()
	url = "https://www.imdb.com/name/{_id}/?ref_=nv_sr_srsg_1"
	request = get_request(actor_id, url)
	# all links of films which actor has taken part in
	all_actor_films_links = get_actor(request, actor_id)
	for actor_film_link in all_actor_films_links:
		url = 'https://www.imdb.com{_id}'
		all_actors_in_film = get_film(get_request(actor_film_link, url))
		print(all_actors_in_film)
if __name__ == '__main__':
	main()