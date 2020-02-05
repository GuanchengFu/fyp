import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
	'fyp.settings')

import django
django.setup()
from  core.models import File, Folder

"""
This script will construct a file architecture looks like this:
user1:
--test file 1
--test file 2
--test file 3
--test folder 1
   --test file 4
   --test file 5
   --test folder 2
      --test folder 3
      --test folder 4
         --test file 6
"""

def populate():
	separate_files = [
		{'description': "test file 1"},
		{'description': "test file 2"},
		{'description': "test file 3"},
	]

	folder_1 = [
		{'description': "test file 4"},
		{'description': "test file 5"},
	]

	folder_2 = [
		{}
	]

	folder_4 = [
		{'description': "test file 6"}
	]

	folder = [
		{'name': "test folder 1",
		'folder': None,
		'files': folder_1},
		{'name': "test folder 2",
		'folder': "test folder 1",
		'files': folder_2},
		{'name': "test folder 4",
		'folder': "test folder 2",
		'files': folder_4},
	]

	# des = "description"   detail = "test file 1" 
	for f in folder:
		name = f['name']
		folder = f['folder']
		new_folder = add_folder(name, folder)
		for file in f['files']:
			if file:
				description = file['description']
				add_file(description, new_folder)
		#print("Folder with name {0} was added successfully".format(name))


	for file in separate_files:
		description = file['description']
		add_file(description, None)


def add_folder(name, folder):
	if folder:
		print(folder)
		f = Folder.objects.get(name = folder)
	else:
		f = None
	new_folder = Folder(name = name, folder = f)
	new_folder.save()
	return new_folder


def add_file(descript, folder):
	#if folder is null
	f = File(description = descript, folder = folder)
	f.save()
	return f


if __name__ == '__main__':
	print('Starting file population test script...')
	populate()

	for folder in Folder.objects.all():
		for file in folder.files.all():
			print("{0} - {1}".format(folder, file))
