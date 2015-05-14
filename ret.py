
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def ret():
	json_key = json.load(open('/Users/eoglethorpe/nepal/ggoauth.json'))
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
	return gspread.authorize(credentials)


if __name__ == 'main':
	ret()
