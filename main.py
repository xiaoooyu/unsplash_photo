import biz.photo as biz
from model.tracker import Tracker

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
	
	input_page = input("input page num to start:")
	page = 1
	try:
		page = int(input_page)
	except ValueError:
		page = 1
	
	biz.scanPageAndFindDedicatePhoto(page, tracker)

if __name__ == "__main__":
	main3()