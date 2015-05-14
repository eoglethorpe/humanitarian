import os
import gspread

col = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK','CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ']

def cxn():
    global gc
    global sh
    global out
    gc = gspread.login(os.environ['gmail_add'],os.environ['gmail_pw'])
    sh = gc.open('nepal test')
    out = sh.worksheet('Aggregated')

def add():
	x = 10
	y = 10
	loc_inc = 0
	cell = out.range('A1:J10')
	print len(cell)
	for i in xrange(1,x+1):
		for p in xrange(1,y+1):
			print cell
			cell[loc_inc].value = '=Gorkha!%s%i'%(col[p],i)	
			loc_inc+=1

	out.update_cells(cell)
cxn()
add()
