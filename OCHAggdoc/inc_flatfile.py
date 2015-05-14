import gspread
import os

cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ']


rv = 3 #default starting row value
master_cell = []

def cxn():
	global gc
	global sh
	global out
	gc = gspread.login(os.environ['gmail_add'],os.environ['gmail_pw'])
	sh = gc.open('150505 Priority VDC list with Population')
	out = sh.worksheet('Aggregated')

	#get names of all worksheets
	#titles = [n.title for n in t.worksheets()]

def do_sheet(s_name):
	cxn()
	cell = insert_flat(s_name, find_cord(s_name))
	
	out.update_cells(cell)

def find_start_y():
	c = sh.worksheet('Aggregated')
	cv = c.acell('A1').value	
	it = 1
	
	while cv != '':
		it+=1
		cv = c.acell('A%i'%it).value
	
	return it

def insert_flat(s_name, cords):
	#cords: [TL, TR, BL, BR]
	global rv
	global master_cell
	c = sh.worksheet(s_name)
	out = sh.worksheet('Aggregated')
	values_list = None
	cxn()
	#print out references, not values themselves
        
	#TR - TL
	hor_len = int(cords[1][0]) - int(cords[0][0])
        
	#BL - TL
	ver_len = int(cords[2][1]) - int(cords[0][1])

	rv=find_start_y()

	cell = None
        cell = out.range('A%i:%s%i'%(rv, cols[hor_len], rv+ver_len))

	loc_int = 0
	#vert
	for i in xrange(1,ver_len+2):
		#horizontal (1 = A in col)
                for p in xrange(0,hor_len+1): 
			cell[loc_int].value = '=%s!%s%i'%(s_name,cols[p],i+2)
			rv+=1
			loc_int+=1
	
	print cell
	return cell

def find_cord(s_name):			
	#return array with format [TL, TR, BL, BR]
	#top left
	c = sh.worksheet(s_name)

	if c.acell('A2').value.lower() == 'district_name':
		TL = ['1','3']
	else:
		print 'error TL %s' % s_name
		print c.acell('A2').value
	
	#top right... cycle across col names and find end
	cv = 't'
	it = 1 

	while cv != '':
		it+=1
		cv = c.acell('%s2'%cols[it]).value

	TR = [str(it-1) , '3']
	
	#bottom left
	cv = 't'
	it = 3
	while cv != '':
		it+=1
		cv = c.acell('A%i'%it).value
	BL = ['A' , str(it-1)]
	
	BR = [TR[0] , str(it-1)]
	
	print [TL,TR,BL,BR]
	
	return [TL,TR,BL,BR]	
	
if __name__ == "__main__":	
	cxn()
	cycle_sheets()
