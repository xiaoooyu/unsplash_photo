import requests

from os import path
import os

from time import time

import concurrent.futures

from model.photo import Photo
from model.page import Page
from model.tracker import Tracker

DRY_RUN = False

# api-endpoint
URL = "https://unsplash.com/napi/photos"
PAGE_SIZE = 30

MAX_DOWNLOAD_WORKER = 30
MAX_SCAN_WORKER = 10

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


def getPaging(pageIndex, downloadPhotoFn, tracker):
	pageObject = Page(URL, pageIndex, PAGE_SIZE)
	
	photos = pageObject.fetchPhotos()
	
	print("PREPARE: create download task for Page: {0}".format(pageIndex))
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as downloadExecutor:
		
		executor = downloadExecutor
		#executor = None

		for photo in photos:			
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

	if Photo.fetchOneById(photo.id) is not None:
		print("SKIP: {0} has record".format(photo.id))

		if path.exists(archive_file_name):
			print("SKIP: downloading {0} becase exist of {1}, url {2}".format(file_name, archive_file_name, url))
			os.rename(archive_file_name, delete_file_name)

		if tracker is not None:
			tracker.finishTask(1)
			tracker.report()
		
		return

	if path.exists(archive_file_name):
		print("SKIP: downloading {0} becase exist of {1}, url {2}".format(file_name, archive_file_name, url))
		
		photo.insertOrUpdate()
		os.rename(archive_file_name, delete_file_name)
		
		if tracker is not None:
			tracker.finishTask(1)
			tracker.report()
		
		return
	
	if DRY_RUN == False:
		r_start_time = int(time() * 1000)
		r = requests.get(url = url)	
		open(download_file_name, 'wb').write(r.content)
		r_end_time = int(time() * 1000)

		r_using_time = r_end_time - r_start_time	

		print("FINISH: downloading {0}(use {1} ms)"
			.format(file_name, r_using_time))
		
		photo.insertOrUpdate()
	else:
		print("DRYRUN: downloading {0}".format(file_name))

	if tracker is not None:
		tracker.finishTask(1)
		tracker.report()

def scanPageAndFindDedicatePhoto(initPage, tracker):
	page = initPage
	buff = []
	key = ''
	while not key == 'd':		
		with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_SCAN_WORKER) as scanExecutor:
			for i in range(page, page + 10):
				scanExecutor.submit(findDedicateInPage, i, buff)
				#findDedicateInPage(i, buff)
		key = input("Find qulified photo: {1}. Press 'd' to download, any other key to continue.".format(page, len(buff)))		
		page += 10

	input("{0} quanlified photos have found, press key to continue".format(len(buff)))	

	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKER) as downloadExecutor:
		executor = downloadExecutor
		#executor = None

		for photo in buff:			
			
			if tracker is not None:
				tracker.addTask(1)				
			
			if executor is None:
				downloadPhoto(photo, tracker)
			else:			
				executor.submit(downloadPhoto, photo, tracker)

	
def findDedicateInPage(pageIndex, buff):
	print("START: scan page {0}".format(pageIndex))	
	page = Page(URL, pageIndex, PAGE_SIZE)	
	for photo in page.fetchPhotos():
		if Photo.fetchOneById(photo.id) is None:
			buff.append(photo)
			print("SCAN: {0} is qulified because cannot find record locally".format(photo.id))
		else:
			print("SKIP: {0} has a local record.".format(photo.id))
