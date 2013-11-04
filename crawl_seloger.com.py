#-*- coding:utf-8 -*-
"""
crawl all the rental ads in Paris from the website seloger.com
"""
from bs4 import BeautifulSoup
import re
import urllib
import csv


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
	get the monthly price
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	prix variable [int]
	"""
	#<b class="prix_brut">348&nbsp;&euro;&nbsp;cc<sup>*</sup> </b>
	return soup.find("b", {"class": "prix_brut"}).get_text().split()[0]


def get_piece(soup):
	"""
	FUNCTION
	get the number of rooms
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	piece variable [int]
	"""
	return soup[0].find("b").get_text().strip()


def get_surf(soup):
	"""
	FUNCTION
	get the surface
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	surf variable [int]
	"""
	#<li class="switch_style" title="Surface">Surface <b title="10 m²">    10 m² </b></li>
	return soup[1].find("b").get_text().split()[0]


def get_etg(soup):
	"""
	FUNCTION
	get the number of floors
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	etg variable [int]
	"""
	return soup[2].find("b").get_text().strip()


def get_asc(soup):
	"""
	FUNCTION
	get the lift data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	asc variable [int]
	"""
	return soup[3].find("b").get_text().strip()


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


def get_transp(soup):
	"""
	FUNCTION
	get the means of transport in the neighborhood
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	transp variable [int]
	"""
	#<dt class="trans_ann">Transports&nbsp;:</dt><dd class="metro_paris" title="Métro Paris">Hotel de Ville</dd>
	transp=""
	metro="metro:"+soup.find("dt", {"class": "trans_ann"}).findNext("dd", {"class": "metro_paris"}).get_text().strip()
	rer="rer:"
	transp=metro+";"+rer
	return transp


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


def get_descr(soup):
	"""
	FUNCTION
	get the description of the ad
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	descr variable [int]
	"""
	#<meta name="description" content="Chambre avec coin cuisine, rue du plâtre, au 7ème étage sans ascenseur. WC et douche communs à l'étage." />
	return soup.find("meta", {"name": "description"})["content"]


def get_hon(soup):
	"""
	FUNCTION
	get the price of fees
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	hon variable [int]
	"""
	#<li title="Honoraires ttc en sus">Honoraires ttc... <b>356,41&nbsp;&euro;</b></li>
	return soup.find("li", {"title": "Honoraires ttc en sus"}).find("b").get_text().split()[0]


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


def get_chauf(soup):
	"""
	FUNCTION
	get the heater system
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	chauf variable [int]
	"""
	return ""


def get_cuis(soup):
	"""
	FUNCTION
	get the kitchen data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	cuis variable [int]
	"""
	return ""


def get_gar(soup):
	"""
	FUNCTION
	get the garantee price
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	gar variable [int]
	"""
	return ""


def get_disp(soup):
	"""
	FUNCTION
	get the availability
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	disp variable [int]
	"""
	return ""


def get_sdb(soup):
	"""
	FUNCTION
	get the bathroom data of the rental
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	sdb variable [int]
	"""
	return ""


def get_rang(soup):
	"""
	FUNCTION
	get the rangement data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	rang variable [int]
	"""
	return ""


def get_const(soup):
	"""
	FUNCTION
	get the year of construction of the building/house/flat
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	const variable [int]
	"""
	return ""


def get_gard(soup):
	"""
	FUNCTION
	get the watchman data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	gard variable [int]
	"""
	return ""


def get_toil(soup):
	"""
	FUNCTION
	get the WC data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	toil variable [int]
	"""
	return ""


def get_toil_sep(soup):
	"""
	FUNCTION
	indicates whether WC are separated
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	toil_sep variable [int]
	"""
	return ""


def get_ent(soup):
	"""
	FUNCTION
	get the number of entrances
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	ent variable [int]
	"""
	return ""


def get_calme(soup):
	"""
	FUNCTION
	get the quietness data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	calme variable [int]
	"""
	return ""


def get_meuble(soup):
	"""
	FUNCTION
	get the furniture data
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	meuble variable [int]
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
				value=eval("get_"+name)(soup_specific)
				rental.append(value)
				print name+":", value
			except Exception, e:
				print "get_data_rental exception", e
	return rental


def get_data_rental(url=""):
	"""
	FUNCTION
	get data of a rental in Paris from the page in parameter
	PARAMETERS
	url: page of the rental to crawl [string]
	example of page: http://www.seloger.com/annonces/locations/appartement/paris-4eme-75/82466803.htm?cp=75&idqfix=1&idtt=1&idtypebien=1,2)
	VARIABLES TO RETRIEVE
	cp: zip postal of the rental
	prix: price of the rental
	piece: number of rooms
	surf: surface
	etg: number of floors
	asc: is there a lift?
	ter: is there a terrace?
	park: is there a car park?
	maj: on-line publishing date (or date of update)
	ref: reference of the rental
	transp: means of transport in the neighborhood
	prox: shops, buildings in the neighborhood
	descr: description of the ad
	hon: price of fees
	tel: phone number of the announcer or owner

	#TODO
	score: score of the location (security, reputation, means of transports, quietness)
	chauf: is there a heater system?
	cuis: is there a kitchen?
	gar: price of the guarantee
	disp: availability
	sdb: is there a bathroom?
	rang: rangements
	const: year of construction
	gard: is there a watchman?
	toil: is there one WC?
	toil_sep: is the WC separated?
	ent: number of entrances
	calme: is it quiet?
	meuble: are there furniture?

	link: webpage of the rental
	RETURN
	rental: retrieved data from a rental page [list]
	"""
	rental=[]
	#TEST (to be removed)
	url="example1.html"
	soup = BeautifulSoup(urllib.urlopen(url))

	#cp, prix
	#<div class="header_ann" itemscope itemtype="http://schema.org/Product">
	soup_cp_prix=soup.find("div", {"class": "header_ann"})
	names=["cp", "prix"]
	rental.extend(get_specific_vars(names, soup_cp_prix))

	#piece, surf, etg, asc, ter, park, maj, ref, transp, prox
	#<div class="infos_ann_light"><ol class="liste_details">
	soup_main_vars=soup.find("div", {"class": "infos_ann_light"})
	#piece, surf, etg, asc, ter, park:
	#<li class="switch_style">
	soup_main_info=soup_main_vars.find("ol", {"class": "liste_details"}).find_all("li")
	names=["piece", "surf", "etg", "asc", "ter", "park"]
	rental.extend(get_specific_vars(names, soup_main_info))
	#maj, ref
	#<div class="maj_ref">
	soup_maj_ref=soup_main_vars.find("div", {"class": "maj_ref"})
	names=["maj", "ref"]
	rental.extend(get_specific_vars(names, soup_maj_ref))
	#transp, prox
	#<dl>
	soup_transp_prox=soup_main_vars.find("dl")
	names=["transp", "prox"]
	rental.extend(get_specific_vars(names, soup_transp_prox))

	#other independant variables
	names=["descr", "hon", "tel"]
	rental.extend(get_specific_vars(names, soup))


	#add the link of the page
	rental.append(url)

	return rental

get_data_rental()


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
	return ["cp", "prix", "piece", "surf", "etg", "asc", "ter", "park", "maj", "ref", "transp", "prox", "descr", "hon", "tel", "score", "chauf", "cuis", "gar", "disp", "sdb", "rang", "const", "gard", "toil", "toil_sep", "ent", "calme", "meuble"]


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
	headers=get_headers_rentals().append("link")
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
	save_data_rentals(path_file, rentals)

path_file="data.csv"
#call main function
#~ main(path_file)
