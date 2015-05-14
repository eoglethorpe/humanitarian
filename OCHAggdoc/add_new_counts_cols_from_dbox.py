import gspread
import os

def cxn():
	gc = gspread.login(os.environ['gmail_add'],os.environ['gmail_pw'])
	sh = gc.open('150505 Priority VDC list with Population')
	c = sh.worksheet('eo_sandbox')

	#get names of all worksheets
	titles = [n.title for n in t.worksheets()]

def makearr():
	d_names = [ 'Gorkha', 'Dhading', 'Nuwakot', 'Lamjung', 'Kabrepalenchowk', 'Lalitpur', 'Okhaldhunga', 'Sindhupalchowk', 'Rasuwa', 'Ramechap', 'Dolakha', 'Bhaktapur', 'Kathmandu']
	final_left = 'B'
	final_right = 'I'
	start_left = 4

if __name__=='main':
	cxn()
	
