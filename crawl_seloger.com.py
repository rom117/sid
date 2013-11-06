#-*- coding:utf-8 -*-
"""
crawl all the rental ads in Paris from the website seloger.com
"""
from bs4 import BeautifulSoup
import urllib
import csv
import os
#retrieve variables data
from get_variables import *


def get_vars(names, soup_specific, get_function=""):
	"""
	FUNCTION
	get specific variables contained in a part of the html content of the page and retrieved in a similar fashion
	PARAMETERS
	names: list of variables to retrieve [list]
	soup_specific: part of the html content of the page [BeautifulSoup object]
	get_function: function to call to retrieve the set of variables [string]
	RETURN
	values of variables given in parameter [list]
	"""
	rental=[]
	for name in names:
		try:
			if get_function=="":
				value=eval("get_"+name)(soup_specific)
			else:
				value=eval(get_function)(soup_specific, name[1])
		except Exception, e:
			#~ print "get_specific_vars exception", e
			value=""
		rental.append(value.encode('utf-8'))
	return rental


def get_data_rental(mapping, url):
	"""
	FUNCTION
	get data of a rental in Paris from the page in parameter
	PARAMETERS
	mapping: dictionary mapping variables and text search [dictionary]
	url: page of the rental to crawl [string]
	example of page: http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2)
	VARIABLES TO RETRIEVE
	#DONE
	url: webpage of the rental
	cp: zip postal of the rental
	prix: price of the rent
	etg: floor of the rental
	ter: is there a terrace?
	park: is there a car park?
	maj: on-line publishing date (or date of update)
	ref: reference of the rental
	disp: date of availability
	gar: price of the guarantee
	transp: means of transport in the neighborhood
	prox: shops, buildings in the neighborhood
	surf: surface
	const: year of construction
	toil: number of WCs
	toil_sep: is the WC separated?
	sdb: number of bathrooms
	meuble: furnished?
	rang: are there storage units?
	asc: is there a lift?
	chauf: type of heating system
	cuis: type of kitchen
	gard: is there a watchman?
	ent: is there an individual entrance
	calme: is it quiet?
	piece: number of rooms
	descr: description of the ad
	hon: price of fees
	tel: phone number of the announcer or owner
	#TODO
	score_gen: general score of the location
	date_last_vote: date of the last vote on this rental
	score_shop: (Commerce alimentaire)
	score_rest: (Restaurants et bars)
	score_rep: (Réputation du quartier)
	score_transp: (Transports en commun)
	score_cult: (Culture ou sport)
	score_neigh: (Voisins et habitants)
	score_safe: (Sécurité)
	score_clean: (Propreté et urbanisme)
	score_calm: (Tranquillité de la rue)
	score_price: (Prix des magasins)
	score_green: (Espaces verts)
	score_traf: (Circulation routière)
	score_air: (Qualité de l'air)
	score_park: (Stationnement)
	RETURN
	rental: retrieved data from a rental page [list]
	"""
	rental=[]
	soup = BeautifulSoup(urllib.urlopen(url))
	#add the url of the page
	rental.append(url)

	#cp, prix
	#<div class="header_ann" itemscope itemtype="http://schema.org/Product">
	soup_part=soup.find("div", {"class": "header_ann"})
	rental.extend(get_vars(mapping["cp_prix"], soup_part))

	#<div class="infos_ann_light">
	soup_first_vars=soup.find("div", {"class": "infos_ann_light"})
	#etg, asc, ter, park
	#<ol class="liste_details">
	soup_part=soup_first_vars.find("ol", {"class": "liste_details"})
	rental.extend(get_vars(mapping["first_vars"], soup_part, "get_first_vars"))
	#maj, ref
	#<div class="maj_ref">
	soup_part=soup_first_vars.find("div", {"class": "maj_ref"})
	rental.extend(get_vars(mapping["maj_ref"], soup_part))
	#disp, gar
	#<ol class="liste_details" id="mentions_ann">
	soup_part=soup_first_vars.find("ol", {"id": "mentions_ann"})
	rental.extend(get_vars(mapping["disp_gar"], soup_part, "get_first_vars"))
	#transp, prox
	#<dl>
	soup_part=soup_first_vars.find("dl")
	rental.extend(get_vars(mapping["transp_prox"], soup_part))

	#surf, toil, toil_sep, sdb, meuble, chauf cuis, gard, ent calme
	#<div class="bloc_infos_ann" id="detail"><ol class="liste_details">
	soup_part=soup.find("div", {"id": "detail"}).find("ol", {"class": "liste_details"})
	rental.extend(get_vars(mapping["details"], soup_part, "get_details"))
	#piece
	rental.extend(get_vars(mapping["piece"], soup_part))

	#other independent variables
	rental.extend(get_vars(mapping["descr_hon_tel"], soup))

	#score variables
	#<div id="layer_notation_generale">
	soup_score_gen = BeautifulSoup(urllib.urlopen("http://www.seloger.com/"+url[-12:-4]+"/ajax_notation_quartiers_generale_new.htm")).find("div", {"id": "layer_notation_generale"})
	#~ #score_gen, date_last_vote
	rental.extend(get_vars(mapping["score_gen"], soup_score_gen))
	#score_shop, score_rest, score_rep, score_transp, score_cult, score_neigh, score_safe, score_clean, score_calm, score_price, score_green, score_traf, score_air, score_park
	#<div class="notes_categories">
	soup_part = soup_score_gen.find("div", {"class": "notes_categories"})
	rental.extend(get_vars(mapping["score_vars"], soup_part, "get_score_vars"))

	return rental


def get_data_rentals():
	"""
	FUNCTION
	get data of all the rental ads in Paris from the website seloger.com
	PARAMETERS
	None
	RETURN
	data: retrieved data from all the rental pages [list of lists]
	"""
	mapping=group_variables()
	#TODO: check domain name
	pages=[]
	#TEST
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-9eme-75/lorette-martyrs/83162365.htm")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-18eme-75/78463899.htm")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-8eme-75/parc-monceau/82439751.htm")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-16eme-75/porte-dauphine/78897937.htm")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-7eme-75/invalides/81937887.htm")

	rentals=[]
	for index in xrange(len(pages)):
		print "page", str(index+1)
		rentals.append(get_data_rental(mapping, pages[index]))
	return rentals


def group_variables():
	"""
	FUNCTION
	group together variables that can be found in a similar fashion in the rental page
	PARAMETERS
	None
	RETURN
	mapping: dictionary mapping variables and text search [dictionary]
	"""
	mapping={}
	mapping["cp_prix"]=["cp", "prix"]
	mapping["first_vars"]=[("etg", "Etage"), ("asc", "Ascenseur"), ("ter", "Terrasse"), ("park", "Parking")]
	mapping["maj_ref"]=["maj", "ref"]
	mapping["disp_gar"]=[("disp", "Disponible"), ("gar", "Garantie")]
	mapping["transp_prox"]=["transp", "prox"]
	mapping["details"]=[("surf", "Surface"), ("const", "Année de construction"), ("toil", "Toilettes"), ("toil_sep", "Toilettes Séparées"), ("sdb", "Salles de bain"), ("meuble", "Meublé"), ("rang", "Rangements"), ("chauf", "Type de chauffage"), ("cuis", "Type de cuisine"), ("gard", "Gardien"), ("ent", "Entrée"), ("calme", "Calme")]
	mapping["piece"]=["piece"]
	mapping["descr_hon_tel"]=["descr", "hon", "tel"]
	mapping["score_gen"]=["score_gen", "date_last_vote"]
	mapping["score_vars"]=[("score_shop", "Commerce alimentaire"), ("score_rest", "Restaurants et bars"), ("score_rep", "Réputation du quartier"), ("score_transp", "Transports en commun"), ("score_cult", "Culture ou sport"), ("score_neigh", "Voisins et habitants"), ("score_safe", "Sécurité"), ("score_clean", "Propreté et urbanisme"), ("score_calm", "Tranquillité de la rue"), ("score_price", "Prix des magasins"), ("score_green", "Espaces verts"), ("score_traf", "Circulation routière"), ("score_air", "Qualité de l'air"), ("score_park", "Stationnement")]

	return mapping


def get_headers_rentals():
	"""
	FUNCTION
	get the list of variable names to retrieve
	PARAMETERS
	None
	RETURN
	list of variable names [list]
	"""
	return ["url", "cp", "prix", "etg", "asc", "ter", "park", "maj", "ref", "disp", "gar", "transp", "prox", "surf", "const", "toil", "toil_sep", "sdb", "meuble", "rang", "chauf", "cuis", "gard", "ent", "calme", "piece", "descr", "hon", "tel", "score_gen", "date_last_vote", "score_shop", "score_rest", "score_rep", "score_transp", "score_cult", "score_neigh", "score_safe", "score_clean", "score_calm", "score_price", "score_green", "score_traf", "score_air", "score_park"]


def save_data_rentals(path_file, rentals):
	"""
	FUNCTION
	save all the collected data in a csv file
	PARAMETERS
	path_file: path of the file that will contain the collected data
	rentals: retrieved data from all the rental pages [list of lists]
	RETURN
	None
	"""
	#open file
	writer=csv.writer(open(path_file, 'w'))

	#write headers
	headers=get_headers_rentals()
	writer.writerow(headers)

	#write every rental in the file
	for rental in rentals:
		writer.writerow(rental)


def main(path_file):
	"""
	MAIN FUNCTION
	run the crawling of all the rental ads in Paris from the website seloger.com
	RETURN
	None
	"""
	#delete the file if already exists
	if os.path.exists(path_file):
		os.remove(path_file)

	#get data from all the rentals
	rentals=get_data_rentals()

	#save it in a csv file
	save_data_rentals(path_file, rentals)


#call main function
path_file="data.csv"
main(path_file)
