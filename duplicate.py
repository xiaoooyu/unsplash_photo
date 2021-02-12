
import os
from os import path

SOURCE = "downloads"
TARGET = "downloads-all"

if __name__ == "__main__":
	duplicates = set()

	for filename in os.listdir(SOURCE):
		if path.exists(path.join(TARGET, filename)):			
			duplicates.add(filename)

	print(len(duplicates))
	text = input("input 'y' to delete duplicate files:")
	if text == "y":		
		for filename in duplicates:
			os.remove(path.join(SOURCE, filename))