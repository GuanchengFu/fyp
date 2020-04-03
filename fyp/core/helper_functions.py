import datetime


def generate_time_prefix(file_name):
	"""
	Add a prefix which is a timestamp to the file_name.
	"""
	time = datetime.datetime.now().strftime('%d%m%y%I%M%S')
	return time + '_' + file_name
