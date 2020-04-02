import datetime


def generate_file_name(time, filename):
	"""
	Rename the file as 202004021726
	"""
	return '{%Y%m%d%H%M%S}'.format(datetime.datetime.now()) + filename