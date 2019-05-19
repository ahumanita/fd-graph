from math import sqrt

class Node :
	def __init__(self,id,x=(0,0),Adj=[],v=(1,1),a=(0,0),m=1) :
		self.x = x
		self.v = v
		self.a = a
		self.m = m
		self.id = id
		self.Adj = Adj

class Edge :
	def __init__(self,id,start,target,feather=0.02) :
		self.id = id
		self.start = start
		self.target = target
		self.feather = feather

class Graph :
	def __init__(self,V,E) :
		self.V = V
		self.E = E

	def update(self,width,height) :
		for node in self.V :
			# coord update
			if node.x[0]+node.v[0] >= width or node.x[0]+node.v[0] <= 0 or node.x[1]+node.v[1] >= height or node.x[1]+node.v[1] <= 0 :
					node.v = (-node.v[0],-node.v[1])
			else :
				node.x = (node.x[0]+node.v[0], node.x[1]+node.v[1])

			# acceleration update
			node.a = (node.a[0]+node.v[0],node.a[1]+node.v[1])

			# electric force update
			# elec = 100
			# for mnode in self.V :
			# 	if mnode != node :
			# 		dist = sqrt((node.x[0]-mnode.x[0])**2 + (node.x[1]-mnode.x[1])**2)
			# 		node.a = (node.a[0]+(node.x[0]-mnode.x[0])*elec/(dist**3)
			# 					,node.a[1]+(node.x[1]-mnode.x[1])*elec/(dist**3))

		for edge in self.E :
			# feather update
			start = self.V[edge.start]
			target = self.V[edge.target]
			start.a = (start.a[0]-edge.feather*(start.x[0]-target.x[0])
						,start.a[1]-edge.feather*(start.x[1]-target.x[1]))