data= [11,None,442,None,54,435,16,87,18]

def norm(un_norm):
	print un_norm
	print "un //"
	valid = True
	try:
		minv = int(min(int(v) for v in un_norm if v is not None and v.isdigit()))
		maxv = int(max(int(v) for v in un_norm if v is not None and v.isdigit()))
		print "min " + str(minv)
		print "max " + str(maxv)
	except:
		#if there are no vald entries in an array (hopefully)
		valid = False
	finally:
		norm = []
		for x in un_norm:
			if x is not None and x.isdigit() and valid:
				x = int(x)
				if maxv-minv != 0:
					norm+=['%.4f' % ((x-minv+.0)/(maxv-minv+.0))]
				else:
					norm+='1'
			else:
				norm+=['']
	return norm
