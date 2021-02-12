# importing the request library
import requests

from os import path
import os

import concurrent.futures

#
DOWNLOAD = "downloads"
ARCHIVE = "downloads-all"

# api-endpoint
URL = "https://unsplash.com/napi/photos"
PAGE_SIZE = 12
MAX_WORKER = 50

def get_filename(url):
	fragment_removed = url.split("#")[0]
	query_string_removed = fragment_removed.split("?")[0]
	schema_removed = query_string_removed.split("://")[-1].split(":")[-1]
	if schema_removed.find("/") == -1:
		return ""
	return path.basename(schema_removed)

def download_photo(url):
	
	file_name = get_filename(url)
	download_file_name = '{0}/{1}.jpg'.format(DOWNLOAD, file_name)
	archive_file_name = path.join(ARCHIVE, file_name)
	#print("START: {0} downloading @{1}".format(url, final_file_name))

	if path.exists(archive_file_name):
		print("SKIP: downloading {0} becase exist of {1} ".format(url, archive_file_name))
		return
	
	r = requests.get(url = url)	
	open(download_file_name, 'wb').write(r.content)
	print("FINISH: download {0} @{1}".format(url, download_file_name))


def get_photo(page, executor):
	# os.mkdir(path.join(FOLDER, str(page)))

	PARAMS = {'per_page':PAGE_SIZE, 'page':page}
	r = requests.get(url = URL, params = PARAMS)

	data = r.json()
	
	print("start download page: {0}".format(page))
	for d in data:
		full = d['urls']['full']
		# print(full.path)			
		# download_photo(full)
		executor.submit(download_photo, full)

if __name__ == "__main__":
	if not path.exists(DOWNLOAD):
		os.mkdir(DOWNLOAD)
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
		for i in range(1, 51):
			get_photo(i, executor)
