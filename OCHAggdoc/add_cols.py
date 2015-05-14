import os
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json

d_names = [ 'Gorkha', 'Dhading', 'Nuwakot', 'Lamjung', 'Kabrepalanchowk', 'Lalitpur', 'Okhaldhunga', 'Sindhupalchowk', 'Rasuwa', 'Ramechhap', 'Dolakha', 'Bhaktapur', 'Kathmandu']

json_key = json.load(open('nepal-e5164b382ea0.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
sh = gc.open('Priority VDC List Master')

for v in d_names:
	out = sh.worksheet(v)
	out.add_cols(50)
