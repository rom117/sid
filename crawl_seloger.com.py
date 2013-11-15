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
from time import sleep


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
	score_gen: general score of the location
	nb_votes: total number of votes
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
	#add the url of the page
	rental.append(url)
	i=0
	#while the page is not available, try to download it up to 5 times
	#the page may be unavailable for two reasons: blocked because too much traffic or the ad has been removed
	while len(rental)==1 and i<5:
		i+=1
		print "while: ", i
		#if it is the second time or more that the page is not accessible, wait a moment before trying again
		if i>1:
			sleep(300)

		try:
			#TODO: check for rentals already rented (Annonce expirée : ce bien n'est malheureusement plus disponible)
			#~ http://www.seloger.com/annonces/locations/appartement/paris-18eme-75/la-chapelle-marx-dormoy/82250985.htm
			soup = BeautifulSoup(urllib.urlopen(url))

			#cp, prix
			#<div class="header_ann" itemscope itemtype="http://schema.org/Product">
			soup_part=soup.find("div", {"class": "header_ann"})

			#check that the page exists
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

			soup_score = BeautifulSoup(urllib.urlopen("http://www.seloger.com/"+url[-12:-4]+"/ajax_notation_quartiers_generale_new.htm")).find("div", {"id": "layer_notation_generale"})
			#~ #score_gen
			rental.extend(get_vars(mapping["score_gen"], soup_score))
			#nb_votes, date_last_vote
			soup_part=soup_score.find("div", {"class": "notes_recap"}).get_text()
			rental.extend(get_vars(mapping["vote"], soup_part))
			#score_shop, score_rest, score_rep, score_transp, score_cult, score_neigh, score_safe, score_clean, score_calm, score_price, score_green, score_traf, score_air, score_park
			#<div class="notes_categories">
			soup_part = soup_score.find("div", {"class": "notes_categories"})
			rental.extend(get_vars(mapping["score_vars"], soup_part, "get_score_vars"))

		except Exception, e:
			print "get_data_rental exception", e
			#~ print "soup:", soup
			print "The page: "+ url +" does not exist!"
			#in case of error, re-initialize the rental list that stores the rental data and try again
			rental=[]
			rental.append(url)

	return rental


def get_url(url):
	"""
	FUNCTION
	get the right url of the rental
	PARAMETERS
	url: url of the rental as given on the search page [string]
	RETURN
	url: right url [string]
	"""
	#in case the domain name is not the same, fall back to www.seloger.com
	#e.g.: www.bellesdemeures.com for very cozy rentals
	#http://www.bellesdemeures.com/annonces/locations/appartement/paris-16eme-75/80716831.htm
	#http://www.seloger.com/annonces/locations/appartement/paris-16eme-75/80716831.htm
	start_url = re.search("\.com", url).end()
	#remove parameters from url to have it work (otherwise the new design is used to render the page and the program fails!)
	end_url = re.search("\?", url).start()
	url="http://www.seloger.com"+url[start_url:end_url]
	print "url rental:", url
	return url


def get_save_rentals(writer):
	"""
	FUNCTION
	get data of all the rental ads in Paris from the website seloger.com and save them into a csv file
	PARAMETERS
	writer: csv file wrapper [File object]
	RETURN
	None
	"""
	mapping=group_variables()
	#TEST
	ranges=[1850, 1902, 2502, 3502, 6002, 100002]
	#~ ranges=[0, 802, 1002, 1252, 1502, 1902, 2502, 3502, 6002, 100002]
	total_nb_rentals=0
	#when searching for paris and rentals, only the first 2,000 rentals are displayed (200 pages of 10 rentals each) -> the search must be done in several steps so as capture the 10,000 and more ads -> split criteria: price
	#for each range of price
	for index in xrange(len(ranges)-1):
		higher=str(ranges[index+1]-1)
		lower=str(ranges[index])
		url_search_page="http://www.seloger.com/new_recherche,new_recherche.htm?cp=75&idtt=1&idtypebien=1,2&pxmin="+lower+"&pxmax="+higher+"&ANNONCEpg="
		#for each range of price, look through the results of the search: 200 pages maximum
		for page_num in xrange(1,201):
			new_url=url_search_page+str(page_num)
			soup = BeautifulSoup(urllib.urlopen(new_url))
			#<a class="annone__detail__title annonce__link" href="http://www.seloger.com/annonces/locations/appartement/paris-9eme-75/lorette-martyrs/83350931.htm?refonte2013=1&cp=75&idtt=1&idtypebien=1,2&pxmax=800&pxmin=0&bd=Li_LienAnn_2"  >
			ads=soup.find_all("a", {"class": ["annone__detail__title"]})
			#if the a tag cannot be found, there are no more rental for this range of price
			if len(ads)==0:
				break
			#always 10 rentals per page except for the last page
			for ad_num in xrange(len(ads)):
				url_rental=get_url(ads[ad_num]["href"])
				#get and save the rental data in the csv file
				writer.writerow(get_data_rental(mapping, url_rental))
				total_nb_rentals+=1
				print "processed pages:", total_nb_rentals


def group_variables():
	"""
	FUNCTION
	group together variables that can be found in a similar fashion in the rental page
	PARAMETERS
	None
	RETURN
	mapping: dictionary mapping variables and text to search if any [dictionary]
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
	mapping["score_gen"]=["score_gen"]
	mapping["vote"]=["nb_votes", "date_last_vote"]
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
	return ["url", "cp", "prix", "etg", "asc", "ter", "park", "maj", "ref", "disp", "gar", "transp", "prox", "surf", "const", "toil", "toil_sep", "sdb", "meuble", "rang", "chauf", "cuis", "gard", "ent", "calme", "piece", "descr", "hon", "tel", "score_gen", "nb_votes", "date_last_vote", "score_shop", "score_rest", "score_rep", "score_transp", "score_cult", "score_neigh", "score_safe", "score_clean", "score_calm", "score_price", "score_green", "score_traf", "score_air", "score_park"]


def main():
	"""
	MAIN FUNCTION
	run the crawling of all the rental ads in Paris from the website seloger.com
	PARAMETERS
	RETURN
	None
	"""
	print "***************************************************************************************************"
	print "* Please check the log.txt file to visualize the log of the execution of the program.             *"
	print "* Please check the data.csv file to visualize the retrieved data.                                 *"
	print "***************************************************************************************************"
	print "The program is running..."

	#save all the prints in a log file
	import sys
	sys.stdout = open("log.txt", "w")

	#delete the file if already exists
	if os.path.exists(path_file):
		os.remove(path_file)

	#open file
	f=open(path_file, 'w')
	writer=csv.writer(f)

	#write headers
	writer.writerow(get_headers_rentals())

	#get and save data from all the rentals
	get_save_rentals(writer)

	#close the file
	f.close()


#call main function
path_file="data.csv"
main()
#~ get_data_rental(group_variables(), "http://www.seloger.com/annonces/locations/appartement/paris-17eme-75/la-fourche-guy-moquet/81161807.htm")
