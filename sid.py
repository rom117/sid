#-*- coding:Utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib
import unicodedata
import StringIO
import csv
import codecs as c
import pdb



flat_description = []

#print seloger.get_text()
#for every offer on the website


#get description


def convert_fake_unicode_to_real_unicode(string):
    return ''.join(map(chr, map(ord, string))).decode('utf-8')
#get whole box
def crawl(url,file):
    i=1
    seloger = BeautifulSoup(urllib.urlopen(url+str(i)))
    page = 'BCLANNpg='
    wb = csv.writer(open('C:/Users/toshiba/Documents/TUAData/location'+file+'.csv','w'))

    #pages
    for i in range(1,20):
        print i
        try:

            seloger = BeautifulSoup(urllib.urlopen(url+page+str(i)))


            for link in seloger.find_all("div", {"class" : "ann_ann_border"}):


                for doc in link.find_all('a',{'class':'red_link'}):
                    more = str(doc.get('href'))


                    #print more

                    if '#' not in more and '=' not in more and more != 'None' and 'http' in more and 'com/' in more:
                        print more

                    #print more


                        features = []
                        #print more

                        #print more
                        soup = BeautifulSoup(urllib.urlopen(more))

                        arrond = ''
                        prox = ''
                        prix = ''
                        maj = ''
                        ref = ''
                        cauf = ''
                        cuis = ''
                        surf = ''
                        park = ''
                        gar = ''
                        hon = ''
                        disp = ''
                        ter = ''
                        asc = ''
                        sdb = ''
                        etg = ''
                        piece = ''
                        rang = ''
                        const = ''
                        gard = ''
                        ent = ''
                        toil = ''
                        toil_sep = ''
                        sds = ''



                        prix = soup.title.text[-7:-1]
                        arrond = soup.title.text[soup.title.text.find("(")+1:soup.title.text.find(")")]
                        for li in soup.find_all('span'):

                                s = StringIO.StringIO(li.text)
                                for line in s:
                                    if 'maj' in line.lower():
                                        #print line
                                        maj = line
                                        features.append(line)



                                    if 'réf.:' in line.lower():
                                        features.append(line)
                                        ref = line
                                        #print line




                        for li in soup.find_all('li', {"class" : "switch_style"}):
                            s = StringIO.StringIO(li.text)
                            for line in s:

                                if 'type de chauffage' in line.lower():
                                    cauf = line
                                    #print line



                                if 'type de cuisine' in line.lower():
                                    cuis = line
                                    #print line


                        for li in soup.find_all('li', {"class" : "switch_style"}):

                            s = StringIO.StringIO(li.text)
                            count = 0
                            for line in s:


                                if 'surface  ' in line.lower():
                                    count += 1


                                    surf = re.findall('\d+', line)[0]
                                    break
                                    #print line







                                for li in soup.find_all('li'):


                                    if 'parking' in li.text.lower():

                                        if 'N.C' in li.text.replace(' ', ''):
                                            park = 'Parking: N.C'
                                            #print 'Parking: N.C'



                                    s = StringIO.StringIO(li.text)
                                    for line in s:

                                        if 'garantie' in line.lower():

                                            gar = line
                                            if ',' in line:
                                                gar = line.replace(',','.')

                                            if '-' in gar:
                                                gar = line.replace('-','.')

                                            #print line



                                        if 'honoraires' in line.lower():
                                            hon = line
                                            #hon = hon[-5:-1]
                                            if ',' in line:
                                                hon = line.replace(',','.')
                                                #hon = hon[-5:-1]


                                            #print line



                                        if 'disponible' in line.lower():
                                            disp = line
                                            #print line



                                        if 'terrasse  ' in line.lower():
                                            ter = line
                                            #print line



                                        if 'ascenseur  ' in line.lower():
                                            asc = line
                                            #print line



                                        if 'salle de bain' in line.lower():
                                            sdb = line
                                            #print line



                                        if 'etages' in line.lower():
                                            etg = line
                                            #print line



                                        if 'pièce    ' in line.lower():
                                            piece = line
                                            #print line



                                        if 'rangements' in line.lower():
                                            rang = line
                                            #print line



                                        if 'construction' in line.lower():
                                            const = line
                                            #print line



                                        if 'gardien' in line.lower():
                                            gard = line
                                            #print line



                                        if 'entré' in line.lower():
                                            ent = line
                                            #print line





                                        if 'toilettes séparées' in line.lower():
                                            toil_sep = line[-4:]
                                            #print line
                                        else:
                                            if 'toilettes' in line.lower():
                                                toil = line[-2:]
                                                #print line

                                        #salle de sejour
                                        if 'salle de séjour' in line.lower():
                                            if 'oui' in line.lower():
                                                sds = line[-4:]
                                            else:
                                                sds = re.findall('\d+', line)[0]


                        features.append(prix)
                        if cauf == '': features.append('')
                        else: features.append(cauf)
                        if cuis == '': features.append('')
                        else: features.append(cuis)
                        if surf == '': features.append('')
                        else: features.append(surf)
                        #print surf

                        if park == '': features.append('')
                        else: features.append(park)
                        if gar == '': features.append('')
                        else: features.append(gar)
                        if hon == '': features.append('')
                        else: features.append(hon)
                        if disp == '': features.append('')
                        else: features.append(disp)
                        if ter == '': features.append('')
                        else: features.append(ter)
                        if asc == '': features.append('')
                        else: features.append(asc)
                        if sdb == '': features.append('')
                        else: features.append(sdb)
                        if etg == '': features.append('')
                        else: features.append(etg)
                        if piece == '': features.append('')
                        else: features.append(piece)
                        if rang == '': features.append('')
                        else: features.append(rang)
                        if const == '': features.append('')
                        else: features.append(const)
                        if gard == '': features.append('')
                        else: features.append(gard)
                        if ent == '': features.append('')
                        else: features.append(ent)
                        if toil == '': features.append('')
                        else: features.append(toil)
                        if toil_sep == '': features.append('')
                        else: features.append(toil_sep)
                        if sds == '': features.append('')
                        else: features.append(sds)
                        if arrond == '': features.append('')
                        else: features.append(arrond)

                        print features
                        #pdb.set_trace()
                        wb.writerow(features)


        except Exception as ex:
            print ex


def crawl_test():
    url_no_search = 'http://www.seloger.com/recherche.htm?cp=75&idtt=1&idtypebien=1,2&org=engine&BCLANNpg='


    url_40 = 'http://www.seloger.com/new_recherche,new_recherche.htm?org=engine&idtt=1&cp=75&idtypebien=1,2&#idtt=1&idtypebien=1&idtypebien=2&cp=75&pxmin=min&pxmax=max&surfacemin=min&surfacemax=40&surf_terrainmin=min&surf_terrainmax=max&etagemin=min&etagemax=max&'
    url_40_70 = 'http://www.seloger.com/recherche.htm?pxbtw=NaN/NaN&surfacebtw=40/70&idtt=1&nb_pieces=all&idtypebien=1,2&bilance=all&bilanegs=all&=&nb_chambres=all&tri=a_px_loyer&cp=75&idsubdivision=17649&idqfix=1&BCLANNpg='
    url_70_100 = 'http://www.seloger.com/recherche.htm?pxbtw=NaN/NaN&surfacebtw=70/100&idtt=1&nb_pieces=all&idtypebien=1,2&bilance=all&bilanegs=all&=&nb_chambres=all&tri=a_px_loyer&cp=75&idsubdivision=17649&idqfix=1&BCLANNpg='
    url_100 = 'http://www.seloger.com/recherche.htm?pxbtw=NaN/NaN&surfacebtw=100/max&idtt=1&nb_pieces=all&idtypebien=1,2&bilance=all&bilanegs=all&=&nb_chambres=all&tri=a_px_loyer&cp=75&idsubdivision=17649&idqfix=1&BCLANNpg=1#pxbtw:NaN;NaN/surfacebtw:100;NaN/idtt:1/nb_pieces:all/idtypebien:1,2/bilance:all/bilanegs:all/:/nb_chambres:all/tri:a_px_loyer/cp:75/idsubdivision:17649/idqfix:1/BCLANNpg:'
    '''
    crawl(url_40_70,'url_40_70')
    crawl(url_70_100,'url_70_100')
    crawl(url_100, 'url_100')
    '''
    crawl(url_40,'under-40')




def crawl_test2():
    postal_codes = [92000,
                    78420,
                    78500,
                    78600,
                    78260,
                    78700]
    urls = ['http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=920050&idtypebien=1,2,14&pxmin=1000&pxmax=1500&nb_pieces=3&',
            'http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=780124&idtypebien=1,2,14&pxmin=1000&pxmax=1500&nb_pieces=3&',
            'http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=780586&idtypebien=1,2,14&pxmin=1000&pxmax=1500&nb_pieces=3&',
            'http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=780358&idtypebien=1,2&pxmin=1000&pxmax=1500&nb_pieces=3&',
            'http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=780005&idtypebien=1,2&pxmin=1000&pxmax=1500&nb_pieces=3&',
            'http://www.seloger.com/recherche.htm?org=engine&idtt=1&ci=780172&idtypebien=1,2&pxmin=1000&pxmax=1500&nb_pieces=3&']

    k=0
    for i in urls:
        crawl(i,str(postal_codes[k]))
        k += 1


crawl_test2()

