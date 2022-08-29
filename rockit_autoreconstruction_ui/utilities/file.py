def read_ascii(filename=''):
	'''return contain of an ascii file'''
	with open(filename, 'r') as f:
		text = f.read()
	return text