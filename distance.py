import random
import numpy




class Distance:
	def __init__(self,input_file,solution_file):
		
		self.cities = [] 
		self.read_in_file(input_file)
		self.n = self.cities.shape[0]
		self.path = self.read_solution(solution_file)
		print(self.path)

	def run(self):
		dist = 0
		for i in range(0,self.path.shape[0] -1): 
			dist += self.cities[self.path[i],self.path[i+1]]

		print(dist)


	def read_in_file(self,input_file):
		
		with open(input_file) as textFile:
			self.cities = numpy.array([[int(d) if d.isdigit() else numpy.inf  for d in line.split()] for line in textFile])


	def read_solution(self,input_file):
		path=[]
		with open(input_file) as textFile:
			path = numpy.array([int(d) if d.isdigit() else numpy.inf  for d in textFile.readline().split()] )
		return path
		


_as = Distance("in_files\\29.in","sol.in")
_as.run()


