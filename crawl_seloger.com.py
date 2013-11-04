#-*- coding:utf-8 -*-
"""
crawl all the rental ads in Paris from the website seloger.com
"""
from bs4 import BeautifulSoup
import re
import urllib
import csv
import os

def get_cp(soup):
	"""
	FUNCTION
	get the zip code
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	cp variable [int]
	"""
	#<h1 itemprop="name" title="Location Studio | Paris 4ème (75004)">Location Studio<br />Paris 4ème (75004)</h1>
	cp=soup.find("h1").get_text()
	return cp[cp.find("(")+1:cp.find(")")]


def get_prix(soup):
	"""
	FUNCTION
	get the monthly price of the rent
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	prix variable [int]
	"""
	#<b class="prix_brut">348&nbsp;&euro;&nbsp;cc<sup>*</sup> </b>
	prix_temp=soup.find("b", {"class": "prix_brut"}).get_text()
	prix=""
	for char in prix_temp:
		if char==u"€":
			break
		prix+=char
	return prix


def get_etg(soup):
	"""
	FUNCTION
	get the floor of the rental
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	etg variable [string]
	"""
	#<li>Etage <b>rdc</b></li>
	return soup[2].find("b").get_text().strip()


def get_ter(soup):
	"""
	FUNCTION
	get the terrace data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	ter variable [int]
	"""
	return soup[4].find("b").get_text().strip()


def get_park(soup):
	"""
	FUNCTION
	get the car park data (yes or no)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	park: park variable [boolean]
	"""
	# <li class="switch_style float_right">Parking <b>N.C</b></li>
	return soup[5].find("b").get_text().strip()


def get_maj(soup):
	"""
	FUNCTION
	get the on-line publishing date (or date of update)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	maj variable [date]
	"""
	#<span class="maj" title="Date de mise à jour de l'annonce">MAJ : <b>03 / 11 / 2013</b></span>
	return soup.find("span", {"class": "maj"}).get_text().split(":")[1].strip()


def get_ref(soup):
	"""
	FUNCTION
	get the reference
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	ref variable [string]
	"""
	#<span title="Référence de l'annonce">Réf.: <b title=""> 82466803</b></span>
	return soup.find("span", {"title": "Référence de l'annonce"}).find("b").get_text().strip()


def get_disp(soup):
	"""
	FUNCTION
	get the date of availability
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	disp variable [date]
	"""
	#<li class="noimportant">Disponible le <b>07 / 11 / 2013</b></li>
	return soup.find(text=re.compile("Disponible")).findNext("b").get_text().strip()


def get_gar(soup):
	"""
	FUNCTION
	get the garantee price
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	gar variable [string]
	"""
	#<li class="switch_style">Garantie <b>2moiscc&nbsp;&euro;</b></li>
	return soup.find(text=re.compile("Garantie")).findNext("b").get_text().strip()


def get_transp(soup):
	"""
	FUNCTION
	get the means of transport in the neighborhood
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	transp variable [int]
	"""
	#<dt class="trans_ann">Transports&nbsp;:</dt><dd class="metro_paris" title="Métro Paris">Notre-Dame de Lorette</dd><dd class="metro_paris" title="Métro Paris">Pigalle</dd><dd class="metro_paris" title="Métro Paris">Saint-Georges</dd><dd class="rer_idf" title="RER Paris">Avenue Foch</dd>
	transp=""
	for transport_name in ["metro_paris", "rer_idf"]:
		try:
			transports=soup.findAll("dd", {"class": transport_name})
			if transports:
				transp+=transport_name+":"
				for transport in transports:
					transp+=transport.get_text().strip()+","
				transp=transp[:-1]+";"
		except:
			pass

	return transp[:-1]


def get_prox(soup):
	"""
	FUNCTION
	get the shops, buildings in the neighborhood
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	prox variable [int]
	"""
	#<dt>Proximité :</dt><dd>Métro hôtel de ville commerces</dd>
	return soup.find("dt", text="Proximité :").findNext("dd").get_text().strip()


def get_surf(soup):
	"""
	FUNCTION
	get the surface
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	surf variable [int]
	"""
	#<li class="float_right switch_style" title="Surface">Surface <b title="10 m²">    10 m² </b></li>
	return soup.find("li", {"title": "Surface"}).find("b").get_text().split()[0]


def get_const(soup):
	"""
	FUNCTION
	get the year of construction of the building/house/flat
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	const variable [int]
	"""
	#<li class="float_right switch_style" title="Année de construction">Année de construction <b title="1900">    1900 </b></li>
	return soup.find("li", {"title": "Année de construction"}).find("b").get_text().strip()


def get_piece(soup):
	"""
	FUNCTION
	get the number of rooms
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	piece variable [int]
	"""
	#<li class="float_right" title="Pièce">Pièce <b title="1">    1 </b></li>
	#<li class="float_right" title="Pièces">Pièces <b title="2">    2 </b></li>
	piece=""
	try:
		piece=soup.find("li", {"title": "Pièce"}).find("b").get_text().strip()
	except:
		piece=soup.find("li", {"title": "Pièces"}).find("b").get_text().strip()
	return piece


def get_toil(soup):
	"""
	FUNCTION
	get the number of WCs
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	toil variable [int]
	"""
	#<li class="float_right switch_style" title="Toilettes">Toilettes <b title="6">    6 </b></li>
	return soup.find("li", {"title": "Toilettes"}).find("b").get_text().strip()


def get_toil_sep(soup):
	"""
	FUNCTION
	indicates whether WC are separated
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	toil_sep variable [string]
	"""
	#<li class="float_right" title="Toilettes Séparées">Toilettes Séparées <b title="">oui </b></li>
	return soup.find("li", {"title": "Toilettes Séparées"}).find("b").get_text().strip()


def get_sdb(soup):
	"""
	FUNCTION
	get the number of bathrooms
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	sdb variable [int]
	"""
	#<li class="float_right" title="Salles de bain">Salles de bain <b title="4">    4 </b></li>
	return soup.find("li", {"title": "Salles de bain"}).find("b").get_text().strip()


def get_meuble(soup):
	"""
	FUNCTION
	get the furniture data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	meuble variable [string]
	"""
	#<li class="switch_style" title="Meublé">Meublé <b title="">oui </b></li>
	return soup.find("li", {"title": "Meublé"}).find("b").get_text().strip()


def get_rang(soup):
	"""
	FUNCTION
	get storage data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	rang variable [int]
	"""
	#<li class="float_right switch_style" title="Rangements">Rangements <b title="">oui </b></li>
	return soup.find("li", {"title": "Rangements"}).find("b").get_text().strip()


def get_asc(soup):
	"""
	FUNCTION
	get the lift data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	asc variable [string]
	"""
	#<li class="float_right switch_style" title="Ascenseur">Ascenseur <b title="">oui </b></li>
	try:
		asc=soup.find("li", {"title": "Ascenseur"}).find("b").get_text().strip()
	except:
		asc="non"
	return asc


def get_chauf(soup):
	"""
	FUNCTION
	get the type of heater system
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	chauf variable [string]
	"""
	#<li class="float_right" title="Type de chauffage">Type de chauffage <b title="central">    central </b></li>
	return soup.find("li", {"title": "Type de chauffage"}).find("b").get_text().strip()


def get_cuis(soup):
	"""
	FUNCTION
	get the type of kitchen
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	cuis variable [string]
	"""
	#<li class="float_right switch_style" title="Type de cuisine">Type de cuisine <b title="coin cuisine">    coin... </b></li>
	return soup.find("li", {"title": "Type de cuisine"}).find("b").get_text().strip()


def get_gard(soup):
	"""
	FUNCTION
	get the watchman data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	gard variable [string]
	"""
	#<li class="switch_style" title="Gardien">Gardien <b title="">oui </b></li>
	return soup.find("li", {"title": "Gardien"}).find("b").get_text().strip()


def get_ent(soup):
	"""
	FUNCTION
	get the entrance data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	ent variable [string]
	"""
	#<li class="float_right switch_style" title="Entrée">Entrée <b title="">oui </b></li>
	return soup.find("li", {"title": "Entrée"}).find("b").get_text().strip()


def get_calme(soup):
	"""
	FUNCTION
	get the quietness data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	calme variable [string]
	"""
	#<li class="float_right switch_style" title="Calme">Calme <b title="">oui </b></li>
	return soup.find("li", {"title": "Calme"}).find("b").get_text().strip()


def get_descr(soup):
	"""
	FUNCTION
	get the description of the ad
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	descr variable [int]
	"""
	#<p itemprop="description" class="textdesc">
	return soup.find("p", {"class": "textdesc"}).get_text().strip()


def get_hon(soup):
	"""
	FUNCTION
	get the price of fees
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	hon variable [string]
	"""
	#<li title="Honoraires ttc en sus">Honoraires ttc... <b>356,41&nbsp;&euro;</b></li>
	hon=""
	try:
		hon=soup.find("li", {"title": "Honoraires ttc en sus"}).find("b").get_text().strip()
	except Exception, e:
		#~ print "hon exception", e
		pass
	return hon


def get_tel(soup):
	"""
	FUNCTION
	get the phone number of the announcer or owner
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	tel variable [string]
	"""
	#<div class="tel">01 46 24 48 66</div>
	return soup.find("div", {"class": "tel"}).get_text().strip()




def get_score(soup):
	"""
	FUNCTION
	get the score of the location (security, reputation, means of transports, quietness)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	score variable [int]
	"""
	return ""




def get_specific_vars(names, soup_specific):
	"""
	FUNCTION
	get specific variables cotained in a part of the html content of the page
	PARAMETERS
	var_names: list of variables to retrieve [list]
	soup_specific: part of the html content [BeautifulSoup object]
	RETURN
	values of variables included given in parameter [list]
	"""
	rental=[]
	for name in names:
		try:
			value=eval("get_"+name)(soup_specific).encode('utf-8')
		except Exception, e:
			#~ print "get_data_rental exception", e
			value=""
		rental.append(value)
		print name+":", value
	return rental


def get_data_rental(url=""):
	"""
	FUNCTION
	get data of a rental in Paris from the page in parameter
	PARAMETERS
	url: page of the rental to crawl [string]
	example of page: http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2)
	VARIABLES TO RETRIEVE
	#DONE
	link: webpage of the rental
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
	piece: number of rooms
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
	descr: description of the ad
	hon: price of fees
	tel: phone number of the announcer or owner
	#TODO
	score: score of the location (security, reputation, means of transports, quietness)

	RETURN
	rental: retrieved data from a rental page [list]
	"""
	rental=[]
	#TEST (to be removed)
	#http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2&tri=
	#~ url="example1.html"
	#http://www.seloger.com/annonces/locations/appartement/paris-9eme-75/lorette-martyrs/83162365.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2
	#~ url="example2.html"
	#http://www.seloger.com/annonces/locations/appartement/paris-18eme-75/78463899.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer
	#~ url="example3.html"
	#http://www.seloger.com/annonces/locations/appartement/paris-8eme-75/parc-monceau/82439751.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer
	#~ url="example4.html"
	#http://www.seloger.com/annonces/locations/appartement/paris-16eme-75/porte-dauphine/78897937.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer
	#~ url="example5.html"
	#http://www.seloger.com/annonces/locations/appartement/paris-7eme-75/invalides/81937887.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer
	#~ url="example6.html"
	soup = BeautifulSoup(urllib.urlopen(url))

	#add the link of the page
	print "link:", url
	rental.append(url)

	#cp, prix
	#<div class="header_ann" itemscope itemtype="http://schema.org/Product">
	soup_part=soup.find("div", {"class": "header_ann"})
	names=["cp", "prix"]
	rental.extend(get_specific_vars(names, soup_part))

	#<div class="infos_ann_light">
	soup_first_vars=soup.find("div", {"class": "infos_ann_light"})
	#ter, park
	#<ol class="liste_details">
	soup_part=soup_first_vars.find("ol", {"class": "liste_details"}).find_all("li")
	names=["etg", "ter", "park"]
	rental.extend(get_specific_vars(names, soup_part))
	#maj, ref
	#<div class="maj_ref">
	soup_part=soup_first_vars.find("div", {"class": "maj_ref"})
	names=["maj", "ref"]
	rental.extend(get_specific_vars(names, soup_part))
	#disp, gar
	#<ol class="liste_details" id="mentions_ann">
	soup_part=soup_first_vars.find("ol", {"id": "mentions_ann"})
	names=["disp", "gar"]
	rental.extend(get_specific_vars(names, soup_part))
	#transp, prox
	#<dl>
	soup_part=soup_first_vars.find("dl")
	names=["transp", "prox"]
	rental.extend(get_specific_vars(names, soup_part))

	#surf, piece, toil, toil_sep, sdb, meuble, asc, chauf cuis, gard, ent calme
	#<div class="bloc_infos_ann" id="detail"><ol class="liste_details">
	soup_part=soup.find("div", {"id": "detail"}).find("ol", {"class": "liste_details"})
	names=["surf", "const", "piece", "toil", "toil_sep", "sdb", "meuble", "rang", "asc", "chauf", "cuis", "gard", "ent", "calme"]
	rental.extend(get_specific_vars(names, soup_part))

	#other independant variables
	names=["descr", "hon", "tel", "score"]
	rental.extend(get_specific_vars(names, soup))

	print ""
	print "-----------------------------------------------------------------------------"
	print ""

	return rental

#~ get_data_rental()


def get_data_rentals():
	"""
	FUNCTION
	get data of all the rental ads in Paris from the website seloger.com
	PARAMETERS
	None
	RETURN
	data: retrieved data from all the rental pages [list of lists]
	"""
	rentals=[]
	#TODO: check domain name
	pages=[]
	#TEST
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2&tri=")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-9eme-75/lorette-martyrs/83162365.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-18eme-75/78463899.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-8eme-75/parc-monceau/82439751.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-16eme-75/porte-dauphine/78897937.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer")
	pages.append("http://www.seloger.com/annonces/locations/appartement/paris-7eme-75/invalides/81937887.htm?bilance=all&bilanegs=all&cp=75&idqfix=1&idsubdivision=17649&idtt=1&idtypebien=1,2&nb_chambres=all&nb_pieces=all&pxbtw=NaN%2fNaN&surfacebtw=NaN%2fNaN&tri=d_px_loyer")

	for page in pages:
		rentals.append(get_data_rental(page))
	return rentals


def get_headers_rentals():
	"""
	FUNCTION
	get the list of variable names to retrieve
	PARAMETERS
	None
	RETURN
	list of variable names [list]
	"""
	return ["link", "cp", "prix", "etg", "ter", "park", "maj", "ref", "disp", "gar", "transp", "prox", "surf", "const", "piece", "toil", "toil_sep", "sdb", "meuble", "rang", "asc", "chauf", "cuis", "gard", "ent", "calme", "descr", "hon", "tel", "score"]


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
	writer=csv.writer(open(path_file, 'w'))

	#write headers
	headers=get_headers_rentals()
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
	#erase the file if already exists
	if os.path.exists(path_file):
		os.remove(path_file)
	#get data from all the rentals
	rentals=get_data_rentals()
	#save it in a csv file
	save_data_rentals(path_file, rentals)


#call main function
path_file="data.csv"
main(path_file)
