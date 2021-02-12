# importing the request library
import requests

from os import path
import os

from time import time

import concurrent.futures

from model.photo import Photo
import database as dbutil

#
DOWNLOAD = "downloads"
ARCHIVE = "downloads-all"

# api-endpoint
URL = "https://unsplash.com/napi/photos"
PAGE_SIZE = 12
MAX_PROFILE_WORKER = 4
MAX_DOWNLOAD_WORKER = 12

G_TASKS = 0
G_TASKS_FINISHED = 0

G_START_TIME = 0

class DownloadFileInfo:
	def __init__(self, url, page):
		self.url = url
		self.page = page
	

def get_filename(url):
	fragment_removed = url.split("#")[0]
	query_string_removed = fragment_removed.split("?")[0]
	schema_removed = query_string_removed.split("://")[-1].split(":")[-1]
	if schema_removed.find("/") == -1:
		return ""
	return path.basename(schema_removed)

def report_task_progress():
	global G_TASKS_FINISHED
	global G_START_TIME

	now = (int)(time() * 1000)
	G_TASKS_FINISHED += 1
	elapse_time = now - G_START_TIME

	print("{0}: {1}/{2} tasks finished".format(elapse_time, G_TASKS_FINISHED, G_TASKS))

def download_photo(downloadFileInfo, photo):
	#url = photo.full
	url = photo.thumb
	page = downloadFileInfo.page

	file_name = '{0}.jpg'.format(get_filename(url))
	download_file_name = path.join(DOWNLOAD, file_name)
	archive_file_name = path.join(ARCHIVE, file_name)	

	if path.exists(archive_file_name):
		print("SKIP: Page:{0} downloading {1} becase exist of {2}, url {3}".format(page, file_name, archive_file_name, url))
		report_task_progress()
		return
	
	r_start_time = int(time() * 1000)
	r = requests.get(url = url)	
	open(download_file_name, 'wb').write(r.content)
	r_end_time = int(time() * 1000)

	r_using_time = r_end_time - r_start_time	

	print("FINISH: Page:{0} downloading {1}(use {2} ms)"
		.format(page, file_name, r_using_time))
	report_task_progress()
	
	#if dbutil.fetchOneById(photo.id) is None:		
	#	dbutil.insertOrUpdate(photo)

def get_photo(page):
	
	# os.mkdir(path.join(FOLDER, str(page)))

	PARAMS = {'per_page':PAGE_SIZE, 'page':page}
	r = requests.get(url = URL, params = PARAMS)

	data = r.json()
	
	print("PREPARE: create download task for Page: {0}".format(page))
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as executor:
		for d in data:
			full = d['urls']['full']
			info = DownloadFileInfo(full, page)
			photo = Photo(d)
			
			global G_TASKS
			G_TASKS += 1
			
			if executor is None:
				download_photo(info, photo)
			else:			
				executor.submit(download_photo, info, photo)

if __name__ == "__main__":
	if not path.exists(DOWNLOAD):
		os.mkdir(DOWNLOAD)
	
	G_START_TIME = int(time() * 1000)
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROFILE_WORKER) as profile_executor:		
			for i in range(1, 10):
				#profile_executor.submit(get_photo, i, executor)
				profile_executor.submit(get_photo, i)
				# get_photo(i, executor)
				# get_photo(i, None)