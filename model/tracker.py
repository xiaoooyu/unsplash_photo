from time import time
from datetime import datetime

class Tracker:
	def __init__(self):
		self.taskStartAt = (int)(time() * 1000)
		self.taskNum = 0
		self.taskFinishedNum = 0

	def report(self):	
		now = int(time() * 1000)		
		elapse_time = datetime.now().strftime('%H:%M:%S')

		print("{0}: {1}/{2} tasks finished".format(elapse_time, self.taskFinishedNum, self.taskNum))

	def finishTask(self, n):
		self.taskFinishedNum += n

	def addTask(self, n):
		self.taskNum += n