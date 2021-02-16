import concurrent.futures

import biz.photo as biz
from model.tracker import Tracker

MAX_PROFILE_WORKER = 12

def main():
	tracker = Tracker()	
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PROFILE_WORKER) as profile_executor:		
			for i in range(2001, 4001):				
				profile_executor.submit(biz.getPaging, i, biz.downloadPhoto, tracker)
				#biz.getPaging(i, biz.downloadPhoto, tracker)

def main2():
	tracker = Tracker()
	input_page = input("input page num to start:")
	page = int(input_page)
	while True:	
		biz.getPaging(page, biz.downloadPhoto, tracker)
		page += 1
		input("Continue to download page {0}?".format(page))		

def main3():
	tracker = Tracker()
	biz.scanPageAndFindDedicatePhoto(1, tracker)

if __name__ == "__main__":
	main3()