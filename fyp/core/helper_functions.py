import datetime


def generate_time_prefix(file_name):
	"""
	Add a prefix which is a timestamp to the file_name.
	"""
	time = datetime.datetime.now().strftime('%d%m%y%I%M%S')
	return time + '_' + file_name


def contain_invalid_char(s):
	if '*' in s:
		return True
	if '\\' in s:
		return True
	if '/' in s:
		return True
	if ':' in s:
		return True
	if '?' in s:
		return True
	if '"' in s:
		return True
	if '<' in s:
		return True
	if '>' in s:
		return True
	if '|' in s:
		return True


def validate_add_user(user, add_user):
	"""
	Validate whether the searched user is a validate choice.
	"""
	if user.is_candidate:
		return add_user.is_professor
	elif user.is_professor:
		return add_user.is_candidate
	else:
		return False
