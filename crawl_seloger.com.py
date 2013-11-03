#-*- coding:utf-8 -*-
"""
crawl all the rental ads in Paris from the website seloger.com
"""
from bs4 import BeautifulSoup
import re
import urllib
import csv


	#~ prix = soup.title.text[-7:-1]
	#~ print "prix", prix
	#~ arrond = soup.title.text[soup.title.text.find("(")+1:soup.title.text.find(")")]
	#~ print "arrond", arrond
	#~ for li in soup.find_all('span'):
#~
#~
	#~ if 'réf.:' in line.lower():
		#~ features.append(line)
		#~ ref = line
		#~ print "ref", ref
#~
	#~ for li in soup.find_all('li', {"class" : "switch_style"}):
		#~ s = StringIO.StringIO(li.text)
		#~ for line in s:
#~
			#~ if 'type de chauffage' in line.lower():
				#~ cauf = line
				#~ print "type_chauffage", cauf
#~
			#~ if 'type de cuisine' in line.lower():
				#~ cuis = line
				#~ print "type_cuisine", cuis
#~
	#~ for li in soup.find_all('li', {"class" : "switch_style"}):
#~
		#~ s = StringIO.StringIO(li.text)
		#~ count = 0
		#~ for line in s:
#~
			#~ if 'surface  ' in line.lower():
				#~ count += 1
				#~ surf = re.findall('\d+', line)[0]
				#~ print "surface", surf
				#~ break
#~
			#~ for li in soup.find_all('li'):
#~
				#~ if 'parking' in li.text.lower():
#~
					#~ if 'N.C' in li.text.replace(' ', ''):
						#~ park = 'Parking: N.C'
					#~ print "parking", park
#~
#~
				#~ s = StringIO.StringIO(li.text)
				#~ for line in s:
#~
					#~ if 'garantie' in line.lower():
#~
						#~ gar = line
						#~ if ',' in line:
							#~ gar = line.replace(',','.')
#~
						#~ if '-' in gar:
							#~ gar = line.replace('-','.')
#~
						#~ print "garantie", garantie
#~
					#~ if 'honoraires' in line.lower():
						#~ hon = line
						#~ #hon = hon[-5:-1]
						#~ if ',' in line:
							#~ hon = line.replace(',','.')
							#~ #hon = hon[-5:-1]
						#~ print "honoraires", hon
#~
					#~ if 'disponible' in line.lower():
						#~ disp = line
						#~ print "disponible", disp
#~
					#~ if 'terrasse  ' in line.lower():
						#~ ter = line
						#~ print "terrasse", ter
#~
					#~ if 'ascenseur  ' in line.lower():
						#~ asc = line
						#~ print "ascenseur", asc
#~
					#~ if 'salle de bain' in line.lower():
						#~ sdb = line
						#~ print "salle_de_bain", sdb
#~
					#~ if 'etages' in line.lower():
						#~ etg = line
						#~ print "etages", etages
#~
					#~ if 'pièce    ' in line.lower():
						#~ piece = line
						#~ print "piece", piece
#~
					#~ if 'rangements' in line.lower():
						#~ rang = line
						#~ print "rangements", rang
#~
					#~ if 'construction' in line.lower():
						#~ const = line
						#~ print "construction", const
#~
					#~ if 'gardien' in line.lower():
						#~ gard = line
						#~ print "gardien", gard
#~
					#~ if 'entré' in line.lower():
						#~ ent = line
						#~ print "entree", ent
#~
					#~ if 'toilettes séparées' in line.lower():
						#~ toil_sep = line[-4:]
					#~ else:
						#~ if 'toilettes' in line.lower():
							#~ toil = line[-2:]
					#~ print "toilettes", toil
#~
					#~ #salle de sejour
					#~ if 'salle de séjour' in line.lower():
						#~ if 'oui' in line.lower():
							#~ sds = line[-4:]
						#~ else:
							#~ sds = re.findall('\d+', line)[0]
					#~ print "salle_de_sejour", sds

def get_maj(soup):
	"""
	FUNCTION
	get the on-line publishing date (or date of update) of the ad
	PARAMETERS
	soup: html source code of the page [BeautifulSoup object]
	RETURN
	maj: maj variable [date]
	"""
	maj=soup.find("span", {"class": "maj"}).get_text()
	maj=maj.split(":")[1].strip()
	return maj


def get_data_rental(url=""):
	"""
	FUNCTION
	get data of a rental in Paris from the page in parameter
	PARAMETERS
	url: page of the rental to crawl
	example of page: http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2)
	VARIABLES TO RETRIEVE
	maj: on-line publishing date (or date of update)
	ref: reference of the rental
	prix: price of the rental
	chauf: is there a heater system?
	cuis: is there a kitchen?
	surf: superficy
	park: is there a parking lot?
	gar: price of the guarantee
	hon: price of the fees
	disp: availability
	ter: is there a terrace?
	asc: is there a lift?
	sdb: is there a bathroom?
	etg: number of floors
	piece: number of rooms
	rang: rangements
	const: year of construction
	gard: is there a watchman?
	toil: is there one WC?
	toil_sep: is the WC separated?
	ent: number of entrances
	cp: code postal of the rental
	transports: nearest means of transport
	proximite: shops, buildings in the neighborhood
	descriptif:
	calme: is it quiet?
	meuble: are there furniture?
	eval: Evaluation de cette localite (securite, reputation, transports en commun, tranquilite)
	link: webpage of the rental
	RETURN
	rental: retrieved data from a rental page [dictionary]
	"""
	rental={}
	#TEST (to be removed)
	url="example.html"
	soup = BeautifulSoup(urllib.urlopen(url))
	rental["maj"]=get_maj(soup)
	print "maj:", rental["maj"]
	return rental


get_data_rental()

def get_data_rentals():
	"""
	FUNCTION
	get data of rental ads in Paris from the website seloger.com
	PARAMETERS
	None
	RETURN
	data: retrieved data from all the rental pages [list of dictionaries]
	"""
	rentals=[]
	for page in pages:
		rentals.append(get_data_rental(page))
	return rentals


def save_data_rentals(path_file, rentals):
	"""
	FUNCTION
	save all the collected data in a csv file
	PARAMETERS
	path_file: path of the file that will contain the collected data
	rentals: retrieved data from all the rental pages [list of dictionaries]
	RETURN
	None
	"""
	writer=csv.writer(open(path_file, 'w'))

	#write headers
	writer.writerow(headers)

	#write every acts in the db
	for rental in rentals:
		writer.writerow(rental)


def main(path_file):
	"""
	MAIN FUNCTION
	run the crawling of all the rental ads in Paris from the website seloger.com
	RETURN
	None
	"""
	#get data from all the rentals
	rentals=get_data_rentals()
	#save it in a csv file
	path_file="/home/rom/Documents/jobs/Sid/python/data.csv"
	save_data_rentals(path_file, rentals)

