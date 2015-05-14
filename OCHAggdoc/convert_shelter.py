#add estimated quanitty (sum HH)
#different status on one line?

from itertools import groupby
import csv
import sys

#Agency	Lpartner District VDC/ Municipalities Municipal Ward Item #items #HH status Start_date Comp_Date Comments

csv.register_dialect('excel')
head = ['Code ', 'District', 'VDCs/municipalities', 'Estimated quantity of needs*',	'Quantity delivered (# of items)**', 'Quantity in Pipeline***', 'Missing quantity', 'Estimated date of next delivery', 'Estimated date for maximum coverage ',	'Pipelines and/or deliveries problems',	'Solutions for the problems?',	'Funding gaps']
list = [['Achham', '69'], ['Arghakhanchi', '51'], ['Baglung', '45'], ['Baitadi', '74'], ['Bajhang', '68'], ['Bajura', '67'], ['Banke', '57'], ['Bara', '33'], ['Bardiya', '58'], ['Bhaktapur', '26'], ['Bhojpur', '10'], ['Chitwan', '35'], ['Dadeldhura', '73'], ['Dailekh', '60'], ['Dang', '56'], ['Darchula', '75'], ['Dhading', '30'], ['Dhankuta', '7'], ['Dhanusha', '17'], ['Dolkha', '22'], ['Dolpa', '62'], ['Doti', '70'], ['Gorkha', '36'], ['Gulmi', '46'], ['Humla', '66'], ['Ilam', '3'], ['Jajarkot', '61'], ['Jhapa', '4'], ['Jumla', '63'], ['Kailali', '71'], ['Kalikot', '64'], ['Kanchanpur', '72'], ['Kapilvastu', '50'], ['Kaski', '40'], ['Kathmandu', '27'], ['Kavre', '24'], ['Khotang', '13'], ['Lalitpur', '25'], ['Lamjung', '37'], ['Mahottari', '18'], ['Makawanpur', '31'], ['Manang', '41'], ['Morang', '5'], ['Mugu', '65'], ['Mustang', '42'], ['Myagdi', '43'], ['Nawalparasi', '48'], ['Nuwakot', '28'], ['Okhaldhunga', '12'], ['Palpa', '47'], ['Panchthar', '2'], ['Parbat', '44'], ['Parsa', '34'], ['Pyuthan', '52'], ['Ramechhap', '21'], ['Rasuwa', '29'], ['Rautahat', '32'], ['Rolpa', '53'], ['Rukum', '54'], ['Rupandehi', '49'], ['Salyan', '55'], ['Sankhuwasabha', '9'], ['Saptari', '15'], ['Sarlahi', '19'], ['Sindhuli', '20'], ['Sindhupalchowk', '23'], ['Siraha', '16'], ['Solukhumbu', '11'], ['Sunsari', '6'], ['Surkhet', '59'], ['Syangja', '39'], ['Tanahu', '38'], ['Taplejung', '1'], ['Teharthum', '8'], ['Udaypur', '14']]
damaged = [['Achham', '0'], ['Arghakhanchi', '140'], ['Baglung', '428'], ['Baitadi', '0'], ['Bajhang', '0'], ['Bajura', '0'], ['Banke', '0'], ['Bara', '7'], ['Bardiya', '0'], ['Bhaktapur', '7000'], ['Bhojpur', '1309'], ['Chitwan', '2046'], ['Dadeldhura', '0'], ['Dailekh', '0'], ['Dang', '7'], ['Darchula', '0'], ['Dhading', '20000'], ['Dhankuta', '15'], ['Dhanusha', '1'], ['Dolkha', '5000'], ['Dolpa', '1'], ['Doti', '0'], ['Gorkha', '44607'], ['Gulmi', '770'], ['Humla', '0'], ['Ilam', '93'], ['Jajarkot', '0'], ['Jhapa', '1'], ['Jumla', '0'], ['Kavre', '30000'], ['Kailali', '0'], ['Kalikot', '2'], ['Kanchanpur', '0'], ['Kapilvastu', '0'], ['Kaski', '174'], ['Kathmandu', '27640'], ['Khotang', '1983'], ['Lalitpur', '16344'], ['Lamjung', '7430'], ['Mahottari', '43'], ['Makawanpur', '363'], ['Manang', '5'], ['Morang', '2'], ['Mugu', '0'], ['Mustang', '56'], ['Myagdi', '97'], ['Nawalparasi', '17'], ['Nuwakot', '30000'], ['Okhaldhunga', '8000'], ['Palpa', '1060'], ['Panchthar', '41'], ['Parbat', '777'], ['Parsa', '16'], ['Pyuthan', '3'], ['Ramechhap', '17072'], ['Rasuwa', '8000'], ['Rautahat', '24'], ['Rolpa', '42'], ['Rukum', '61'], ['Rupandehi', '10'], ['Salyan', '18'], ['Sankhuwasabha', '326'], ['Saptari', '0'], ['Sarlahi', '56'], ['Sindhuli', '4159'], ['Sindhupalchowk', '44310'], ['Siraha', '0'], ['Solukhumbu', '2483'], ['Sunsari', '2'], ['Surkhet', '1'], ['Syangja', '3119'], ['Tanahu', '3377'], ['Taplejung', '3'], ['Teharthum', '162'], ['Udaypur', '95']]

#statuses
COMP_DIST = 'Completed distributions '
PIPE = ['In pipeline (procurement/onroute)','In-Country Stock/ Ongoing distributions']

def read_csv():
	global rows
	f = open('/Users/eoglethorpe/Downloads/test.csv', 'rU')
	reader = csv.DictReader(f)
	rows = []
	tbd_it = 0
	#row: 'Item', 'District', 'VDC/ Municipalities', ' status', '#items', '#HH'
	add = ['Item', 'District', 'VDC/ Municipalities', ' status', '#items', '#HH']
	for row in reader:
		if row['VDC/ Municipalities'] in ['TBD','TBC']:
			row['VDC/ Municipalities'] = row['VDC/ Municipalities'] + str(tbd_it)
			tbd_it+=1

		#spelling hack 5-14
		if row['District']=='Sindhupalchok':
			row['District']='Sindhupalchowk'
	
		rows+=[[row[val] for val in add]]
	
	#sort rows
	rows = sorted(rows, key=lambda k: k[:4])

def agg():
	global aggd
	aggd = []
	for key, group in groupby(rows, lambda x: x[:4]):
		s = 0
		#sum up all items in need
		for g in group:
			s+=int(g[4].replace(',','').replace(' ',''))
		aggd+=[key+[s]]
	
	#sort aggd
	aggd = sorted(aggd, key=lambda k: k[:4])
	
	print '**AGGD**'
	for v in aggd:
		print v

def out():
	#iterate through each item and write it out to its own csv


	global list
	list = sorted(list, key=lambda k: int(k[1]))
	print '**OUT**'
	for key, group in groupby(aggd, lambda x: x[0]):
		print '**IN KEY** ' + str(key)
		#CSV out
		f = open('/Users/eoglethorpe/nepal/OCHAggdoc/%s.csv'%key, 'wt')
		writer = csv.writer(f)
		writer.writerow(head)

		#reset cur_group
		cur_group = []

		#add group values
		for g in group:
			cur_group+=[g]

		#check to verify if all districts are coorectly spelled
		check_dist(cur_group)

		#write out to CSV based on if a distrct is in group
		for d in list:
			#write out VDC info
			#row: 'Item', 'District', 'VDC/ Municipalities', ' status', '#items', '#HH'
			if iscontained(d[0], cur_group):
				vdc_list = compile_dist_for_writing(get_dist(d[0], cur_group))
				dist_amt, pip_amt = dist_info_row(vdc_list)

				#write out District info column
				writer.writerow([d[0]]+[d[1],'','EQ',dist_amt,pip_amt,'MS'])

				#write out VDCs
				for v in vdc_list:
					if v[5] == COMP_DIST:
						writer.writerow(['','',v[2],'',v[4]])
					elif v[5] in PIPE:
						writer.writerow(['','',v[2],'','',v[4]])

				print 'matched,finished with ' + d[0]
			
			else:
				#write out code, VDC name
				writer.writerow([d[0]]+[d[1]])


		#close CSV
		f.close()

def dist_info_row(vdc_list):
	#check 3rd and 4th cols and sum vals
	dist_amt = 0
	pip_amt = 0

	print str(vdc_list)

	for v in vdc_list:
		if v[5] == COMP_DIST:
			if v[4]!='':
				dist_amt+=int(v[4])
	
		elif v[5] in PIPE:
			if v[4]!='':
				pip_amt+=int(v[4])
		else:
				print "NOT PIPE OR COMP"

	return dist_amt, pip_amt
def compile_dist_for_writing(cur_dist):
	dist_ret = []

	#iterate through VDCs that have been returned for district
	for v in cur_dist:
		print 'V3 IS' + str(v[3])
		#check status for which col to write to
		#v3 is status
		if v[3] == COMP_DIST:
			dist_ret+=[['','',v[2],'',v[4],v[3]]]
			print 'IN CD'
		elif v[3] in PIPE:
			dist_ret+=[['','',v[2],'',v[4],v[3]]]
			print 'IN PIPE'
		else:
			print 'MISSING FOR*** ' + str(v)

	return dist_ret

def get_dist(d, group):
	ret = []
	for v in group:
		if v[1] == d:
			ret+=[v]

	return ret

def check_dist(group):
	for d in group:
		f = False
		for l in list:
			if l[0] == d[1]:
				f = True
		if not f:
			raise Excpetion('bad dist match%s'%l)



def iscontained(d, cur_group):
	cont = False
	for v in cur_group:
		if d == v[1]:
			cont = True

	return cont

def check_list_match():
	print '**MISSING**:'
	for l in list:
		f = False
		for d in damaged:
			if l[0]==d[0]:
				f = True
		if not f:
			raise Excpetion('bad list match%s'%l)

if __name__ == '__main__':
	check_list_match()
	read_csv()
	agg()
	out()
