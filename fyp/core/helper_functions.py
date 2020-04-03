import datetime


def generate_time_prefix():
	"""
	Return ddmmyyhhmmss format of the current time.
	"""
	return datetime.datetime.now().strftime('%d%m%y%I%M%S')
