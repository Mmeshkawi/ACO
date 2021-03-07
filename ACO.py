import random
import numpy




class AS:
	_ALPHA= 1
	_BETA = 1
	_C = 1 # inital value of Tij which is small positive contant C
	
	_Q = 1
	_P = 0.2
	#r is a coefficient such that (1 - r) represents the evaporation of trail between time t and t+n
	#https://www.hindawi.com/journals/mpe/2016/6469721/

	def __init__(self,input_file,m,NC_max):
		
		self.t= 0 #time counter
		self.NC = 0 # cycles counter
		self.m = m # number of ants
		self._NC_max=NC_max # number of cycles
		
		self.tabu = [] # visited cities

		self.cities = [] 
		self.read_in_file(input_file)
		self.n = self.cities.shape[0]
		#self.print_arr('cities',self.cities)
		

		#For every edge (i,j) set an initial value tij(t)=c for trail intensity and Dtij= 0 
		self.t_intensity = numpy.empty(shape=(self.n,self.n))
		self.t_intensity.fill(AS._C)
		numpy.fill_diagonal(self.t_intensity, 0)

		#self.t_intensity = [[_C if self.cities[i][j] != 0 else 0 for j in range(0,self.n)] for i in range(0,self.n)]
		#self.print_arr('t_intensity',self.t_intensity)

		#Place the m ants on the n nodes
		pass

		

		self.shortest_tour = None
		self.shortest_tour_distance = numpy.inf
			
	def run(self):
		
		while self.NC < self._NC_max:
			self.s = 0 # s is the tabu list index
			#Place the starting town of the k-th ant in tabuk(s)
			#
			self.tabu = numpy.array([[random.randint(0,self.n-1)]  for i in range(0,self.m)],dtype=int) # ints are positioned on different towns		
			self.L= numpy.empty(shape=(self.m))
			self.L.fill(0)
			
		
			for i in range(0,self.n): #3- Repeat until tabu list is full {this step will be repeated (n-1) times}
				# it is mentioned in the psuedo code that this loop should be repeated (n-1), but i think it should be n because of the last move which is to the start city
				self.s = self.s+1
				
				_shortest = numpy.inf
				_shortest_i = None

				_next_cities =  numpy.empty(shape=(self.m,1),dtype=int)

				for k in range(0,self.m):
					#3- Choose the town j to move to, with probability pij k (t) given by equation (4)
					if i != self.n -1:
						next_city = self.next_city(k)
					else:
						next_city=self.tabu[k][0] # back to start city

					#Move the k-th ant to the town j
					_next_cities[k][0] =int(next_city)  # set the last item to next_city, the last item has -1 as intitial value
					
					#4- Compute the length Lk of the tour described by the k-th ant
					self.L[k] += self.cities[self.tabu[k][-1]][next_city]
					
					#4- Update the shortest tour found
					if _shortest > self.L[k]:
						_shortest = self.L[k]
						_shortest_i = k

				self.tabu = numpy.append(self.tabu,_next_cities,axis=1)
			if self.shortest_tour_distance > _shortest:
				self.shortest_tour_distance = _shortest
				self.shortest_tour = numpy.copy(self.tabu[_shortest_i] )

			self.delta_t = numpy.empty(shape=(self.n,self.n))
			self.delta_t.fill(0)
			#4- 
			for _i in range(0,self.n):
				for _j in range(0,self.n):#For every edge (i,j)
					for _k in range(0,self.m):
						if _i not in self.tabu[k]:#if (i, j) belongs to tour described by tabu_k
							continue

						_ind_i = numpy.where(self.tabu[_k]==_i)[0]
						if _ind_i.shape !=(1,):
							continue

						if _ind_i[0] +1 >= self.tabu[_k].shape[0]: #_ind_i[0] +1 is _j
							continue

						if self.tabu[k][_ind_i[0] +1] != _j: # the ant did not go from _i to _j
							continue

						self.delta_t[_i][_j] += AS._Q/ self.L[_k]

			#5 - For every edge (i,j) compute tij(t+n) according to equation tij(t+n)=p.tij(t)+Delta_t_ij	
			for _i in range(0,self.n):
				for _j in range(0,self.n):
					self.t_intensity[_i][_j] = AS._P * self.t_intensity[_i][_j] +self.delta_t[_i][_j]
			self.t += self.n
			self.NC +=1

		print(self.shortest_tour)
		print(self.shortest_tour_distance)
		#print(numpy.amin(self.L))

	def next_city(self,k):#,j):
		#Choose the town j to move to, with probability pij k (t) given by equation (4)
		i= self.tabu[k][-1]
		_t_intensity_i = self.t_intensity[i]
		_t_intensity_i = numpy.copy(_t_intensity_i)
		_t_intensity_i[list(self.tabu[k])] = 0 # if city j is no visited by ant k

		_a = _t_intensity_i ** AS._ALPHA * ((1.0 / self.cities[i]) ** AS._BETA)# equation (4)

		# _a = ((self.t_intensity[i][j] ** self._ALPHA  ) * ( (1/ self.cities[i][j])** self._BETA))
		# _b = sum([(self.t_intensity[i][z] ** self._ALPHA )*( (1/ self.cities[i][z])** self._BETA))  for z in range(0,self.n) if z not in self.tabu[k]])
		
		prob_all = _a / _a.sum()

		max_ind = numpy.argwhere(prob_all == numpy.amax(prob_all))
		max_ind = max_ind.flatten().tolist()

		if len(max_ind) != 1:#TODO select random city if more than one has the same max probability 
			aa = max_ind[0]
			print('!!!multiple max probability')


		return max_ind[0]

	def read_in_file(self,input_file):
		
		with open(input_file) as textFile:
			self.cities = numpy.array([[int(d) if d.isdigit() else numpy.inf  for d in line.split()] for line in textFile])



	def print_arr(self,arr_name,arr):
			print(f'{arr_name}->')
			for i in arr:
				print(i)



_as = AS("in_files\\29.in",m=15,NC_max=40)

_as.run()


