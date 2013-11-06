#-*- coding:utf-8 -*-
import re
"""
get all the variables from a rental page
"""

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


def get_first_vars(soup, text):
	"""
	FUNCTION
	get the floor of the rental (etg), the lift data (asc), the terrace data (ter), the car park data (park), date of availability (disp) or the garantee price (gar)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	text: text to search [string]
	RETURN
	etg, asc, ter, park disp or gar variable [string or date]
	"""
	#<li>Etage <b>rdc</b></li>
	#<li class="float_right">Ascenseur <b>N.C</b></li>
	#<li class="switch_style">Terrasse <b>N.C</b></li>
	#<li class="switch_style float_right">Parking <b>N.C</b></li>
	#<li class="noimportant">Disponible le <b>07 / 11 / 2013</b></li>
	#<li class="switch_style">Garantie <b>2moiscc&nbsp;&euro;</b></li>
	return soup.find(text=re.compile(text)).findNext("b").get_text().strip()


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
	#<dt class="trans_ann">Transports&nbsp;:</dt><dd class="metro_paris" title="Métro Paris">Notre-Dame de Lorette</dd><dd class="metro_paris" title="Métro Paris">Pigalle</dd><dd class="metro_paris" title="Métro Paris">Saint-Georges</dd><dd class="rer_idf" title="RER Paris">Avenue Foch</dd>
	transp=""
	for transport_name in ["metro_paris", "rer_idf"]:
		try:
			transports=soup.find_all("dd", {"class": transport_name})
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


def get_details(soup, text):
	"""
	FUNCTION
	get the surface (surf), year of construction (const), number of WCs (toil), toil_sep data (toil_sep), number of bathrooms (sdb), furniture data (meuble), storage data (rang), type of heater system (chauf), type of kitchen (cuis), watchman data (gard), entrance data (ent) or quietness data (calme)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	text: text of search [string]
	RETURN
	surf, const, toil, toil_sep, sdb, meuble, rang, chauf, cuis, gard, ent or calme variable [string or int]
	"""
	#<li class="float_right switch_style" title="Surface">Surface <b title="10 m²">    10 m² </b></li>
	#<li class="float_right switch_style" title="Année de construction">Année de construction <b title="1900">    1900 </b></li>
	#<li class="float_right switch_style" title="Toilettes">Toilettes <b title="6">    6 </b></li>
	#<li class="float_right" title="Toilettes Séparées">Toilettes Séparées <b title="">oui </b></li>
	#<li class="float_right" title="Salles de bain">Salles de bain <b title="4">    4 </b></li>
	#<li class="switch_style" title="Meublé">Meublé <b title="">oui </b></li>
	#<li class="float_right switch_style" title="Rangements">Rangements <b title="">oui </b></li>
	#<li class="float_right" title="Type de chauffage">Type de chauffage <b title="central">    central </b></li>
	#<li class="float_right switch_style" title="Type de cuisine">Type de cuisine <b title="coin cuisine">    coin... </b></li>
	#<li class="switch_style" title="Gardien">Gardien <b title="">oui </b></li>
	#<li class="float_right switch_style" title="Entrée">Entrée <b title="">oui </b></li>
	#<li class="float_right switch_style" title="Calme">Calme <b title="">oui </b></li>
	return soup.find("li", {"title": text}).find("b").get_text().strip()


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
		piece=soup.find("li", {"title": "Pièce"})
	except:
		piece=soup.find("li", {"title": "Pièces"})
	return piece.find("b").get_text().strip()


def get_descr(soup):
	"""
	FUNCTION
	get the description of the ad
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	descr variable [string]
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

	return soup.find("li", {"title": "Honoraires ttc en sus"}).find("b").get_text().strip()


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


def get_score_gen(soup):
	"""
	FUNCTION
	get the general score of the location
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	score_gen variable [string]
	"""
	#<div class="notes_globales"><div class="star_libelle">Séduisante</div>
	return soup.find("div", {"class": "notes_globales"}).find("div", {"class": "star_libelle"}).get_text().strip()


def get_date_last_vote(soup):
	"""
	FUNCTION
	get the date of the last vote for the location
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	RETURN
	date_last_vote variable [date]
	"""
	#<div class="notes_recap">Au total : 15 voix (dont 15 sur la zone) - Dernier vote le 29/10/2013</div>
	return soup.find("div", {"class": "notes_recap"}).get_text().strip()[-10:]


def get_score_vars(soup, text):
	"""
	FUNCTION
	get the "Commerce alimentaire" score (score_shop), "Restaurants et bars" score (score_rest), "Réputation du quartier" score (score_rep), "Transports en commun" score (score_transp), "Culture ou sport" score (score_cult), "Voisins et habitants" score (score_neigh), "Sécurité" score (score_safe), "Propreté et urbanisme" score(score_clean), "Tranquillité de la rue" score (score_calm), "Prix des magasins" score (score_price), "Espaces verts" score (score_green), "Circulation routière" score (score_traf), "Qualité de l'air" score (score_air) or "Stationnement" score (score_park)
	PARAMETERS
	soup: html content of the page [BeautifulSoup object]
	text: text of search [string]
	RETURN
	score_shop, score_rest, score_rep, score_transp, score_cult, score_neigh, score_safe, score_clean, score_calm, score_price, score_green, score_traf, score_air or score_park variable [int]
	"""
	#~ <div>
		#~ <span class="categorie_intitule">Commerce alimentaire</span>
		#~ <div id="note_box_1_1" class="note_box_value"></div>
		#~ <div id="note_box_2_1" class="note_box_value"></div>
		#~ <div id="note_box_3_1" class="note_box_value"></div>
		#~ <div id="note_box_4_1" class="note_box_value"></div>
		#~ <div id="note_box_5_1" class="note_box_vide"></div>
		#~ <div class="categorie_note_texte"></div>
		#~ <div class="clear"></div>
	#~ </div>
	score=soup.find("span", {"class": "categorie_intitule"}, text=text).find_parent("div").find_all("div", {"class": "note_box_value"})
	return str(len(score))
