import os
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json
import normalize

d_names = [ 'Gorkha', 'Dhading', 'Nuwakot', 'Lamjung', 'Kabrepalanchowk', 'Lalitpur', 'Okhaldhunga', 'Sindhupalchowk', 'Rasuwa', 'Ramechhap', 'Dolakha', 'Bhaktapur', 'Kathmandu']

json_key = json.load(open('nepal-e5164b382ea0.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
sh = gc.open('Priority VDC List Master')

cols_reg = [
['death_population',None, None],
['missing_population',None, None],
['injured_population',None, None],
['affected_household',None, None],
['male_affected_population',None, None],
['female_affected_population',None, None],
['displaced_families',None, None],
['displaced_population',None, None],
['damaged_household_completely',None,None],
['damaged_household_partially',None,None]]

cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ']

start_norm= [3,49]
start_reg= [3,8]

def norm_dist(d_name):
	global cur
	cur = sh.worksheet(d_name)
	#how many VDCs?
	no_vdc = len(cur.col_values(3))-2
	print 'len is: ' + str(no_vdc)
	print 'dist: ' + d_name


	#get values
	vals = cur.get_all_values()
	
	for col in cols_reg:
		col[1] = cur.col_values(vals[1].index(col[0])+1)[2:]
		print col[1]	
	#normalize values in each column
	
	for col in cols_reg:
		col[2]= normalize.norm(col[1])

	#get output cells and  normalize
	for col in cols_reg:
		index = vals[1].index(col[0]+"_normalized")
		
		out_vals = cur.range(cols[index]+"3:"+cols[index]+str(no_vdc+1))
	
		it = 0
		for cell in out_vals:
			if it < len(col[2]):
				cell.value = col[2][it]
				it+=1
	
	print out_vals	
	cur.update_cells(out_vals)
	
def norm(un_norm):
	norm_prep = []
	blanks = []
	it = 3
	for c in un_norm:
		if c == None:
			c = 'null'
			
		if c.isdigit():
			norm_prep+=[int(c)]
		else: 
			blanks+=[it]
	
		it+=1
	
	return norm


for district in d_names:
	norm_dist(district)
