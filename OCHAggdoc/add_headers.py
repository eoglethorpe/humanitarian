import os
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json

d_names = [ 'Gorkha', 'Dhading', 'Nuwakot', 'Lamjung', 'Kabrepalanchowk', 'Lalitpur', 'Okhaldhunga', 'Sindhupalchowk', 'Rasuwa', 'Ramechhap', 'Dolakha', 'Bhaktapur', 'Kathmandu']

cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ','DA','DB','DC','DD','DE','DF','DG','DH','DI','DJ','DK','DL','DM','DN','DO','DP','DQ','DR','DS','DT','DU','DV','DW','DX','DY','DZ','EA','EB','EC','ED','EE','EF','EG','EH','EI','EJ','EK','EL','EM','EN','EO','EP','EQ','ER','ES','ET','EU','EV','EW','EX','EY','EZ']

json_key = json.load(open('nepal-e5164b382ea0.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
sh = gc.open('Priority VDC List Master')

for district in d_names:
	it=0
	o = sh.worksheet(district)
	#top row
	r = o.range('A1:'+cols[o.col_count-1]+"1")
	for c in r:
		c.value = "=Header!"+cols[it]+"1"
		it+=1
	o.update_cells(r)

	#second row
	s = o.range('A2:'+cols[o.col_count-1]+"2")
	it=0
	for c in s:
		c.value = "=Header!"+cols[it]+"2"
		it+=1
	o.update_cells(s)

	print "done with: " + district
