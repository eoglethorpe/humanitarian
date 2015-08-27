#add estimated quanitty (sum HH)
#different status on one line?

from itertools import groupby
import csv
import sys

#Agency	Lpartner District VDC/ Municipalities Municipal Ward Item #items #HH status Start_date Comp_Date Comments

csv.register_dialect('excel')
head = ['Code ', 'District', 'VDCs/municipalities', 'Estimated quantity of needs*',	'Quantity delivered (# of items)**', 'Quantity in Pipeline***', 'Missing quantity', 'Estimated date of next delivery', 'Estimated date for maximum coverage ',	'Pipelines and/or deliveries problems',	'Solutions for the problems?',	'Funding gaps']
list = {'Taplejung': '1', 'Panchthar': '2', 'Ilam': '3', 'Jhapa': '4', 'Morang': '5', 'Sunsari': '6', 'Dhankuta': '7', 'Teharthum': '8', 'Sankhuwasabha': '9', 'Bhojpur': '10', 'Solukhumbu': '11', 'Okhaldhunga': '12', 'Khotang': '13', 'Udaypur': '14', 'Saptari': '15', 'Siraha': '16', 'Dhanusha': '17', 'Mahottari': '18', 'Sarlahi': '19', 'Sindhuli': '20', 'Ramechhap': '21', 'Dolakha': '22', 'Sindhupalchowk': '23', 'Kabhrepalanchok': '24', 'Lalitpur': '25', 'Bhaktapur': '26', 'Kathmandu': '27', 'Nuwakot': '28', 'Rasuwa': '29', 'Dhading': '30', 'Makwanpur': '31', 'Rautahat': '32', 'Bara': '33', 'Parsa': '34', 'Chitawan': '35', 'Gorkha': '36', 'Lamjung': '37', 'Tanahu': '38', 'Syangja': '39', 'Kaski': '40', 'Manang': '41', 'Mustang': '42', 'Myagdi': '43', 'Parbat': '44', 'Baglung': '45', 'Gulmi': '46', 'Palpa': '47', 'Nawalparasi': '48', 'Rupandehi': '49', 'Kapilvastu': '50', 'Arghakhanchi': '51', 'Pyuthan': '52', 'Rolpa': '53', 'Rukum': '54', 'Salyan': '55', 'Dang': '56', 'Banke': '57', 'Bardiya': '58', 'Surkhet': '59', 'Dailekh': '60', 'Jajarkot': '61', 'Dolpa': '62', 'Jumla': '63', 'Kalikot': '64', 'Mugu': '65', 'Humla': '66', 'Bajura': '67', 'Bajhang': '68', 'Achham': '69', 'Doti': '70', 'Kailali': '71', 'Kanchanpur': '72', 'Dadeldhura': '73', 'Baitadi': '74', 'Darchula': '75'}

#statuses
COMP_DIST = 'Completed distributions '
PIPE = ['In pipeline (procurement/onroute)','In-Country Stock/ Ongoing distributions']

def read_csv():
	global rows
	f = open('/Users/eoglethorpe/nepal/report_transform/shelther_10th.csv', 'rU')
	reader = csv.DictReader(f)
	rows = []
	tbd_it = 0
	#row: 'Item', 'District', 'VDC/ Municipalities', ' status', '#items', '#HH'
	add = ['Item', 'District', 'VDC/ Municipalities', 'Status', '#items', '#HH']
	for row in reader:
		if row['VDC/ Municipalities'] in ['TBD','TBC']:
			row['VDC/ Municipalities'] = row['VDC/ Municipalities'] + str(tbd_it)
			tbd_it+=1

		#spelling hack 5-14
		if row['District']=='Sindhupalchok':
			row['District']='Sindhupalchowk'
		if row['District']=='Makawanpur':
			row['District']='Makwanpur'
		if row['District']=='Tanahun':
			row['District']='Tanahu'
		if row['District']=='Udayapur':
			row['District']='Udaypur'
		if row['District']=='Kavre':
			row['District']='Kabhrepalanchok'
		if row['District']=='Terhathum':
			row['District']='Teharthum'
		if row['District']=='Kavrepalanchok':
			row['District']='Kabhrepalanchok'
		if row['District']=='sindhuli':
			row['District']='Sind
			huli'
	
		#skip TBD districts
		if row['District']!='TBD':
			rows+=[[row[val] for val in add]]
	
	#sort rows
	rows = vatypes = [v[0] for v in vals]

ed(rows, key=lambda k: k[:4])

def agg():
	global aggd
	aggd = []
	for key, group in groupby(rows, lambda x: x[:4]):
		s = 0
		#sum up all items in need
		for g in group:
			if g[4] != '':
				s+=int(g[4].replace(',','').replace(' ',''))

		aggd+=[key+[s]]
	
	#sort aggd
	aggd = sorted(aggd, key=lambda k: k[:4])
	
	print '**AGGD**'
	for v in aggd:
		print v

def out():
	#iterate through each item and write it out to its own csv


	print '**OUT**'
	for key, group in groupby(aggd, lambda x: x[0]):
		print '**IN KEY** ' + str(key)
		#CSV out
		f = open('/Users/eoglethorpe/nepal/report_transform/%s.csv'%key, 'wt')
		writer = csv.writer(f)
		writer.writerow(head)

		#reset cur_group
		cur_group = []

		#add group values
		for g in group:
			cur_group+=[g]

		#check to verify if all districts are corectly spelled
		check_dist(cur_group)

		#write out to CSV based on if a distrct is in group
		for k,v in list.iteritems():
			#write out VDC info
			#row: 'Item', 'District', 'VDC/ Municipalities', ' status', '#items', '#HH'
			if iscontained(k, cur_group):
				vdc_list = compile_dist_for_writing(get_dist(k, cur_group))
				dist_amt, pip_amt = dist_info_row(vdc_list)

				#write out District info column
				remaining_need = int(damaged[k]) - dist_amt - pip_amt
				writer.writerow([k]+[v,'',damaged[k],dist_amt,pip_amt,remaining_need])

				#write out VDCs
				for v in vdc_list:
					if v[5] == COMP_DIST:
						writer.writerow(['','',v[2],'',v[4]])
					elif v[5] in PIPE:
						writer.writerow(['','',v[2],'','',v[4]])

				print 'matched,finished with ' + k
			
			else:
				#write out code, VDC name
				writer.writerow([k]+[v])


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
	bad = []
	for d in group:
		if not list.has_key(d[1]):
			bad += [d[1]]
	if len(bad) > 0:
		raise Exception('bad dist match %s '% str(bad))

def iscontained(d, cur_group):
	cont = False
	for v in cur_group:
		if d == v[1]:
			cont = True

	return cont

def check_list_match():
	print '**MISSING**:'
	bad = []
	for k,v in list.iteritems():
		if not damaged.has_key(k):
			bad+=[k]

	if len(bad) > 0:
		raise Exception('bad list match %s'%str(bad))

def compile_damage():
	ret = {}
	f = open('/Users/eoglethorpe/nepal/report_transform/damage.csv', 'rU')
	reader = csv.DictReader(f)
	for r in reader:
		ret[r['District']]=r['HHs totally destroyed']

	print 'COMP!!!'
	print ret
	f.close()
	return ret
	


if __name__ == '__main__':
	damaged = compile_damage()
	check_list_match()
	read_csv()
	agg()
	out()
