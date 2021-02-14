import requests

from os import path
import os

from time import time

import concurrent.futures

from model.photo import Photo
from model.tracker import Tracker
import database as dbutil

# api-endpoint
URL = "https://unsplash.com/napi/photos"
PAGE_SIZE = 12

MAX_DOWNLOAD_WORKER = 12

PARENT = "downloads"
DOWNLOAD = "downloads/current"
ARCHIVE = "downloads/all"
DELETE = "downloads/delete"

if not path.exists(PARENT):
	os.mkdir(PARENT)

if not path.exists(DOWNLOAD):
	os.mkdir(DOWNLOAD)
	
if not path.exists(ARCHIVE):
	os.mkdir(ARCHIVE)

if not path.exists(DELETE):
	os.mkdir(DELETE)

def get_filename(url):
	fragment_removed = url.split("#")[0]
	query_string_removed = fragment_removed.split("?")[0]
	schema_removed = query_string_removed.split("://")[-1].split(":")[-1]
	if schema_removed.find("/") == -1:
		return ""
	return path.basename(schema_removed)


def getPaging(page, downloadPhotoFn, tracker):
	params = {'per_page':PAGE_SIZE, 'page':page}
	r = requests.get(url = URL, params = params)

	data = r.json()
	
	print("PREPARE: create download task for Page: {0}".format(page))
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as downloadExecutor:
		
		executor = downloadExecutor
		#executor = None

		for d in data:						
			photo = Photo(d) 					
			
			if tracker is not None:
				tracker.addTask(1)				
			
			if executor is None:
				downloadPhotoFn(photo, tracker)
			else:			
				executor.submit(downloadPhotoFn, photo, tracker)


def downloadPhoto(photo, tracker):
	url = photo.full
	#url = photo.thumb	
	
	file_name = '{0}.jpg'.format(get_filename(url))
	download_file_name = path.join(DOWNLOAD, file_name)
	archive_file_name = path.join(ARCHIVE, file_name)
	delete_file_name = path.join(DELETE, file_name)

	if dbutil.fetchOneById(photo.id) is not None:
		print("SKIP: {0} has record".format(photo.id))

		if path.exists(archive_file_name):
			os.rename(archive_file_name, delete_file_name)

		if tracker is not None:
			tracker.finishTask(1)
			tracker.report()
		
		return

	if path.exists(archive_file_name):
		
		print("SKIP: downloading {0} becase exist of {1}, url {2}".format(file_name, archive_file_name, url))
		dbutil.insertOrUpdate(photo)
		os.rename(archive_file_name, delete_file_name)
		
		if tracker is not None:
			tracker.finishTask(1)
			tracker.report()
		
		return
	
	r_start_time = int(time() * 1000)
	r = requests.get(url = url)	
	open(download_file_name, 'wb').write(r.content)
	r_end_time = int(time() * 1000)

	r_using_time = r_end_time - r_start_time	

	print("FINISH: downloading {0}(use {1} ms)"
		.format(file_name, r_using_time))
	
	dbutil.insertOrUpdate(photo)

	if tracker is not None:
		tracker.finishTask(1)
		tracker.report()

	# if dbutil.fetchOneById(photo.id) is None:		
	# 	print("DB: {0} has no records, try to insert one".format(photo.id))
		
	# else:
	# 	print("SKIP: {0} has record".format(photo.id))
