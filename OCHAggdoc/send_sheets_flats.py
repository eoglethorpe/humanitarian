import inc_flatfile

#d_names = [ 'Gorkha', 'Dhading', 'Nuwakot', 'Lamjung', 
d_names = ['Rasuwa', 'Ramechap', 'Dolakha', 'Bhaktapur', 'Kathmandu']

for v in d_names:
	inc_flatfile.do_sheet(v)
	reload(inc_flatfile)
