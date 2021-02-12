# importing the request library
import requests

import concurrent.futures

from model.photo import Photo
from model.tracker import Tracker

import database as dbutil

import biz.photo as biz

MAX_PROFILE_WORKER = 4

if __name__ == "__main__":
	tracker = Tracker()	
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROFILE_WORKER) as profile_executor:		
			for i in range(1, 10):				
				profile_executor.submit(biz.getPaging, i, biz.downloadPhoto, tracker)
				#biz.getPaging(i, biz.downloadPhoto, tracker)